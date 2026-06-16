"""
Model-agnostic LLM provider. Supports Gemini (default) and Anthropic (optional).
Swap providers by setting LLM_PROVIDER in .env.
Includes automatic retry with backoff for transient API errors (429, 503, etc.).
"""

import json
import time
import urllib.request
import urllib.error
from shared.config import get_secret

MAX_RETRIES = 3
RETRY_DELAYS = [1, 3, 6]  # seconds between retries


def get_provider():
    return get_secret("LLM_PROVIDER", "gemini")


def call_llm(prompt: str, system: str = "", model: str = None) -> str:
    provider = get_provider()
    if provider == "gemini":
        return _call_with_retry(_call_gemini, prompt, system, model)
    elif provider == "anthropic":
        return _call_with_retry(_call_anthropic, prompt, system, model)
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")


def _call_with_retry(fn, prompt: str, system: str, model: str) -> str:
    """Retry LLM calls on transient HTTP errors (429, 500, 502, 503, 504)."""
    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            return fn(prompt, system, model)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < MAX_RETRIES - 1:
                last_error = e
                time.sleep(RETRY_DELAYS[attempt])
            else:
                raise RuntimeError(
                    f"LLM API error (HTTP {e.code}) after {attempt + 1} attempt(s). "
                    f"This is usually a temporary issue — try again in a few seconds."
                ) from e
        except urllib.error.URLError as e:
            if attempt < MAX_RETRIES - 1:
                last_error = e
                time.sleep(RETRY_DELAYS[attempt])
            else:
                raise RuntimeError(
                    f"Network error connecting to LLM API after {attempt + 1} attempt(s). "
                    f"Check your internet connection and try again."
                ) from e
    raise last_error


def _call_gemini(prompt: str, system: str = "", model: str = None) -> str:
    api_key = get_secret("GEMINI_API_KEY")

    model = model or "gemini-2.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    contents = []
    if system:
        contents.append({"role": "user", "parts": [{"text": system}]})
        contents.append({"role": "model", "parts": [{"text": "Understood. I will follow these instructions."}]})
    contents.append({"role": "user", "parts": [{"text": prompt}]})

    payload = json.dumps({"contents": contents}).encode()
    req = urllib.request.Request(
        f"{url}?key={api_key}",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())

    return data["candidates"][0]["content"]["parts"][0]["text"]


def _call_anthropic(prompt: str, system: str = "", model: str = None) -> str:
    api_key = get_secret("ANTHROPIC_API_KEY")

    model = model or "claude-sonnet-4-20250514"
    url = "https://api.anthropic.com/v1/messages"

    payload = json.dumps({
        "model": model,
        "max_tokens": 4096,
        "system": system or "You are a helpful assistant.",
        "messages": [{"role": "user", "content": prompt}],
    }).encode()

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )

    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())

    return data["content"][0]["text"]

"""
Model-agnostic LLM provider. Supports Gemini (default) and Anthropic (optional).
Swap providers by setting LLM_PROVIDER in .env.
"""

import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()


def get_provider():
    return os.getenv("LLM_PROVIDER", "gemini")


def call_llm(prompt: str, system: str = "", model: str = None) -> str:
    provider = get_provider()
    if provider == "gemini":
        return _call_gemini(prompt, system, model)
    elif provider == "anthropic":
        return _call_anthropic(prompt, system, model)
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")


def _call_gemini(prompt: str, system: str = "", model: str = None) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set in .env")

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
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in .env")

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

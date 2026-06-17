"""
Slack connector. Reads recent messages from a Slack channel using Bot Token.

Setup:
1. Go to https://api.slack.com/apps → Create New App → From Scratch
2. Add Bot Token Scopes: channels:history, channels:read
3. Install to workspace, copy Bot User OAuth Token
4. Add SLACK_BOT_TOKEN and SLACK_CHANNEL_ID to .env
"""

import requests
from shared.config import get_secret


def _get_headers():
    token = get_secret("SLACK_BOT_TOKEN")
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def read_channel_messages(limit: int = 20) -> list[dict]:
    """Read recent messages from the configured Slack channel.

    Returns list of dicts with keys: user, text, timestamp.
    """
    channel_id = get_secret("SLACK_CHANNEL_ID")
    url = "https://slack.com/api/conversations.history"
    params = {"channel": channel_id, "limit": limit}

    resp = requests.get(url, headers=_get_headers(), params=params)
    resp.raise_for_status()
    data = resp.json()

    if not data.get("ok"):
        raise RuntimeError(f"Slack API error: {data.get('error', 'unknown')}")

    messages = []
    for msg in data.get("messages", []):
        if msg.get("subtype") in ("channel_join", "channel_leave", "bot_message"):
            continue
        messages.append({
            "user": msg.get("user", "unknown"),
            "text": msg.get("text", ""),
            "timestamp": msg.get("ts", ""),
        })

    return messages


def get_channel_name() -> str:
    """Get the name of the configured Slack channel."""
    channel_id = get_secret("SLACK_CHANNEL_ID")
    url = "https://slack.com/api/conversations.info"
    params = {"channel": channel_id}

    resp = requests.get(url, headers=_get_headers(), params=params)
    resp.raise_for_status()
    data = resp.json()

    if not data.get("ok"):
        return "unknown-channel"

    return data.get("channel", {}).get("name", "unknown-channel")

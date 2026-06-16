"""
Config helper. Reads from .env locally, falls back to st.secrets on Streamlit Cloud.
"""

import os
from dotenv import load_dotenv

load_dotenv()


def get_secret(key: str, default: str = None) -> str:
    """Get a config value from .env or st.secrets."""
    value = os.getenv(key)
    if value:
        return value

    try:
        import streamlit as st
        if key in st.secrets:
            return st.secrets[key]
    except (ImportError, AttributeError):
        pass

    if default is not None:
        return default
    raise ValueError(f"{key} not set. Add it to .env or Streamlit secrets.")

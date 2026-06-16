"""
Shared Google authentication. Returns credentials for any Google API.
Supports both local (.env with JSON file) and Streamlit Cloud (st.secrets with JSON string).
"""

import os
import json
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/documents.readonly",
]


def get_google_credentials():
    # Option 1: Streamlit Cloud — credentials stored as JSON string in st.secrets
    try:
        import streamlit as st
        if "GOOGLE_CREDENTIALS_JSON" in st.secrets:
            info = json.loads(st.secrets["GOOGLE_CREDENTIALS_JSON"])
            return service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    except (ImportError, AttributeError):
        pass

    # Option 2: Local — credentials stored as a JSON file path in .env
    creds_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
    if not creds_path:
        raise ValueError("No Google credentials found. Set GOOGLE_CREDENTIALS_PATH in .env or GOOGLE_CREDENTIALS_JSON in st.secrets.")

    if not os.path.isabs(creds_path):
        creds_path = os.path.join(os.path.dirname(__file__), "..", "..", creds_path)

    return service_account.Credentials.from_service_account_file(creds_path, scopes=SCOPES)

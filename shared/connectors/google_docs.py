"""
Google Docs connector. Reads document content and returns plain text.
"""

from googleapiclient.discovery import build
from .google_auth import get_google_credentials
from shared.config import get_secret


def _get_service():
    return build("docs", "v1", credentials=get_google_credentials())


def read_doc() -> str:
    """Read the Google Doc and return its full text content."""
    doc_id = get_secret("GOOGLE_DOC_ID")

    service = _get_service()
    doc = service.documents().get(documentId=doc_id).execute()

    text_parts = []
    for element in doc.get("body", {}).get("content", []):
        if "paragraph" in element:
            for run in element["paragraph"].get("elements", []):
                if "textRun" in run:
                    text_parts.append(run["textRun"]["content"])

    return "".join(text_parts)

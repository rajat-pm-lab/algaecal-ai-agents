"""
Google Sheets connector. Reads sheet data and returns structured dicts.
"""

from googleapiclient.discovery import build
from .google_auth import get_google_credentials
from shared.config import get_secret


def _get_service():
    return build("sheets", "v4", credentials=get_google_credentials())


def read_sheet(sheet_name: str, range_suffix: str = "") -> list[dict]:
    """Read a named sheet tab and return rows as list of dicts (header row = keys)."""
    sheet_id = get_secret("GOOGLE_SHEET_ID")

    range_str = f"'{sheet_name}'"
    if range_suffix:
        range_str += f"!{range_suffix}"

    service = _get_service()
    result = service.spreadsheets().values().get(
        spreadsheetId=sheet_id, range=range_str
    ).execute()

    rows = result.get("values", [])
    if len(rows) < 2:
        return []

    headers = rows[0]
    return [dict(zip(headers, row)) for row in rows[1:]]


def read_all_sheets() -> dict[str, list[dict]]:
    """Read all sheet tabs and return {tab_name: [rows]}."""
    sheet_id = get_secret("GOOGLE_SHEET_ID")
    service = _get_service()

    metadata = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
    tab_names = [s["properties"]["title"] for s in metadata["sheets"]]

    data = {}
    for tab in tab_names:
        data[tab] = read_sheet(tab)
    return data

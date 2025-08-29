import time
from typing import List, Optional
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Spreadsheet + worksheets (set the spreadsheet name in secrets)
SPREADSHEET_NAME = st.secrets["google_sheet"]["name"]
CANDIDATES_WS = "candidates"
RESPONSES_WS  = "responses"

# --- Auth via Streamlit secrets (works locally & on Cloud) ---
_creds = Credentials.from_service_account_info(st.secrets["gspread_service_account"])
_client = gspread.authorize(_creds)

def _open_or_create_worksheet(spreadsheet, title: str, headers: List[str]):
    try:
        ws = spreadsheet.worksheet(title)
    except gspread.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(title=title, rows=1000, cols=max(10, len(headers)))
        ws.append_row(headers)
    # Ensure headers exist (first row)
    first_row = ws.row_values(1)
    if [h.lower() for h in first_row] != [h.lower() for h in headers]:
        if first_row:
            # Replace row 1 with headers
            ws.delete_rows(1)
        ws.insert_row(headers, 1)
    return ws

def init_db():
    """Create spreadsheet tabs and headers if missing."""
    ss = _client.open(SPREADSHEET_NAME)
    _open_or_create_worksheet(ss, CANDIDATES_WS,
        ["id","name","email","phone","experience","position","location","tech_stack","timestamp"])
    _open_or_create_worksheet(ss, RESPONSES_WS,
        ["candidate_id","question","answer","timestamp"])

def _get_candidates_ws():
    ss = _client.open(SPREADSHEET_NAME)
    return ss.worksheet(CANDIDATES_WS)

def _get_responses_ws():
    ss = _client.open(SPREADSHEET_NAME)
    return ss.worksheet(RESPONSES_WS)

def _next_candidate_id(ws) -> int:
    values = ws.col_values(1)  # id column (including header)
    if len(values) <= 1:
        return 1
    # last non-empty id
    for v in reversed(values[1:]):
        try:
            return int(v) + 1
        except:
            continue
    return 1

def insert_candidate(name: str, email: str, phone: str, experience: int,
                     position: str, location: str, tech_stack: str) -> int:
    ws = _get_candidates_ws()
    cid = _next_candidate_id(ws)
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    ws.append_row([cid, name, email, phone, experience, position, location, tech_stack, ts])
    return cid

def get_candidate_by_id(candidate_id: int) -> Optional[list]:
    """
    Return the row as a list matching header order:
    [id, name, email, phone, experience, position, location, tech_stack, timestamp]
    """
    ws = _get_candidates_ws()
    ids = ws.col_values(1)[1:]  # skip header
    for idx, v in enumerate(ids, start=2):  # row index in sheet
        try:
            if int(v) == int(candidate_id):
                return ws.row_values(idx)
        except:
            continue
    return None

def insert_response(candidate_id: int, question: str, answer: str):
    ws = _get_responses_ws()
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    ws.append_row([candidate_id, question, answer, ts])






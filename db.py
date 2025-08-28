import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# ---------------- Google Sheets Setup ----------------

# Read service account JSON from Streamlit secrets
creds_json = st.secrets["gspread_service_account"]

# Load credentials
creds_dict = json.loads(creds_json)
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Open your Google Sheet by name
sheet_name = st.secrets["google_sheet_name"]  # e.g., "Talentscout Responses"
candidates_sheet = client.open(sheet_name).worksheet("candidates")
responses_sheet = client.open(sheet_name).worksheet("responses")

# ---------------- Insert Functions ----------------

def insert_candidate(name, email, phone, experience, position, location, tech_stack):
    all_rows = candidates_sheet.get_all_values()
    candidate_id = len(all_rows)  # simple incremental id
    candidates_sheet.append_row([candidate_id, name, email, phone, experience, position, location, tech_stack])
    return candidate_id

def insert_response(candidate_id, question, answer):
    responses_sheet.append_row([candidate_id, question, answer])

# ---------------- Fetch Functions ----------------

def get_all_candidates():
    return candidates_sheet.get_all_values()[1:]  # skip header

def get_responses_for_candidate(candidate_id):
    rows = responses_sheet.get_all_values()[1:]  # skip header
    return [(q, a) for cid, q, a in rows if int(cid) == int(candidate_id)]



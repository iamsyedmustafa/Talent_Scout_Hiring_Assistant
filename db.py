import gspread
import json
from google.oauth2.service_account import Credentials

# Path to your service account JSON file (keep this file in your project folder)
SERVICE_ACCOUNT_FILE = "service_account.json"

# Google Sheets name
SHEET_NAME = "Talentscout Responses"   # change this to your sheet name

# Load credentials from JSON file
with open(SERVICE_ACCOUNT_FILE, "r") as f:
    creds_dict = json.load(f)

# Define the scope
scopes = ["https://www.googleapis.com/auth/spreadsheets"]

# Authorize with Google
credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
client = gspread.authorize(credentials)

# Open the spreadsheet
spreadsheet = client.open(SHEET_NAME)

# Access both sheets
candidates_sheet = spreadsheet.worksheet("candidates")
responses_sheet = spreadsheet.worksheet("responses")

# ---------- Utility Functions ---------- #

def add_candidate(candidate_data):
    """
    Add a new candidate to the candidates sheet.
    candidate_data should be a list in this order:
    [id, name, email, phone, experience, position, location, tech_stack]
    """
    candidates_sheet.append_row(candidate_data)

def add_response(response_data):
    """
    Add a response to the responses sheet.
    response_data should be a list in this order:
    [candidate_id, question, answer]
    """
    responses_sheet.append_row(response_data)

def get_all_candidates():
    """Fetch all candidates"""
    return candidates_sheet.get_all_records()

def get_all_responses():
    """Fetch all responses"""
    return responses_sheet.get_all_records()





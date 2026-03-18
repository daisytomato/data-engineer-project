"""
Writes scraped job data to a Google Sheet.
Creates the sheet on first run; appends/overwrites daily on subsequent runs.

Required env vars:
  GOOGLE_SERVICE_ACCOUNT_JSON  – full JSON of a service account key
  GOOGLE_SHEET_ID              – ID of the target Google Sheet (from URL)
"""

import os
import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

COLUMNS = [
    "Job Title",
    "Company",
    "Location",
    "Employment Type",
    "Salary",
    "Date Posted",
    "Source",
    "Searched Role",
    "Apply Link",
    "Job Description",
]

TAB_NAME_FORMAT = "%Y-%m-%d"   # one tab per day


def get_client() -> gspread.Client:
    sa_json = os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
    creds_dict = json.loads(sa_json)
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    return gspread.authorize(creds)


def write_to_sheet(jobs: list[dict]) -> str:
    """Write jobs to Google Sheet. Returns the sheet URL."""
    client = get_client()
    sheet_id = os.environ["GOOGLE_SHEET_ID"]
    spreadsheet = client.open_by_key(sheet_id)

    tab_name = datetime.utcnow().strftime(TAB_NAME_FORMAT)

    # Delete existing tab for today if re-running
    try:
        existing = spreadsheet.worksheet(tab_name)
        spreadsheet.del_worksheet(existing)
        print(f"[INFO] Replaced existing tab: {tab_name}")
    except gspread.WorksheetNotFound:
        pass

    worksheet = spreadsheet.add_worksheet(title=tab_name, rows=500, cols=len(COLUMNS))

    # Header row with formatting request
    rows = [COLUMNS]
    for job in jobs:
        row = [job.get(col, "") for col in COLUMNS]
        rows.append(row)

    worksheet.update(rows, value_input_option="USER_ENTERED")

    # Bold header + freeze top row
    spreadsheet.batch_update({
        "requests": [
            {
                "repeatCell": {
                    "range": {
                        "sheetId": worksheet.id,
                        "startRowIndex": 0,
                        "endRowIndex": 1,
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
                            "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
                        }
                    },
                    "fields": "userEnteredFormat(textFormat,backgroundColor)",
                }
            },
            {
                "updateSheetProperties": {
                    "properties": {
                        "sheetId": worksheet.id,
                        "gridProperties": {"frozenRowCount": 1},
                    },
                    "fields": "gridProperties.frozenRowCount",
                }
            },
            # Auto-resize all columns
            {
                "autoResizeDimensions": {
                    "dimensions": {
                        "sheetId": worksheet.id,
                        "dimension": "COLUMNS",
                        "startIndex": 0,
                        "endIndex": len(COLUMNS),
                    }
                }
            },
        ]
    })

    sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}"
    print(f"[INFO] Written {len(jobs)} jobs to tab '{tab_name}': {sheet_url}")
    return sheet_url


if __name__ == "__main__":
    with open("jobs.json") as f:
        jobs = json.load(f)
    write_to_sheet(jobs)

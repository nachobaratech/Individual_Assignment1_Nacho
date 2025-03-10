import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Authenticate Google Sheets
SERVICE_ACCOUNT_FILE = "JSON_individual-task-453011-2bfd3a329abb.json"  # Your actual JSON file
SHEET_ID = "1g3DVcrxEt2jT3oPBAFGJ8G1o4DjgZghChD21ez0ZriM"  #  actual Sheet ID
SHEET_NAME = "Sheet1"  # sheet name

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
)
client = gspread.authorize(credentials)

# Open Google Sheet
sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

# Fetch dataset from Google Sheets
data = sheet.get_all_records()
df = pd.DataFrame(data)

print("Dataset loaded from Google Sheets:")
print(df.head())  # Display first few rows

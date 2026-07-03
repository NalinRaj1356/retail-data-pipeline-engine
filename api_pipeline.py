import os
import sqlite3
from datetime import datetime
import pandas as pd
import requests
from dotenv import load_dotenv

# 1. Initialization and Security Configuration
load_dotenv()
API_KEY = os.getenv("MY_SECRET_API_KEY")
URL = "https://httpbin.org/headers"
DB_FILE = "pipeline_warehouse.db"

if not API_KEY:
    print("CRITICAL ERROR: 'MY_SECRET_API_KEY' was not found!")
    exit()

headers = {
    "X-API-Key": API_KEY,
    "User-Agent": "DataPipelineEngine/2.0",
    "Accept": "application/json",
}

print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ingestion job initialized.")

try:
    # 2. Extract Data from API
    response = requests.get(URL, headers=headers, timeout=10)

    if response.status_code == 200:
        print("Extraction Successful! Status 200 OK.")
        raw_payload = response.json()

        # 3. Transform Data into Pandas DataFrame
        extracted_headers = raw_payload.get("headers", {})
        df = pd.DataFrame(
            list(extracted_headers.items()),
            columns=["Metadata_Key", "Metadata_Value"],
        )
        df["Ingested_At"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 4. Load Data to Database (The New Append Engine)
        # We establish a connection to our local SQLite database file
        conn = sqlite3.connect(DB_FILE)

        # We append the DataFrame directly into a table named 'api_logs'
        # if_exists='append' ensures we add rows to the bottom rather than wiping old data!
        df.to_sql("api_logs", conn, if_exists="append", index=False)

        # Close the warehouse connection securely
        conn.close()

        print(
            f"Load Successful! Appended {len(df)} rows to database warehouse: {DB_FILE}"
        )
    else:
        print(f"PIPELINE ERROR: HTTP Status Code {response.status_code}")

except Exception as e:
    print(f"UNEXPECTED PIPELINE CRASH: {e}")
import os
import sqlite3
import time
from datetime import datetime
import pandas as pd
import requests

# 1. Pipeline Settings
# Pulling live arrival data for London St Pancras International (Station ID: 940GZZLUZSP)
URL = "https://api.tfl.gov.uk/StopPoint/940GZZLUWLO/Arrivals"
DB_FILE = "pipeline_warehouse.db"

print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Live UK Rail Ingestion Job Initialized.")

try:
    # 2. Extraction Layer (Fetching genuine, live public transit streams)
    # The TfL API is public and does not require an API key for baseline requests
    response = requests.get(URL, timeout=10)

    if response.status_code == 200:
        print("Live Extraction Successful! Status 200 OK.")
        raw_trains = response.json()

        # If the station happens to have no active trains in the vector, handle it gracefully
        if not raw_trains:
            print("No active train telemetry detected at this timestamp.")
            exit()

        live_rail_records = []
        
        # 3. Transformation Layer (Parsing live JSON stream into structured relational columns)
        # We will loop through the first 5 live trains currently approaching the station
        for train in raw_trains[:5]:
            # Convert raw ISO timestamps from the API into readable strings
            expected_time_raw = train.get("expectedArrival")
            
            # Format the timestamp nicely if it exists
            if expected_time_raw:
                expected_dt = datetime.strptime(expected_time_raw, "%Y-%m-%dT%H:%M:%SZ")
                expected_arrival = expected_dt.strftime("%Y-%m-%d %H:%M:%S")
            else:
                expected_arrival = "N/A"

            # Calculate a critical business metric: Time to station in minutes
            time_to_station_seconds = train.get("timeToStation", 0)
            minutes_away = round(time_to_station_seconds / 60, 1)

            record = {
                "Train_ID": train.get("vehicleId", "UNKNOWN"),
                "Line_Name": train.get("lineName"),
                "Destination": train.get("destinationName"),
                "Minutes_Until_Arrival": minutes_away,
                "Expected_Arrival_Time": expected_arrival,
                "Current_Location": train.get("currentLocation"),
                "Ingested_At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            live_rail_records.append(record)

        # Convert our array of real-time records into a clean DataFrame
        df = pd.DataFrame(live_rail_records)

        print("\n--- Live St Pancras Rail Telemetry Stream ---")
        print(df.to_string(index=False))
        print("---------------------------------------------\n")

        # 4. Loading Layer (Appending live data to a production warehouse table)
        conn = sqlite3.connect(DB_FILE)
        df.to_sql("live_uk_rail", conn, if_exists="append", index=False)
        conn.close()

        print(f"Success! Appended live public transit metrics to database table: 'live_uk_rail'")
    else:
        print(f"PIPELINE ERROR: Live transit API responded with status code {response.status_code}")

except Exception as e:
    print(f"CRITICAL TRANSIT PIPELINE CRASH: {e}")
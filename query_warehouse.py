import sqlite3
import pandas as pd

DB_FILE = "pipeline_warehouse.db"

# Establish connection to the warehouse
conn = sqlite3.connect(DB_FILE)

print("--- ANALYTICS CONSOLE: LIVE UK TRANSIT WAREHOUSE ---")

try:
    # Query 1: Calculate Total Rows Collected So Far
    query_total = "SELECT COUNT(*) as total_records FROM live_uk_rail;"
    total_df = pd.read_sql(query_total, conn)
    print(f"\n[Metric] Total Live Rail Rows Ingested: {total_df['total_records'].values[0]}")

    # Query 2: View the Latest Ingestion Cycle
    # This pulls the absolute freshest data that entered the warehouse
    print("\n--- Fresh Data Assets Inside 'live_uk_rail' ---")
    query_fresh = """
    SELECT Train_ID, Line_Name, Destination, Minutes_Until_Arrival, Expected_Arrival_Time, Ingested_At 
    FROM live_uk_rail 
    ORDER BY Ingested_At DESC 
    LIMIT 10;
    """
    fresh_df = pd.read_sql(query_fresh, conn)
    print(fresh_df.to_string(index=False))

except Exception as e:
    print(f"DATABASE QUERY ERROR: {e}")
    print("Tip: Make sure the rail_pipeline.py has run successfully at least once to create the table.")

# Securely close the warehouse connection
conn.close()
import sqlite3
import pandas as pd

DB_FILE = "pipeline_warehouse.db"

# Establish connection to the warehouse
conn = sqlite3.connect(DB_FILE)

print("--- ANALYTICS CONSOLE: QUERYING PRODUCTION WAREHOUSE ---")

# Query 1: Calculate Total Rows Collected So Far
query_total = "SELECT COUNT(*) as total_records FROM api_logs;"
total_df = pd.read_sql(query_total, conn)
print(f"\n[Metric] Total API Metadata Rows Ingested: {total_df['total_records'].values[0]}")


# Query 2: Find Unique Timestamps (How many times has the script run?)
query_runs = "SELECT DISTINCT Ingested_At FROM api_logs ORDER BY Ingested_At DESC;"
runs_df = pd.read_sql(query_runs, conn)
print(f"[Metric] Number of Pipeline Cycles Logged: {len(runs_df)}")


# Query 3: Deep-Dive Analysis (Filter for specific security headers)
# We use standard SQL WHERE and LIKE clauses to look for specific records
query_analysis = """
SELECT Metadata_Key, Metadata_Value, Ingested_At 
FROM api_logs 
WHERE Metadata_Key LIKE '%key%' OR Metadata_Key = 'user-agent'
ORDER BY Ingested_At DESC;
"""
analysis_df = pd.read_sql(query_analysis, conn)

print("\n--- Security & Header Configuration Audit Log ---")
print(analysis_df.to_string(index=False))

# Securely close the warehouse connection
conn.close()
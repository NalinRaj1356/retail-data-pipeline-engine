import pandas as pd
from datetime import datetime

# 1. Read the raw data we extracted earlier
input_file = "api_extraction_output.csv"
print(f"Reading raw data from: {input_file}")

try:
    df = pd.read_csv(input_file)

    print("\n--- Step 1: Raw Data Loaded ---")
    print(df)

    # 2. Transformation: Clean the metadata keys (Make them all lowercase)
    df["Metadata_Key"] = df["Metadata_Key"].str.lower()

    # 3. Transformation: Filter the dataset
    # Let's keep only rows where the key contains 'key', 'user', or 'accept'
    keywords = ["key", "user", "accept"]
    df_filtered = df[df["Metadata_Key"].str.contains("|".join(keywords))].copy()

    # 4. Transformation: Enrich the data (Add a Lineage/Audit tracking column)
    df_filtered["Data_Steward"] = "Data_Engineering_Team"
    df_filtered["Last_Modified_At"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print("\n--- Step 2: Transformed & Filtered Data ---")
    print(df_filtered)

    # 5. Load: Export the clean data as a premium Excel report
    output_excel = "final_analytics_report.xlsx"
    df_filtered.to_excel(output_excel, index=False, sheet_name="API_Metadata")
    
    print(f"\nTransformation Complete! Clean report saved as: {output_excel}")

except FileNotFoundError:
    print(f"Error: Could not find '{input_file}'. Make sure you run your first script first!")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
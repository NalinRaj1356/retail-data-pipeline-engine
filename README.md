# Real-Time UK Rail Transit Ingestion & Analytics Engine

A production-grade, end-to-end data engineering pipeline that ingests live, real-time public transit telemetry from the Transport for London (TfL) API, structures complex time-series data elements, and loads them into a relational database warehouse.

## 🛠️ System Architecture & Data Flow

1. **Live Ingestion Layer:** Establishes direct connections to the public TfL API gateway to scrape real-time arrival vectors for major transport hubs like London Waterloo.
2. **Data Transformation & Engineering:** Processes raw nested JSON streams, handles chronological ISO timestamp formatting, and dynamically derives business-critical operational metrics (e.g., calculating real-time arrival proximity in minutes).
3. **Relational Warehousing:** Persists streaming data assets into an optimized SQLite data warehouse (`pipeline_warehouse.db`) via transactional append operations to build a historical analytical timeline.
4. **Automation Scheduler:** Managed by a Unix background daemon (`cron`) configured to run on a stable production cadence with comprehensive error-stream redirection logging.

## 📂 Project Directory Map

* `rail_pipeline.py` — Core ETL pipeline script handling live network extraction, transformation logic, and warehouse ingestion.
* `pipeline_warehouse.db` — Local relational database storage layer tracking real-time transit history (excluded from source control).
* `rail_pipeline.log` — Active system log file capturing print statements and network exception streams.
* `.gitignore` — Security filter ensuring localized database binaries and configuration logs remain secure.

## 📈 Live Transit Warehouse Schema Design

The pipeline maps unstructured streaming payloads into a structured relational table named `live_uk_rail`:

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| **Train_ID** | TEXT | Unique vehicle identifier tracking the specific active rolling stock. |
| **Line_Name** | TEXT | The operational transit line (e.g., Bakerloo, Jubilee). |
| **Destination** | TEXT | Target station terminal destination for the approaching train. |
| **Minutes_Until_Arrival**| REAL | Calculated delta marking exactly how close the train is to the platform. |
| **Expected_Arrival_Time**| TEXT | Formatted relational timestamp indicating estimated arrival. |
| **Current_Location** | TEXT | Real-time physical track sector telemetry or last recorded station block. |
| **Ingested_At** | TEXT | High-precision chronological marker capturing database load execution time. |
# Resilient Retail Inventory Ingestion & Analytics Engine

A production-grade, end-to-end data engineering pipeline designed to ingest live retail transactional telemetry, manage target warehouse schemas locally, handle network faults gracefully, and provide structured analytical audit capabilities. 

## 🛠️ System Architecture & Data Flow

1. **Ingestion Layer:** Connects to public API gateways to fetch storefront transactional logs using robust HTTP headers.
2. **Resiliency & Fault-Tolerance:** Engineered with a 3-tier exponential backoff retry mechanism to intercept network outages (e.g., HTTP 503) and features an automated failover mock stream to protect pipeline execution continuity.
3. **Storage & Warehousing:** Migrates data away from volatile flat files into an organized relational SQLite data warehouse (`pipeline_warehouse.db`) utilizing historical append engines.
4. **Analytics Layer:** A dedicated script leveraging Pandas and SQL logic to extract business-critical key performance indicators (KPIs) directly from the live database.
5. **Automation Scheduler:** Configured via a Unix background daemon (`cron`) to manage execution on a clean production cadence.

## 📂 Project Directory Map

* `retail_pipeline.py` — Core ETL pipeline script handling network resiliency, data transformation, and warehouse loading.
* `query_warehouse.py` — Analytics script executing SQL queries to generate inventory audit metrics.
* `pipeline_warehouse.db` — Relational database storage layer tracking transactional history (untracked in version control).
* `retail_pipeline.log` — Dedicated logging file tracking pipeline execution status and error streams.
* `.gitignore` — Security filter ensuring sensitive configuration keys and binary database files remain localized.

## 📈 Enterprise Retail Schema Design

The ingestion pipeline maps unstructured data streams into a structured relational table named `retail_inventory`:

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| **SKU** | TEXT | Unique stock-keeping unit identifier for retail items. |
| **Product_Name** | TEXT | Descriptive title of the retail asset. |
| **Category** | TEXT | Operational department classification (e.g., Beauty, Healthcare). |
| **Current_Stock** | INTEGER | Real-time units remaining in inventory. |
| **Units_Sold_Today**| INTEGER | Total transaction volume recorded for the active date. |
| **Restock_Alert_Flag**| INTEGER | Binary business exception flag (1 = Active, 0 = Healthy). Triggers automatically if stock drops below 20 units. |
| **Ingested_At** | TEXT | Chronological timestamp marking database warehouse insertion. |

## 🚀 Key Engineering Demonstrations

* **Automated Exception Handling:** Demonstrates how to design systems that self-heal during third-party service degradation using backoff algorithms.
* **Decoupled Business Logic:** Implements logic that automatically isolates low-stock conditions to assist logistics teams with automated replenishment.
* **Secure Environment Management:** Separates infrastructure keys and credentials from source-controlled code files.
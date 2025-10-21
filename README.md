# DEPI Graduation Project: Real-time IoT Data Pipeline

## Project Planning

### 1. Project Overview
This project involves building a comprehensive, end-to-end data pipeline that simulates real-time IoT sensor data (temperature and humidity). The pipeline will process this data using both batch (ETL) and real-time streaming techniques, demonstrating orchestration, real-time analytics, and cloud-native processing.

### 2. Objectives
The primary goals for this project are:
* **Simulate & Ingest:** Create a Python script to simulate IoT sensor data and ingest it into a message queue (Apache Kafka).
* **Batch Process:** Build a batch ETL pipeline (using Python or Azure Data Factory) to extract the data, perform transformations (e.g., averaging, flagging anomalies), and load it into a structured data warehouse (SQL or Data Lake).
* **Stream Process:** Implement a streaming pipeline (using Azure Stream Analytics or Kafka) to process data in real-time and raise alerts for threshold breaches.
* **Visualize:** Create a real-time dashboard (using Power BI or Streamlit) to visualize key metrics and system performance.

### 3. Scope
* **In-Scope:** Data generation, message queue implementation (Kafka), batch ETL processing, data warehousing, real-time stream processing, and data visualization/dashboarding.
* **Out-of-Scope:** This project does not include the management of physical IoT hardware or the development of advanced machine learning models (beyond simple anomaly flagging).

### 4. Project Milestones
The project is divided into four key milestones:
* **Milestone 1: Data Simulation and Ingestion**
    * **Deliverable:** Python generator script and sample data logs (from Kafka consumer).
    * **Status:** ✅ **Completed** (Using `generator.py`, `consumer.py`, and Docker for Kafka).
* **Milestone 2: Batch Data Pipeline (ETL)**
    * **Deliverable:** ETL script or Azure Data Factory pipeline and the processed dataset in storage (SQL/Data Lake).
    * **Status:** ⏳ **In Progress**
* **Milestone 3: Streaming Pipeline with Alerts**
    * **Deliverable:** Streaming pipeline setup (e.g., Azure Stream Analytics) and the alert logic/output.
    * **Status:** ◻️ **Not Started**
* **Milestone 4: Dashboard & Final Report**
    * **Deliverable:** A live dashboard or screenshot and a final PDF report summarizing the project.
    * **Status:** ◻️ **Not Started**

### 5. Technologies
* **Data Generation:** Python
* **Messaging/Streaming:** Apache Kafka, Docker, Azure Stream Analytics
* **Batch ETL:** Python (Pandas) or Azure Data Factory
* **Data Storage:** SQL Database or Azure Data Lake
* **Visualization:** Power BI or Streamlit

---

## Stakeholder Analysis

This project simulates a real-world scenario. The primary stakeholders would be the end-users of this data.

| Stakeholder Role | Interest in Project |
| :--- | :--- |
| **Operations Manager** | Needs a real-time dashboard (Milestone 4) to monitor sensor status. Requires immediate alerts (Milestone 3) if a sensor reports dangerous values (e.g., overheating) to prevent equipment failure. |
| **Data Analyst** | Needs access to clean, aggregated historical data in the data warehouse (Milestone 2). Will use this data to analyze long-term trends, identify patterns in sensor behavior, and create reports. |
| **DEPI Project Reviewers** | Interested in the technical implementation of all four milestones. Will evaluate the successful use of Kafka, the batch ETL process, the streaming alerts, and the final dashboard as per the project requirements. |

---

## Database Design

⏳ **Status: In Progress**

*(This section will contain the Entity-Relationship Diagram (ERD) and schema design for the SQL data warehouse from Milestone 2).*

---

## UI/UX Design

⏳ **Status: In Progress**

*(This section will contain mockups or a link to a Figma design for the real-time dashboard from Milestone 4).*
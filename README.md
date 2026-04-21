# 🏎️ F1 Race Intelligence

A hybrid Formula 1 analytics platform combining a real-time layer (OpenF1 API → Streamlit) for live race data and a batch layer (Jolpica API → BigQuery → dbt) for historical analysis across the 2020–2024 seasons — deployed live on Streamlit Community Cloud.

**[🔗 Live Demo](https://f1-race-intelligence.streamlit.app/)** 

---

## 🏗️ Architecture
![Architecture Diagram](docs/architecture.png) ← add later

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Live Ingestion | Python, OpenF1 API |
| Batch Ingestion | Python, Jolpica API (Ergast) |
| Data Warehouse | Google BigQuery |
| Transformation | dbt (dbt-bigquery) |
| Dashboard | Streamlit |
| Version Control | Git, GitHub |

---

## 📊 Dashboard Pages

### 🔴 Live Pages (OpenF1)
- **Live Timing** — Real-time race standings, lap times, sector times, gap to leader
- **Team Radio** — Browse and listen to team radio recordings by session and driver
- **Race Control** — Live flags, safety cars, penalties, and steward decisions

### 📅 Historical Pages (Jolpica + BigQuery + dbt)
- **Race Results** — Full race classification for any race across 2020–2024
- **Driver Performance** — Career stats, lap consistency, best circuits, positions gained
- **Head to Head** — Teammate comparisons with win rate and finish position charts
- **Championship Standings** — Season points progression for drivers and constructors
- **Race Strategy** — Pit stop analysis and tyre degradation per race
- **Circuit Profiles** — Circuit characteristics, fastest tracks, overtaking opportunities
- **Constructor Efficiency** — Team points, DNF rates, pit stop performance

---

## 🗄️ Data Pipeline

**Raw Layer** (`f1_raw` dataset)
- `raw_races` — Full race results per round
- `raw_sprint_races` — Sprint race results
- `raw_lap_times` — Lap times per driver per race
- `raw_pit_stops` — Pit stop records per driver per race

**dbt Transformations** (`f1_dbt` dataset)
- 4 Staging models — Type casting and cleaning
- 2 Dimension tables — Driver and constructor lookup
- 8 Intermediate models — Business logic and analytics calculations
- 5 Mart models — Analytics-ready tables for the dashboard

---

## 🚀 Running Locally

### Prerequisites
- Python 3.11+
- Google Cloud account with BigQuery enabled
- Service account with BigQuery Data Viewer + Job User roles

### Setup

```bash
# Clone the repo
git clone https://github.com/safeu/f1-race-intelligence.git
cd f1-race-intelligence

# Create virtual environment
py -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Fill in your GCP_PROJECT_ID, KEY_PATH, BQ_DATASET

# Run ingestion
py -m ingestion.run_ingestion

# Run dbt transformations
cd dbt/f1_pipeline
dbt run

# Launch dashboard
streamlit run app.py
```

---

## 📁 Project Structure
```
f1-race-intelligence/
├── app.py                      # Streamlit entry point
├── requirements.txt
├── .env.example
│
├── ingestion/
│   ├── jolpica.py              # Jolpica API ingestion with pagination
│   └── run_ingestion.py        # Main ingestion runner
│
├── dbt/f1_pipeline/
│   └── models/
│       ├── staging/            # 4 models — cleaning and type casting
│       ├── dimensions/         # 2 models — driver and constructor lookup
│       ├── intermediate/       # 8 models — business logic
│       └── marts/              # 5 models — analytics-ready tables
│
├── pages/                      # 10 Streamlit dashboard pages
│
├── utils/
│   ├── bigquery_client.py      # BigQuery connection
│   ├── streamlit_bigquery.py   # Cached BigQuery queries for Streamlit
│   ├── openf1_client.py        # OpenF1 API client for live data
│   ├── config.py               # Environment variables and constants
│   ├── transforms.py           # Data flattening utilities
│   └── driver_images.py        # Driver photo fetching
│
└── docs/
└── architecture.png            # Architecture diagram
```
---

## 🔮 Planned Enhancements
- Expand historical data to 26 seasons (2000–2025)
- OpenF1 batch ingestion for post-race historical storage
- Apache Airflow orchestration for automated pipeline runs
- Docker containerization
- Architecture diagram

---

*Data sourced from [Jolpica API](https://api.jolpi.ca/) and [OpenF1](https://openf1.org/) • 2020–2024 Formula 1 seasons*

---
### Sample .env structure
- GCP_PROJECT_ID=your-gcp-project-id
- KEY_PATH=credentials.json
- BQ_DATASET=f1_raw
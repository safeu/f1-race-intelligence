# 🏎️ F1 Race Intelligence

An automated Formula 1 data pipeline and analytics dashboard ingesting historical race data from the Jolpica API into BigQuery, with dbt transformations surfacing pit strategy efficiency, driver consistency scores, tyre degradation curves, and championship progression across the 2020–2024 seasons.

**[🔗 Live Demo](your-streamlit-url-here)** ← update after deployment

---

## 🏗️ Architecture
![Architecture Diagram](docs/architecture.png) ← add later

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Ingestion | Python, Requests |
| Data Warehouse | Google BigQuery |
| Transformation | dbt (dbt-bigquery) |
| Dashboard | Streamlit |
| Version Control | Git, GitHub |

---

## 📊 Dashboard Pages

- **Driver Performance** — Individual driver stats, lap consistency, best circuits, career points
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
git clone https://github.com/yourusername/f1-race-intelligence.git
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
├── ingestion/              # API extraction scripts
│   ├── jolpica.py          # Jolpica API ingestion
│   └── run_ingestion.py
├── dbt/f1_pipeline/        # dbt transformation project
│   ├── models/
│   │   ├── staging/
│   │   ├── intermediate/
│   │   ├── dimensions/
│   │   └── marts/
├── pages/                  # Streamlit dashboard pages
├── utils/                  # Shared utilities
│   ├── bigquery_client.py
│   ├── config.py
│   ├── transforms.py
│   └── streamlit_bigquery.py
└── app.py                  # Streamlit entry point
```

---

*Data sourced from [Jolpica API](https://api.jolpi.ca/) (Ergast replacement) • 2020–2024 Formula 1 seasons*

---
### Sample .env structure
- GCP_PROJECT_ID=your-gcp-project-id
- KEY_PATH=credentials.json
- BQ_DATASET=f1_raw
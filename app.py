"""
===========================================================
F1 Race Intelligence - Home Page
===========================================================
Script purpose:
    Main entry point for the Streamlit dashboard.
    Shows app overview and quick stats.
"""

import streamlit as st
from utils.streamlit_bigquery import get_bq_client, run_query
from utils.config import GCP_PROJECT_ID

st.set_page_config(
    page_title="F1 Race Intelligence",
    page_icon="🏎️",
    layout="wide"
)

st.title("🏎️ F1 Race Intelligence")
st.markdown("""
Welcome to the F1 Race Intelligence dashboard — an automated data pipeline 
ingesting live telemetry and historical race data from dual APIs into BigQuery, 
with dbt models surfacing pit strategy efficiency, driver consistency scores, 
and tyre degradation curves.

*Data covers the 2020–2024 Formula 1 seasons. Currently only have Jolpica API (OpenF1 API in the works)*
""")

st.divider()

st.subheader("📊 Dataset Overview")

stats_query = f"""
    SELECT
        COUNT(DISTINCT driver_id) AS total_drivers,
        COUNT(DISTINCT season) AS total_seasons,
        COUNT(DISTINCT CONCAT(CAST(season AS STRING), '-', CAST(round_num AS STRING))) AS total_races,
        COUNT(*) AS total_entries
    FROM `{GCP_PROJECT_ID}.f1_dbt.mart_driver_performance`
"""

stats = run_query(stats_query)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🏁 Total Races", int(stats['total_races'][0]))
with col2:
    st.metric("👤 Total Drivers", int(stats['total_drivers'][0]))
with col3:
    st.metric("📅 Seasons Covered", int(stats['total_seasons'][0]))
with col4:
    st.metric("📝 Total Entries", int(stats['total_entries'][0]))

st.divider()


st.subheader("🏆 2024 Championship Summary")
champion_query = f"""
    SELECT
        driver_name,
        driver_code,
        MAX(cumulative_drivers_points) AS total_points
    FROM `{GCP_PROJECT_ID}.f1_dbt.mart_championship_standings`
    WHERE season = 2024
    GROUP BY driver_name, driver_code
    ORDER BY total_points DESC
    LIMIT 5
"""

champion_df = run_query(champion_query)

st.markdown("**Top 5 Drivers — 2024 Season**")
st.dataframe(
    champion_df[['driver_name', 'driver_code', 'total_points']],
    hide_index=True,
    use_container_width=True
)

st.divider()
st.caption("Data sourced from Jolpica API (Ergast) • Built with Python, dbt, BigQuery & Streamlit")
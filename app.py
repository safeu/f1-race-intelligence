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

*Data covers the 2010–2026 Formula 1 seasons. With Jolpica API handling 2010-2025 and OpenF1 API handling recent and live race weekends*
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


st.subheader("🏆 2025 Championship Summary")
latest_season = f"SELECT MAX(season) FROM `{GCP_PROJECT_ID}.f1_dbt.mart_championship_standings`"
champion_query = f"""
    SELECT
        driver_name,
        driver_code,
        MAX(cumulative_drivers_points) AS total_points
    FROM `{GCP_PROJECT_ID}.f1_dbt.mart_championship_standings`
    WHERE season = ({latest_season})
    GROUP BY driver_name, driver_code
    ORDER BY total_points DESC
    LIMIT 5
"""

champion_df = run_query(champion_query)

st.markdown("**Top 5 Drivers — 2025 Season**")
st.dataframe(
    champion_df[['driver_name', 'driver_code', 'total_points']],
    hide_index=True,
    use_container_width=True
)
st.divider()



st.subheader("🏆 Past Formula 1 Champions")
champions_query = f"""
    SELECT
        season,
        driver_name,
        driver_code,
        MAX(cumulative_drivers_points) AS total_points
    FROM `{GCP_PROJECT_ID}.f1_dbt.mart_championship_standings`
    WHERE season != ({latest_season})
    GROUP BY season, driver_name, driver_code
    QUALIFY ROW_NUMBER() OVER (PARTITION BY season ORDER BY MAX(cumulative_drivers_points) DESC) = 1
    ORDER BY season DESC
"""

champion_df = run_query(champions_query)

st.markdown("**From 2010 - 2024 Seasons**")
st.dataframe(
    champion_df[['driver_name', 'driver_code', 'total_points']],
    hide_index=True,
    use_container_width=True
)

st.divider()
st.caption("Data sourced from Jolpica API (Ergast) • Built with Python, dbt, BigQuery & Streamlit")
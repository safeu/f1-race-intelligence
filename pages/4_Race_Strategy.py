"""
===========================================================
F1 Race Intelligence - Page 3 Race Strategy
===========================================================
Script purpose:
    Create race strategy page. Analyzes race strategy of teams
    within races.
"""

import streamlit as st
import plotly.express as px
from utils.streamlit_bigquery import run_query
from utils.config import GCP_PROJECT_ID
from utils.config import CONSTRUCTOR_COLORS

st.set_page_config(page_title="Race Strategy", page_icon="🏎️", layout="wide")
st.title("🏎️ Race Strategy")
st.caption("Note: Work in Progress Still")

season_query = f"""
    SELECT
        DISTINCT
            season
    FROM `{GCP_PROJECT_ID}.f1_dbt.mart_race_strategy_outcome`
    ORDER BY season DESC
"""
season_df = run_query(season_query)
selected_season = st.selectbox("Select Season", options=season_df['season'])

st.divider()

round_query = f"""
    SELECT
        DISTINCT
            season,
            round_num
    FROM `{GCP_PROJECT_ID}.f1_dbt.mart_race_strategy_outcome`  
    WHERE season = {selected_season}
    ORDER BY round_num DESC
"""
round_df = run_query(round_query)
selected_round = st.selectbox("Select Round Number", options=round_df['round_num'])

pit_stop_query = f"""
    SELECT
        season,
        round_num,
        driver_code,
        driver_name,
        num_stops,
        total_pit_duration,
        avg_pit_duration,
        stint_number,
        avg_lap_delta,
        degradation_slope
    FROM `{GCP_PROJECT_ID}.f1_dbt.mart_race_strategy_outcome`  
    WHERE season = {selected_season}
        AND round_num = {selected_round}
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY season, round_num, driver_name, stint_number
        ORDER BY avg_pit_duration
    ) = 1
"""

strategy_df = run_query(pit_stop_query)

st.subheader("🔧 Pit Stop Summary")
st.dataframe(
    strategy_df[['driver_code', 'driver_name', 'num_stops', 
                 'total_pit_duration', 'avg_pit_duration']],
    hide_index=True,
    use_container_width=True
)

st.subheader("📉 Tyre Degradation by Stint")
fig = px.line(
    strategy_df,
    x='stint_number',
    y='degradation_slope',
    color='driver_code',
    title=f"Tyre Degradation — Season {selected_season} Round {selected_round}",
    labels={'stint_number': 'Stint', 'degradation_slope': 'Degradation Slope'}
)
st.plotly_chart(fig, use_container_width=True)



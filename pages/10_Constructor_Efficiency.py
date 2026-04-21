"""
===========================================================
F1 Race Intelligence - Page 10 Constructor Efficiency
===========================================================
Script purpose:
    To view constructor efficiency data

"""

import streamlit as st
import plotly.express as px
from utils.streamlit_bigquery import run_query
from utils.config import GCP_PROJECT_ID, CONSTRUCTOR_COLORS

st.set_page_config(page_title="Constructor Efficiency", page_icon="🔧", layout="wide")
st.title("🔧 Constructor Efficiency")

season_query = f"""
    SELECT DISTINCT season
    FROM `{GCP_PROJECT_ID}.f1_dbt.mart_constructor_efficiency`
    ORDER BY season DESC
"""
season_df = run_query(season_query)
selected_season = st.selectbox("Select Season", options=season_df['season'])

constructor_query = f"""
    SELECT
        constructor_id,
        constructor_name,
        total_season_points,
        ROUND(dnf_rate * 100, 1) AS dnf_rate_pct,
        ROUND(avg_pit_duration, 3) AS avg_pit_duration
    FROM `{GCP_PROJECT_ID}.f1_dbt.mart_constructor_efficiency`
    WHERE season = {selected_season}
    ORDER BY total_season_points DESC
"""
constructor_df = run_query(constructor_query)

st.divider()

st.subheader("🏆 Constructor Points")
fig1 = px.bar(
    constructor_df,
    x='constructor_name',
    y='total_season_points',
    title=f"{selected_season} Constructor Points",
    labels={'constructor_name': 'Constructor', 'total_season_points': 'Points'},
    color='constructor_name',
    color_discrete_map=CONSTRUCTOR_COLORS
)
st.plotly_chart(fig1, width='stretch')

st.subheader("💥 DNF Rate")
fig2 = px.bar(
    constructor_df.sort_values('dnf_rate_pct', ascending=False),
    x='constructor_name',
    y='dnf_rate_pct',
    title=f"{selected_season} DNF Rate by Constructor (%)",
    labels={'constructor_name': 'Constructor', 'dnf_rate_pct': 'DNF Rate (%)'},
    color='constructor_name',
    color_discrete_map=CONSTRUCTOR_COLORS
)
st.plotly_chart(fig2, width='stretch')

st.subheader("⏱️ Avg Pit Stop Duration")
fig3 = px.bar(
    constructor_df.sort_values('avg_pit_duration'),
    x='constructor_name',
    y='avg_pit_duration',
    title=f"{selected_season} Average Pit Stop Duration",
    labels={'constructor_name': 'Constructor', 'avg_pit_duration': 'Avg Duration (s)'},
    color='constructor_name',
    color_discrete_map=CONSTRUCTOR_COLORS
)
st.plotly_chart(fig3, width='stretch')

st.divider()
st.subheader("📋 Full Constructor Data")
constructor_df['rank'] = range(1, len(constructor_df) + 1)
st.dataframe(
    constructor_df[['rank', 'constructor_name', 'total_season_points', 
                    'dnf_rate_pct', 'avg_pit_duration']],
    hide_index=True,
    width='stretch'
)
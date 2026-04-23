"""
===========================================================
F1 Race Intelligence - Page 9 Circuit Profiles
===========================================================
Script purpose:
    To analyze/view profile of different circuits
"""

import streamlit as st
import plotly.express as px
from utils.streamlit_bigquery import run_query
from utils.config import GCP_PROJECT_ID

st.set_page_config(page_title="Circuit Profiles", page_icon="🏁", layout="wide")
st.title("🏁 Circuit Profiles")
st.caption("Circuit characteristics averaged across 2010-2025 seasons")

circuits_query = f"""
    SELECT
        circuit_id,
        race_name,
        seasons_held,
        ROUND(avg_lap_time_sec, 3) AS avg_lap_time_sec,
        ROUND(avg_pit_stops, 2) AS avg_pit_stops,
        ROUND(avg_pit_duration, 3) AS avg_pit_duration,
        ROUND(avg_positions_changed, 2) AS avg_positions_changed
    FROM `{GCP_PROJECT_ID}.f1_dbt.mart_circuit_profiles`
    ORDER BY race_name
"""
circuits_df = run_query(circuits_query)

selected_circuit = st.selectbox("Select Circuit", options=circuits_df['race_name'])
circuit_data = circuits_df[circuits_df['race_name'] == selected_circuit].iloc[0]

st.divider()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("⏱️ Avg Lap Time", f"{circuit_data['avg_lap_time_sec']}s")
with col2:
    st.metric("🔧 Avg Pit Stops", circuit_data['avg_pit_stops'])
with col3:
    st.metric("⏳ Avg Pit Duration", f"{circuit_data['avg_pit_duration']}s")
with col4:
    st.metric("📈 Avg Positions Changed", circuit_data['avg_positions_changed'])

st.divider()

st.subheader("⚡ Fastest Circuits")
fig1 = px.bar(
    circuits_df.sort_values('avg_lap_time_sec'),
    x='race_name',
    y='avg_lap_time_sec',
    title="Average Lap Time by Circuit",
    labels={'race_name': 'Circuit', 'avg_lap_time_sec': 'Avg Lap Time (s)'},
    color='avg_lap_time_sec',
    color_continuous_scale='RdYlGn_r'
)
fig1.update_xaxes(tickangle=45)
st.plotly_chart(fig1, width='stretch')

st.subheader("📈 Overtaking Opportunities")
fig2 = px.bar(
    circuits_df.sort_values('avg_positions_changed', ascending=False),
    x='race_name',
    y='avg_positions_changed',
    title="Average Positions Changed by Circuit",
    labels={'race_name': 'Circuit', 'avg_positions_changed': 'Avg Positions Changed'},
    color='avg_positions_changed',
    color_continuous_scale='Blues'
)
fig2.update_xaxes(tickangle=45)
st.plotly_chart(fig2, width='stretch')

st.divider()
st.subheader("📋 Full Circuit Data")
st.dataframe(
    circuits_df[['race_name', 'seasons_held', 'avg_lap_time_sec', 
                 'avg_pit_stops', 'avg_pit_duration', 'avg_positions_changed']],
    hide_index=True,
    width='stretch'
)
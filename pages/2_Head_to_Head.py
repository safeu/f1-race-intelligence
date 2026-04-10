"""
===========================================================
F1 Race Intelligence - Page 2 Head to Head
===========================================================
Script purpose:
    Create Head to Head page. This is for comparison of drivers
    of the same constructors/team.
"""

import streamlit as st
import plotly.express as px
from utils.streamlit_bigquery import run_query
from utils.config import GCP_PROJECT_ID
from utils.driver_images import get_driver_photo

st.set_page_config(page_title="Head to Head", page_icon="⚔️", layout="wide")
st.title("⚔️ Head to Head — Teammate Comparison")
st.caption("Note: Current Data only has the 2020-2024 Formula 1 season")


all_drivers_query = f"""
    SELECT DISTINCT
        CONCAT(d.first_name, ' ', d.last_name) AS driver_name,
        h.driver_id
    FROM `{GCP_PROJECT_ID}.f1_dbt.int_head_to_head` h
    JOIN `{GCP_PROJECT_ID}.f1_dbt.dim_drivers` d
        ON h.driver_id = d.driver_id
    ORDER BY driver_name
"""

all_drivers_df = run_query(all_drivers_query)
selected_driver = st.selectbox("Select Driver", options=all_drivers_df['driver_name'])

selected_driver_id = all_drivers_df[
    all_drivers_df['driver_name'] == selected_driver
]['driver_id'].values[0]



teammates_query = f"""
    SELECT DISTINCT
        CONCAT(d.first_name, ' ', d.last_name) AS teammate_name,
        h.teammate_id
    FROM `{GCP_PROJECT_ID}.f1_dbt.int_head_to_head` h
    JOIN `{GCP_PROJECT_ID}.f1_dbt.dim_drivers` d
        ON h.teammate_id = d.driver_id
    WHERE h.driver_id = '{selected_driver_id}'
    ORDER BY teammate_name
"""

teammates_df = run_query(teammates_query)
selected_teammate = st.selectbox("Select Teammate", options=teammates_df['teammate_name'])


selected_teammate_id = teammates_df[
    teammates_df['teammate_name'] == selected_teammate
]['teammate_id'].values[0]

st.divider()

col_driver1, col_vs, col_driver2 = st.columns([2, 1, 2])

with col_driver1:
    photo1 = get_driver_photo(selected_driver)
    if photo1:
        st.image(photo1, width=200)
    st.subheader(selected_driver)

with col_vs:
    st.markdown("<h1 style='text-align: center; margin-top: 50px;'>VS</h1>", 
                unsafe_allow_html=True)

with col_driver2:
    photo2 = get_driver_photo(selected_teammate)
    if photo2:
        st.image(photo2, width=200)
    st.subheader(selected_teammate)


h2h_query = f"""
    SELECT
        season,
        round_num,
        race_type,
        finish_position,
        teammate_finish,
        beat_teammate
    FROM `{GCP_PROJECT_ID}.f1_dbt.int_head_to_head`
    WHERE driver_id = '{selected_driver_id}'
    AND teammate_id = '{selected_teammate_id}'
    AND race_type = 'race'
    ORDER BY season, round_num
"""

h2h_df = run_query(h2h_query)

if h2h_df.empty:
    st.warning("No head to head data found for this combination.")
    st.stop()



total_races = len(h2h_df)
beats = h2h_df['beat_teammate'].sum()
win_rate = round((beats / total_races) * 100, 1)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🏁 Races Together", total_races)
with col2:
    st.metric(f"✅ {selected_driver} Beat Teammate", int(beats))
with col3:
    st.metric("📊 Head to Head Win Rate", f"{win_rate}%")

st.divider()



st.subheader("🏁 Finish Position Comparison")

import pandas as pd
chart_df = pd.melt(
    h2h_df,
    id_vars=['season', 'round_num'],
    value_vars=['finish_position', 'teammate_finish'],
    var_name='driver',
    value_name='position'
)
chart_df['driver'] = chart_df['driver'].map({
    'finish_position': selected_driver,
    'teammate_finish': selected_teammate
})

fig = px.line(
    chart_df,
    x='round_num',
    y='position',
    color='driver',
    facet_col='season',
    title=f"{selected_driver} vs {selected_teammate}",
    labels={'round_num': 'Round', 'position': 'Finish Position'}
)
fig.update_yaxes(autorange="reversed")
st.plotly_chart(fig, use_container_width=True)
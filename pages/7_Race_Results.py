"""
===========================================================
F1 Race Intelligence - Page 7 Race Results
===========================================================
Script purpose:
    Shows full race classification for any historical race.
"""

import streamlit as st
import plotly.express as px
from utils.streamlit_bigquery import run_query
from utils.config import GCP_PROJECT_ID

st.set_page_config(page_title="Race Results", page_icon="🏆", layout="wide")
st.title("🏆 Race Results")
st.caption("💡 Gap times coming soon — finish positions and points shown above")

season_query = f"""
    SELECT DISTINCT season
    FROM `{GCP_PROJECT_ID}.f1_dbt.mart_driver_performance`
    ORDER BY season DESC
"""
season_df = run_query(season_query)
selected_season = st.selectbox("Select Season", options=season_df['season'])



round_query = f"""
    SELECT DISTINCT round_num, race_name
    FROM `{GCP_PROJECT_ID}.f1_dbt.mart_driver_performance`
    WHERE season = {selected_season}
    ORDER BY round_num
"""
round_df = run_query(round_query)
selected_race = st.selectbox(
    "Select Race",
    options=round_df['race_name'],
)
selected_round = round_df[round_df['race_name'] == selected_race]['round_num'].values[0]

st.divider()
st.subheader(f"🏁 {selected_race} {selected_season} — Race Classification")



results_query = f"""
    SELECT DISTINCT
        mp.finish_position,
        mp.driver_name,
        mp.driver_code,
        dc.constructor_name,
        mp.grid_position,
        mp.positions_gained,
        mp.points,
        mp.status
    FROM `{GCP_PROJECT_ID}.f1_dbt.mart_driver_performance` mp
    LEFT JOIN `{GCP_PROJECT_ID}.f1_dbt.dim_constructors` dc
        ON mp.constructor_id = dc.constructor_id
    WHERE mp.season = {selected_season}
        AND mp.round_num = {selected_round}
    ORDER BY mp.finish_position
"""

results_df = run_query(results_query)



st.dataframe(
    results_df[[
        'finish_position', 'driver_name', 'driver_code',
        'constructor_name', 'grid_position', 'positions_gained',
        'points', 'status'
    ]],
    hide_index=True,
    width='stretch'
)

st.divider()



st.subheader("📈 Positions Gained/Lost")
fig = px.bar(
    results_df.sort_values('finish_position'),
    x='driver_code',
    y='positions_gained',
    color='positions_gained',
    color_continuous_scale='RdYlGn',
    title=f"Positions Gained/Lost — {selected_race} {selected_season}",
    labels={'driver_code': 'Driver', 'positions_gained': 'Positions Gained'}
)
fig.add_hline(y=0, line_dash="dash", line_color="white", opacity=0.5)
st.plotly_chart(fig, width='stretch')
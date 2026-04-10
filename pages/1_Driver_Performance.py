"""
===========================================================
F1 Race Intelligence - Page 1 Driver Performance
===========================================================
Script purpose:
    Create driver performance page. This shows the stats and data
    of individual drivers.
"""

import streamlit as st
import plotly.express as px
from utils.streamlit_bigquery import run_query
from utils.config import GCP_PROJECT_ID
from utils.driver_images import get_driver_photo


st.set_page_config(page_title="Driver Performance", page_icon="🏎️", layout="wide")

st.title("👤 Driver Performance")
st.caption("Note: Current Data only has the 2020-2024 Formula 1 season")


drivers_query = f"""
    SELECT DISTINCT driver_name, driver_code
    FROM `{GCP_PROJECT_ID}.f1_dbt.mart_driver_performance`
    ORDER BY driver_name
"""
drivers_df = run_query(drivers_query)


selected_driver = st.selectbox("Select Driver", options=drivers_df['driver_name'])
photo_url = get_driver_photo(selected_driver)


driver_query = f"""
    SELECT DISTINCT
        driver_name, driver_code, finish_position,
        season, round_num, nationality,
        grid_position, positions_gained, race_name
    FROM `{GCP_PROJECT_ID}.f1_dbt.mart_driver_performance`
    WHERE driver_name = '{selected_driver}'
    ORDER BY season, round_num
"""
driver_df = run_query(driver_query)

col_photo, col_info = st.columns([1, 3])

with col_photo:
    if photo_url:
        st.image(photo_url, width=200)

with col_info:
    st.subheader(selected_driver)
    # get nationality and driver code from driver_df
    nationality = driver_df['nationality'].iloc[0]
    driver_code = driver_df['driver_code'].iloc[0]
    st.markdown(f"**Code:** {driver_code}")
    st.markdown(f"**Nationality:** {nationality}")

points_query = f"""
    SELECT SUM(season_max) as career_points
    FROM (
        SELECT season, MAX(cumulative_drivers_points) as season_max
        FROM `{GCP_PROJECT_ID}.f1_dbt.mart_championship_standings`
        WHERE driver_name = '{selected_driver}'
        GROUP BY season
    )
"""
points_df = run_query(points_query)




st.divider()
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🏁 Total Races", len(driver_df))
with col2:
    st.metric("🏆 Total Points", int(points_df['career_points'][0]))
with col3:
    st.metric("📍 Avg Finish", round(driver_df['finish_position'].mean(), 1))
with col4:
    st.metric("⭐ Best Finish", int(driver_df['finish_position'].min()))



st.divider()
st.subheader("🏁 Finish Position by Race")

fig1 = px.line(
    driver_df,
    x='round_num',
    y='finish_position',
    color='season',
    title=f"{selected_driver} — Finish Position per Race",
    labels={'round_num': 'Round', 'finish_position': 'Finish Position'}
)
fig1.update_yaxes(autorange="reversed")
st.plotly_chart(fig1, use_container_width=True)



st.subheader("📈 Positions Gained/Lost")

fig2 = px.bar(
    driver_df,
    x='round_num',
    y='positions_gained',
    color='season',
    title=f"{selected_driver} — Positions Gained/Lost per Race",
    labels={'round_num': 'Round', 'positions_gained': 'Positions Gained'},
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig2.add_hline(y=0, line_dash="dash", line_color="white", opacity=0.5)
st.plotly_chart(fig2, use_container_width=True)



st.subheader("🏆 Best Circuits")

best_circuits = driver_df.groupby('race_name').agg(
    avg_finish=('finish_position', 'mean'),
    avg_positions_gained=('positions_gained', 'mean'),
    races=('round_num', 'count')
).round(2).sort_values('avg_finish').reset_index()

st.dataframe(best_circuits, hide_index=True, use_container_width=True)
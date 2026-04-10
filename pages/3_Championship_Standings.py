"""
===========================================================
F1 Race Intelligence - Page 3 Championship Standings
===========================================================
Script purpose:
    Create championship standings page. Showcase the championship
    standings of both drivers and constructors world championships
    for each season.
"""

import streamlit as st
import plotly.express as px
from utils.streamlit_bigquery import run_query
from utils.config import GCP_PROJECT_ID
from utils.config import CONSTRUCTOR_COLORS

st.set_page_config(page_title="Championship Standings", page_icon="🏆", layout="wide")
st.title("🏆 Championship Standings")
st.caption("Note: Current Data only has the 2020-2024 Formula 1 season")


season_query = f"""
    SELECT
        DISTINCT
            season
    FROM `{GCP_PROJECT_ID}.f1_dbt.mart_championship_standings`
    ORDER BY season DESC
"""

season_df = run_query(season_query)
selected_season = st.selectbox("Select Season", options=season_df['season'])

st.divider()


#FOR Drivers Championship
st.subheader("🏆 Drivers Championship Progression")
drivers_championship_query = f"""
    SELECT
        round_num,
        driver_name,
        driver_code,
        constructor_name,
        cumulative_drivers_points
    FROM `{GCP_PROJECT_ID}.f1_dbt.mart_championship_standings`
    WHERE season = {selected_season}
    ORDER BY round_num
"""
drivers_df = run_query(drivers_championship_query)

fig1 = px.line(
    drivers_df,
    x='round_num',
    y='cumulative_drivers_points',
    color='driver_code',
    line_dash='driver_code',
    custom_data=['driver_name', 'constructor_name'],
    color_discrete_map={
        row['driver_code']: CONSTRUCTOR_COLORS.get(row['constructor_name'], '#FFFFFF')
        for _, row in drivers_df.drop_duplicates('driver_code').iterrows()
    },
    title=f"{selected_season} Drivers Championship",
)
st.plotly_chart(fig1, width='stretch')


#FOR Constructors Championship
st.subheader("🏆 Constructors Championship Progression")
constructors_championship_query = f"""
    SELECT
        round_num,
        constructor_name,
        cumulative_constructors_points
    FROM `{GCP_PROJECT_ID}.f1_dbt.mart_championship_standings`
    WHERE season = {selected_season}
    ORDER BY round_num
"""
constructors_df = run_query(constructors_championship_query)

fig2 = px.line(
    constructors_df,
    x='round_num',
    y='cumulative_constructors_points',
    color='constructor_name',
    color_discrete_map=CONSTRUCTOR_COLORS,
    title=f"{selected_season} Constructors Championship",
    labels={'round_num': 'Round', 'cumulative_constructors_points': 'Points'}
)
st.plotly_chart(fig2, width='stretch')


st.subheader("📋 Final Drivers Championship Tally")
drivers_champion_query = f"""
    SELECT
        driver_name,
        driver_code,
        MAX(cumulative_drivers_points) AS total_points
    FROM `{GCP_PROJECT_ID}.f1_dbt.mart_championship_standings`
    WHERE season = {selected_season}
    GROUP BY driver_name, driver_code
    ORDER BY total_points DESC
"""

driver_champion_df = run_query(drivers_champion_query)

st.markdown(f"**{selected_season} Season**")
driver_champion_df['rank'] = range(1, len(driver_champion_df) + 1)
st.dataframe(
    driver_champion_df[['rank', 'driver_name', 'driver_code', 'total_points']],
    hide_index=True,
    width='stretch'
)

st.divider()

st.subheader("📋 Final Constructors Championship Tally")
constructors_champion_query = f"""
    SELECT
        constructor_name,
        MAX(cumulative_constructors_points) AS total_points
    FROM `{GCP_PROJECT_ID}.f1_dbt.mart_championship_standings`
    WHERE season = {selected_season}
    GROUP BY constructor_name
    ORDER BY total_points DESC
"""

constructors_champion_df = run_query(constructors_champion_query)

st.markdown(f"**{selected_season} Season**")
constructors_champion_df['rank'] = range(1, len(constructors_champion_df) + 1)
st.dataframe(
    constructors_champion_df[['rank', 'constructor_name', 'total_points']],
    hide_index=True,
    width='stretch'
)

st.divider()

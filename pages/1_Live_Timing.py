"""
===========================================================
F1 Race Intelligence - Page 1 Live Timing
===========================================================
Script purpose:
    Shows live race timing and standings during active race
    weekends. Falls back to most recent completed race when
    no active session.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timezone
from utils.openf1_client import get_latest_session, get_live_timing, get_driver_info, is_session_live, get_intervals
import time


st.set_page_config(page_title="Live Timing", page_icon="🔴", layout="wide")
st.title("🔴 Live Timing")

session = get_latest_session()

if not session:
    st.error("No session data available.")
    st.stop()

session_key = session['session_key']
is_live = is_session_live(session)

if is_live:
    st.success(f"🔴 LIVE — {session['country_name']} Grand Prix")
else:
    st.info(f"📅 Most Recent Race: {session['country_name']} Grand Prix {session['year']}")

st.caption(f"Circuit: {session['circuit_short_name']} | Session: {session['session_name']}")
st.caption("⚠️ DNF/retired drivers may show incorrect positions based on last recorded data")
st.divider()

with st.spinner("Loading data..."):
    drivers_raw = get_driver_info(session_key)
    time.sleep(1)
    laps_raw = get_live_timing(session_key)
    time.sleep(1)
    intervals_raw = get_intervals(session_key)
    time.sleep(1)

if not drivers_raw or not laps_raw or not intervals_raw:
    st.error("No data available for this session.")
    st.stop()

drivers = {d['driver_number']: d for d in drivers_raw}

laps_df = pd.DataFrame(laps_raw)
intervals_df = pd.DataFrame(intervals_raw)

latest_intervals = (
    intervals_df
    .sort_values('date')
    .groupby('driver_number')
    .last()
    .reset_index()
)

latest_laps = (
    laps_df
    .groupby('driver_number')
    .agg(
        current_lap=('lap_number', 'max'),
        best_lap=('lap_duration', 'min'),
        last_lap=('lap_duration', 'last')
    )
    .reset_index()
)

standings = latest_intervals.merge(latest_laps, on='driver_number', how='left')

standings['gap_to_leader'] = pd.to_numeric(standings['gap_to_leader'], errors='coerce')
standings = standings.sort_values(
    ['current_lap', 'gap_to_leader'],
    ascending=[False, True]
).reset_index(drop=True)
standings['position'] = range(1, len(standings) + 1)

standings['gap'] = standings['gap_to_leader'].apply(
    lambda x: "LEADER" if x == 0 else (f"+{x:.3f}s" if pd.notna(x) else "+1 LAP")
)
standings['driver'] = standings['driver_number'].apply(
    lambda x: drivers.get(x, {}).get('name_acronym', str(x))
)
standings['team'] = standings['driver_number'].apply(
    lambda x: drivers.get(x, {}).get('team_name', 'Unknown')
)

standings['best_lap'] = standings['best_lap'].round(3)
standings['last_lap'] = standings['last_lap'].round(3)

st.subheader("🏁 Race Standings")

st.dataframe(
    standings[['position', 'driver', 'team', 'current_lap',
               'last_lap', 'best_lap', 'gap']],
    hide_index=True,
    width='stretch'
)

st.divider()


st.subheader("⏱️ Sector Times — Latest Lap")

latest_lap_per_driver = (
    laps_df
    .sort_values('lap_number')
    .groupby('driver_number')
    .last()
    .reset_index()
)

latest_lap_per_driver['driver'] = latest_lap_per_driver['driver_number'].apply(
    lambda x: drivers.get(x, {}).get('name_acronym', str(x))
)

sector_df = latest_lap_per_driver[[
    'driver', 'lap_number',
    'duration_sector_1', 'duration_sector_2', 'duration_sector_3',
    'lap_duration'
]].sort_values('lap_duration')

st.dataframe(sector_df, hide_index=True, width='stretch')

if is_live:
    st.caption("⟳ Auto-refreshing every 30 seconds")
    time.sleep(30)
    st.rerun()
else:
    st.caption("Data from most recent available race session")
"""
===========================================================
F1 Race Intelligence - Page 2 Team Radio
===========================================================
Script purpose:
    Script that fetches team radio of formula 1 drivers and
    teams. This Lets user listen to team radio during race
    weekends
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timezone
from utils.openf1_client import get_latest_session, get_driver_info, is_session_live, get_team_radio, get_sessions_by_year
import time


st.set_page_config(page_title="Team Radio", page_icon="📻", layout="wide")
st.title("📻 Team Radio")

st.subheader("Select Session")

current_year = datetime.now().year
years = list(range(2024, current_year + 1))

col1, col2, col3 = st.columns(3)

with col1:
    selected_year = st.selectbox("Year", years, index=len(years)-1)

sessions = get_sessions_by_year(selected_year)

if not sessions:
    st.error("No sessions found for this year.")
    st.stop()

meetings = {}
for s in sessions:
    meetings[s['meeting_key']] = s['country_name']

meeting_options = list(meetings.items())

with col2:
    selected_meeting_key = st.selectbox(
        "Race / Grand Prix",
        options=meeting_options,
        format_func=lambda x: x[1]
    )[0]

filtered_sessions = [s for s in sessions if s['meeting_key'] == selected_meeting_key]

session_types = sorted(set(s['session_name'] for s in filtered_sessions))

default_idx = session_types.index("Race") if "Race" in session_types else 0

with col3:
    selected_session_type = st.selectbox(
        "Session Type",
        session_types,
        index=default_idx
    )

session = next(
    (s for s in filtered_sessions if s['session_name'] == selected_session_type),
    None
)

if not session:
    st.error("Session not found.")
    st.stop()



session_key = session['session_key']
is_live = is_session_live(session)

if is_live:
    st.success(f"🔴 LIVE — {session['meeting_name']} ({selected_session_type})")
else:
    st.info(f"📻 {session['country_name']} Grand Prix {selected_year} — {selected_session_type}")

st.caption(
    f"Circuit: {session['circuit_short_name']} | Session: {session['session_name']}"
)

st.divider()



with st.spinner("Loading team radio..."):
    drivers_raw = get_driver_info(session_key)
    time.sleep(1)
    radio_raw = get_team_radio(session_key)

if not drivers_raw or not radio_raw:
    st.warning("No team radio available for this session on the free tier.")
    st.info("Team radio is typically available for sessions from 2024 onward.")
    st.stop()

drivers = {d['driver_number']: d for d in drivers_raw}



driver_options = ["All Drivers"] + [
    f"{d['name_acronym']} - {d['full_name']}"
    for d in drivers_raw
]

selected = st.selectbox("Filter by Driver", options=driver_options)



for msg in radio_raw:
    driver_info = drivers.get(msg['driver_number'], {})
    driver_name = driver_info.get('full_name', f"Driver {msg['driver_number']}")

    if selected != "All Drivers":
        selected_name = selected.split(" - ")[1]
        if driver_name != selected_name:
            continue

    ts = msg.get("date")
    if ts:
        ts = datetime.fromisoformat(ts.replace("Z", "+00:00")).strftime("%H:%M:%S")
    else:
        ts = "Unknown time"

    st.markdown(f"**{ts} — {driver_name}**")

    if msg.get("recording_url"):
        st.audio(msg["recording_url"])

    st.divider()
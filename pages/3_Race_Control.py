"""
===========================================================
F1 Race Intelligence - Page 3 Race Control
===========================================================
Script purpose:
    Script that fetches race control infos like flags, 
    safety cars, penalties, and other race control messages. 

Things to edit:
    - might need to add some sort of filter to not let other data be buried down
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timezone
from utils.openf1_client import get_live_race_control, get_driver_info, get_sessions_by_year
from utils.config import get_flag_display
import time


st.set_page_config(page_title="Race Control", page_icon="🚨", layout="wide")
st.title("🚨 Race Control")

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

st.info(f"🚨 {session['country_name']} {selected_year} — {selected_session_type}")
st.caption(
    f"Circuit: {session['circuit_short_name']} | Session: {session['session_name']}"
)

st.divider()



with st.spinner("Loading race control messages..."):
    drivers_raw = get_driver_info(session_key)
    time.sleep(0.5)
    race_control = get_live_race_control(session_key)

if not race_control:
    st.warning("No race control messages available for this session.")
    st.stop()

drivers = {d['driver_number']: d for d in drivers_raw} if drivers_raw else {}


for msg in race_control:
    flag = msg.get("flag")
    message = msg.get("message", "No message")
    driver_number = msg.get("driver_number")

    driver_name = ""
    if driver_number and driver_number in drivers:
        driver_name = drivers[driver_number]['full_name']

    icon, color = get_flag_display(flag)

    ts = msg.get("date")
    if ts:
        ts = datetime.fromisoformat(ts.replace("Z", "+00:00")).strftime("%H:%M:%S")
    else:
        ts = "Unknown time"

    title = f"{icon} {ts}"
    if driver_name:
        title += f" — {driver_name}"

    st.markdown(f"**{title}**")
    st.markdown(f"<span style='color:{color}'>{message}</span>", unsafe_allow_html=True)

    st.divider()
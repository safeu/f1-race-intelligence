"""
===========================================================
Loading secret variables
===========================================================
Script purpose:
    Script to fetch/load .env variables 
"""

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")


KEY_PATH = os.getenv("KEY_PATH")

try:
    import streamlit as st
    GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID") or st.secrets.get("GCP_PROJECT_ID")
    BQ_DATASET = os.getenv("BQ_DATASET") or st.secrets.get("BQ_DATASET")
except Exception:
    GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
    BQ_DATASET = os.getenv("BQ_DATASET")



#other variable settings
base_url = "https://api.jolpi.ca/ergast/f1"
openf1_base_url = "https://api.openf1.org/v1"


#colors
CONSTRUCTOR_COLORS = {
    'Red Bull': '#3671C6',
    'Ferrari': '#E8002D',
    'Mercedes': '#27F4D2',
    'McLaren': '#FF8000',
    'Aston Martin': '#229971',
    'Alpine F1 Team': '#FF87BC',
    'Williams': '#64C4FF',
    'RB F1 Team': '#6692FF',
    'Haas F1 Team': '#B6BABD',
    'Sauber': '#52E252',
    'Alfa Romeo': '#C92D4B',
    'AlphaTauri': '#5E8FAA',
    'Renault': '#FFF500',
    'Racing Point': '#F596C8',
    'Force India': '#F596C8',
    'Toro Rosso': '#469BFF',
}
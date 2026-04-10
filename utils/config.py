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
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
BQ_DATASET = os.getenv("BQ_DATASET")

if not KEY_PATH:
    raise ValueError("KEY_PATH is not set in .env")
if not GCP_PROJECT_ID:
    raise ValueError("GCP_PROJECT_ID is not set in .env")
if not BQ_DATASET:
    raise ValueError("BQ_DATASET is not set in .env")


#other variable settings
base_url = "https://api.jolpi.ca/ergast/f1"


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
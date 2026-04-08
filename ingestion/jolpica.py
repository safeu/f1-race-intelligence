"""
===========================================================
Ingest data from jolpica API
===========================================================
Script purpose:
    Script to ingest data from the jolpica API. Which contains current and most
    importantly historical Formula 1 data.
"""
import requests
import logging
from utils.config import base_url
import time

logger = logging.getLogger(__name__)


def fetch_all_pages(url, extract_key):
    all_records = []
    offset = 0

    while True:
        response = requests.get(url, params={"limit": 100, "offset": offset})

        if response.status_code == 429:
            logger.warning("Rate limited, waiting 10 seconds...")
            time.sleep(10)
            continue

        response.raise_for_status()

        total = int(response.json()["MRData"]["total"])
        data = response.json()["MRData"]["RaceTable"][extract_key]

        all_records.extend(data)
        offset += 100
        if offset >= total:
            break
    
    logger.info(f"Total records fetched: {total}")
    return all_records

def get_races(season):
    try:
        url = f"{base_url}/{season}/results.json"
        return fetch_all_pages(url, "Races")
    except Exception as e:
        logger.error(f"Error fetching races: {e}")
        return []

def get_lap_times(season, round_num):
    try:
        all_laps = []
        url = f"{base_url}/{season}/{round_num}/laps.json"
        races = fetch_all_pages(url, "Races")
        for race in races:
            all_laps.extend(race["Laps"])
        return all_laps
    except Exception as e:
        logger.error(f"Error fetching lap times: {e}")
        return []

def get_pit_stops(season, round_num):
    try:
        all_pits = []
        url = f"{base_url}/{season}/{round_num}/pitstops.json"
        races = fetch_all_pages(url, "Races")
        for pit in races:
            all_pits.extend(pit["PitStops"])
        return all_pits
    except Exception as e:
        logger.error(f"Error fetching pit stop records: {e}")
        return []


#i forgor sprint races
def get_sprint_results(season):
    try:
        url = f"{base_url}/{season}/sprint.json"
        return fetch_all_pages(url, "Races")
    except Exception as e:
        logger.error(f"Error fetching sprint results: {e}")
        return []

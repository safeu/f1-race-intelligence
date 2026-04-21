"""
===========================================================
SCRIPT: openf1_client
===========================================================
Script purpose:
    Script that fetches live formula 1 data from OpenF1's live
    telemetry. The script requests data from OpenF1 then returns
    clean data.

Functions present:
    fetch_openf1()
        - to fetch openf1 pages similar to fetch_pages in jolpica.py script
    get_latest_session() 
        - gets the most recent/current race session key
    get_live_timing() 
        - gets current lap times for all drivers
    get_live_race_control() 
        - gets flags and safety car info
    get_driver_info() 
        - gets driver numbers and names for that session
"""

import requests
import logging
from utils.config import openf1_base_url

logger = logging.getLogger(__name__)

def fetch_openf1(endpoint, params):
    try:
        url = f"{openf1_base_url}/{endpoint}"
        response = requests.get(url, params=params)

        response.raise_for_status()
        data = response.json()

        logger.info(f"Fetched {len(data)} records from {endpoint}")
        return data
    
    except Exception as e:
        logger.error(f"Failed to fetch openf1 data: {e}")
        raise


def get_latest_session():
    try:
        sessions = fetch_openf1('sessions', {'session_type': 'Race'})
        
        if not sessions:
            return None
        
        latest = sorted(sessions, key=lambda x: x['date_start'], reverse=True)[0]
    
        logger.info(f"Latest session: {latest['session_name']} - {latest['country_name']} {latest['year']}")
        return latest
    
    except Exception as e:
        logger.error(f"Failed to get latest session: {e}")
        raise


def get_live_timing(session_key):
    try:
        timings = fetch_openf1('laps', {'session_key': session_key})

        if not timings:
            return None
        
        logger.info(f"Fetched {len(timings)} lap records for session {session_key}")
        return timings
    except Exception as e:
        logger.error(f"Error getting live timing (laps): {e}")
        raise

def get_live_race_control(session_key):
    try:
        race_controls = fetch_openf1('race_control', {'session_key': session_key})

        if not race_controls:
            return None
        
        logger.info(f"Fetched {len(race_controls)} race control records for session {session_key}")
        return race_controls
    except Exception as e:
        logger.error(f"Error getting live race control data: {e}")
        raise

def get_driver_info(session_key):
    try:
        drivers = fetch_openf1('drivers', {'session_key': session_key})

        if not drivers:
            return None
        
        logger.info(f"Fetched {len(drivers)} driver infos for session {session_key}")
        return drivers
    except Exception as e:
        logger.error(f"Error getting driver info: {e}")
        raise


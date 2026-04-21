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
    is_session_live()
        - checks if there is a session live
    get_intervals()
        - checks gap to leader and intervals during live sessions for standings
    get_team_radio()
        - get team radio during race weekends
    get_sessions_by_year()
        - get f1 sessions by year (useful for team radio)
"""

import requests
import logging
from utils.config import openf1_base_url
from datetime import datetime, timezone
import time

logger = logging.getLogger(__name__)

def fetch_openf1(endpoint, params):
    url = f"{openf1_base_url}/{endpoint}"
    
    for attempt in range(3):
        try:
            response = requests.get(url, params=params)
            
            if response.status_code == 429:
                logger.warning(f"Rate limited on {endpoint}, waiting 10 seconds...")
                time.sleep(10)
                continue
                
            response.raise_for_status()
            data = response.json()
            logger.info(f"Fetched {len(data)} records from {endpoint}")
            return data
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise
            if attempt == 2:
                raise
            time.sleep(5)
            
        except Exception as e:
            logger.error(f"Failed to fetch openf1 data: {e}")
            raise

def get_latest_session():
    try:
        sessions = fetch_openf1('sessions', {'session_type': 'Race'})
        
        if not sessions:
            return None
        
        sorted_sessions = sorted(sessions, key=lambda x: x['date_start'], reverse=True)
        
        for session in sorted_sessions:
            try:
                test = fetch_openf1('laps', {
                    'session_key': session['session_key'], 
                    'lap_number': 1
                })
                if test:
                    logger.info(f"Latest available session: {session['country_name']} {session['year']}")
                    return session
            except Exception:
                continue
        return None
        
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

def is_session_live(session):
    now = datetime.now(timezone.utc)
    date_start = datetime.fromisoformat(session['date_start'])
    date_end = datetime.fromisoformat(session['date_end'])
    return date_start <= now <= date_end


def get_intervals(session_key):
    try:
        intervals = fetch_openf1('intervals', {'session_key': session_key})
        
        if not intervals:
            return None
        
        logger.info(f"Fetched {len(intervals)} interval records for session {session_key}")
        return intervals
    except Exception as e:
        logger.error(f"Error getting intervals: {e}")
        raise


def get_team_radio(session_key):
    try:
        radio = fetch_openf1('team_radio', {'session_key': session_key})
        if not radio:
            return None
        logger.info(f"Fetched {len(radio)} team radio records for session {session_key}")
        return radio
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return None
        raise
    except Exception as e:
        logger.error(f"Error getting team radio: {e}")
        raise

def get_sessions_by_year(year, session_type=None):
    try:
        params = {'year': year}
        if session_type:
            params['session_type'] = session_type
        sessions = fetch_openf1('sessions', params)
        if not sessions:
            return None
        
        sessions = [
            s for s in sessions 
            if s.get('session_type') not in ['Testing']
        ]
        
        return sessions
    except Exception as e:
        logger.error(f"Error getting sessions: {e}")
        raise
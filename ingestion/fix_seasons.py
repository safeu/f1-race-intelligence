"""
===========================================================
Fix seasons
===========================================================
Script purpose:
    Script to fix races in certain seasons that had issues with API.
    Used a separate script to avoid the WRITE_TRUNCATE in run_
    ingestion.py, and to avoid messing with clean data (e.g.
    lap times, sprint races, and pitstops)
"""

import logging
from ingestion.jolpica import get_races
from utils.transforms import flatten_races
from utils.bigquery_client import get_bigquery_client, load_to_bigquery
from utils.config import GCP_PROJECT_ID, BQ_DATASET
import time
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SEASONS_TO_FIX = [2013, 2014, 2015, 2016, 2024, 2025]

def fix_races():
    client = get_bigquery_client()
    
    for season in SEASONS_TO_FIX:
        logger.info(f"Fixing season {season}...")
        
        delete_query = f"""
            DELETE FROM `{GCP_PROJECT_ID}.{BQ_DATASET}.raw_races`
            WHERE season = {season}
        """
        client.query(delete_query).result()
        logger.info(f"Deleted season {season} from raw_races")
        
        max_attempts = 3
        for attempt in range(max_attempts):
            races = get_races(season)
            
            incomplete = [r for r in races if len(r.get("Results", [])) < 15]
            
            if not incomplete:
                logger.info(f"Season {season} - all rounds complete")
                break
            
            logger.warning(f"Season {season} - {len(incomplete)} incomplete rounds, retrying... (attempt {attempt + 1})")
            time.sleep(5)
        
        flat_races = flatten_races(races)
        load_to_bigquery(flat_races, "raw_races", write_mode="WRITE_APPEND")
        logger.info(f"Reloaded {len(flat_races)} races for season {season}")
        time.sleep(3)

if __name__ == "__main__":
    fix_races()
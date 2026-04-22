"""
===========================================================
Run ingestion pipeline
===========================================================
Script purpose:
    Main entry point for loading historical F1 data from
    Jolpica API into BigQuery raw tables.

Warning:
    If this script is ran and you already have data in BigQuery, it would replace
    all of the data in there due to WRITE_TRUNCATE.
"""
import logging
from ingestion.jolpica import get_races, get_lap_times, get_pit_stops, get_sprint_results
from utils.transforms import flatten_races, flatten_lap_times, flatten_pit_stops, flatten_sprint_results
from utils.bigquery_client import load_to_bigquery
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SEASONS = list(range(2010, 2026))


def main():
    try:
        load_to_bigquery([], "raw_races", write_mode="WRITE_TRUNCATE")
        load_to_bigquery([], "raw_lap_times", write_mode="WRITE_TRUNCATE")
        load_to_bigquery([], "raw_pit_stops", write_mode="WRITE_TRUNCATE")
        load_to_bigquery([], "raw_sprint_races", write_mode="WRITE_TRUNCATE")

        for season in SEASONS:
            logger.info(f"Processing season {season}...")

            #basically get all races for that season
            races = get_races(season)
            flat_races = flatten_races(races)
            load_to_bigquery(flat_races, "raw_races", write_mode="WRITE_APPEND")

            #then sprints (i forgor)
            sprint_races = get_sprint_results(season)
            flat_sprints = flatten_sprint_results(sprint_races)
            load_to_bigquery(flat_sprints, "raw_sprint_races", write_mode="WRITE_APPEND")

            seen = set()
            unique_races = []
            for race in races:
                key = race.get("round")
                if key not in seen:
                    seen.add(key)
                    unique_races.append(race)

            for race in unique_races:
                try:
                    #get the laptimes and pit stops for each round
                    round_num = race.get("round")
                    logger.info(f"Processing season {season}, round {round_num}")

                    lap_times = get_lap_times(season, round_num)
                    flat_lap_times = flatten_lap_times(season, round_num, lap_times)
                    load_to_bigquery(flat_lap_times, "raw_lap_times", write_mode="WRITE_APPEND")

                    pit_stops = get_pit_stops(season, round_num)
                    flat_pit_stops = flatten_pit_stops(season, round_num, pit_stops)
                    load_to_bigquery(flat_pit_stops, "raw_pit_stops", write_mode="WRITE_APPEND")
                
                    time.sleep(0.5)
                except Exception as e:
                    logger.error(f"Error fetching/loading data: {e}")
                    continue
                
            time.sleep(1)        
        logger.info("Data loaded successfully")

    except Exception as e:
        logger.error(f"Error fetching data and loading to BigQuery: {e}")
        raise


if __name__ == "__main__":
    main()
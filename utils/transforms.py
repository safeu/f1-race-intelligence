"""
===========================================================
Data transformation utilities
===========================================================
Script purpose:
    Script to transform data from raw API response to flat schema. gets raw API
    response from jolpica.py then transforms it here, before loading it into
    BigQuery.
"""
import logging
from datetime import datetime, timezone
import json

logger = logging.getLogger(__name__)

def flatten_lap_times(season, round_num, laps):
    results = []

    for lap in laps:
        lap_number = lap.get("number", 0)

        for timing in lap.get("Timings", []):
            row = {
                "season": season,
                "round_num": round_num,
                "lap_number": lap_number,
                "driver_id": timing.get("driverId"),
                "lap_time": timing.get("time"),
                "position": timing.get("position", 0),
                "ingested_at": datetime.now(timezone.utc).isoformat()
            }

            results.append(row)
    return results

def flatten_pit_stops(season, round_num, pit_stops):
    results = []
    for pit in pit_stops:
        row = {
                "season": season,
                "round_num": round_num,
                "lap": pit.get("lap"),
                "stop": pit.get("stop"),
                "driver_id": pit.get("driverId"),
                "time": pit.get("time"),
                "duration": pit.get("duration"),
                "ingested_at": datetime.now(timezone.utc).isoformat()
            }
        results.append(row)
    return results

def flatten_races(races):
    results = []
    for race in races:
        row = {
            "season": race.get("season"),
            "round": race.get("round"),
            "race_name": race.get("raceName"),
            "circuit_id": race.get("Circuit", {}).get("circuitId"),
            "date": race.get("date"),
            "results": json.dumps(race.get("Results", [])),
            "ingested_at": datetime.now(timezone.utc).isoformat()
            }

        results.append(row)
    return results
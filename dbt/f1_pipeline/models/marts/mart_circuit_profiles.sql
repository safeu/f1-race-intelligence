/*
=============================================================
Model: mart_circuit_profiles
=============================================================
Description:
    Aggregated circuit characteristics across seasons.
    Useful for comparing circuit difficulty, pit stop strategy,
    and overtaking opportunities.

Depends on:
    - stg_races
    - int_driver_consistency
    - int_pit_strategy
    - int_start_vs_finish
=============================================================
*/

WITH races AS (
    SELECT DISTINCT
        season,
        round_num,
        circuit_id,
        race_name
    FROM {{ ref('stg_races') }}
),

consistency AS (
    SELECT * FROM {{ ref('int_driver_consistency') }}
),

pit_strategy AS (
    SELECT * FROM {{ ref('int_pit_strategy') }}
),

start_vs_finish AS (
    SELECT * FROM {{ ref('int_start_vs_finish') }}
),

circuit_stats AS (
    SELECT
        r.circuit_id,
        r.race_name,
        COUNT(DISTINCT r.season) AS seasons_held,
        ROUND(AVG(c.avg_lap_time_sec), 3) AS avg_lap_time_sec,
        ROUND(AVG(c.stddev_lap_time_sec), 4) AS avg_lap_time_stddev,
        ROUND(AVG(p.num_stops), 2) AS avg_pit_stops,
        ROUND(AVG(p.avg_pit_duration), 3) AS avg_pit_duration,
        ROUND(AVG(ABS(svf.positions_gained)), 2) AS avg_positions_changed
    FROM races r
    LEFT JOIN consistency c
        ON r.season = c.season
        AND r.round_num = c.round_num
    LEFT JOIN pit_strategy p
        ON r.season = p.season
        AND r.round_num = p.round_num
    LEFT JOIN start_vs_finish svf
        ON r.season = svf.season
        AND r.round_num = svf.round_num
    GROUP BY
        r.circuit_id,
        r.race_name
)

SELECT * FROM circuit_stats
ORDER BY circuit_id
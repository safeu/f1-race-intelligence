/*
=============================================================
Model: int_pit_strategy
=============================================================
Description:
    Calculates / Analyzes pitstop behavior per driver per race.

Depends on:
    - stg_pit_stops

Key metrics:
    - num_stops
    - stop_laps
    - total_pit_duration
    - avg_pit_duration
=============================================================
*/


WITH pit_stops AS (
    SELECT
        season,
        round_num,
        driver_id,
        lap,
        duration
    FROM {{ref('stg_pit_stops')}}
    WHERE is_normal_stop = TRUE
)

SELECT
    season,
    round_num,
    driver_id,

    COUNT(*) AS num_stops,

    ARRAY_AGG(lap ORDER BY lap) AS stop_laps,
    SUM(duration) AS total_pit_duration,
    AVG(duration) AS avg_pit_duration

FROM pit_stops

GROUP BY
    season,
    round_num,
    driver_id
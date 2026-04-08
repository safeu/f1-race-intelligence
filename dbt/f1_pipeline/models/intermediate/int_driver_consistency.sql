/*
=============================================================
Model: int_driver_consistency
=============================================================
Description:
    Calculates driver lap time consistency per race by computing
    standard deviation of lap times, excluding pit stop laps.

Depends on:
    - stg_lap_times
    - stg_pit_stops

Key metrics:
    - avg_lap_time_sec
    - stddev_lap_time_sec (lower = more consistent)
    - lap_count
=============================================================
*/



WITH lap_times AS (
    SELECT
        season,
        round_num,
        driver_id,
        lap_number,
        CASE 
            WHEN lap_time LIKE '%:%' 
            THEN (CAST(SPLIT(lap_time, ':')[OFFSET(0)] AS FLOAT64) * 60) + 
                CAST(SPLIT(lap_time, ':')[OFFSET(1)] AS FLOAT64)
            ELSE CAST(lap_time AS FLOAT64)
        END AS lap_time_sec
    FROM {{ref('stg_lap_times')}}
    
),

--script to exclude pitstops (to not mess with sd)
pit_stops AS (
    SELECT
        season,
        round_num,
        driver_id,
        lap
    FROM {{ref('stg_pit_stops')}}
),

-- script to join (left join) laptimes with pitstops (anti-join script to exclude pitstops)
lap_times_no_pits AS (
    SELECT
        lt.* 
        FROM lap_times lt 
        LEFT JOIN pit_stops ps
            ON lt.season = ps.season 
            AND lt.round_num = ps.round_num 
            AND lt.driver_id = ps.driver_id
            AND lt.lap_number = ps.lap
        WHERE ps.lap IS NULL

)


SELECT 
    season,
    round_num,
    driver_id,

    AVG(lap_time_sec) AS avg_lap_time_sec,
    STDDEV(lap_time_sec) AS stddev_lap_time_sec,
    COUNT(*) AS lap_count,
    MIN(lap_time_sec) AS min_lap_time_sec,
    MAX(lap_time_sec) AS max_lap_time_sec
FROM lap_times_no_pits
GROUP BY 
    season,
    round_num,
    driver_id
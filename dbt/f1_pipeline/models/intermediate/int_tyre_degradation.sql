/*
=============================================================
Model: int_tyre_degradation
=============================================================
Description:
    Calculates the tire degradation experienced in races. Calculated with
    lap times.

Depends on:
    - stg_lap_times
    - stg_pit_stops

Key metrics:
    - avg_lap_delta
    - degradation_slope
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

pit_stops AS(
    SELECT 
        season,
        round_num,
        driver_id,
        lap
    FROM {{ref('stg_pit_stops')}}
    WHERE is_normal_stop = TRUE
),


stints AS (
    SELECT 
        lt.*,
        (
            SELECT COUNT(*) 
            FROM pit_stops ps
            WHERE ps.season = lt.season
            AND ps.round_num = lt.round_num
            AND ps.driver_id = lt.driver_id
            AND ps.lap < lt.lap_number
        ) AS stint_number
    FROM lap_times lt
),

stints_with_lap_num AS(
    SELECT *,
        ROW_NUMBER() OVER(
            PARTITION BY season, round_num, driver_id, stint_number
            ORDER BY lap_number
        ) AS stint_lap_number
    FROM stints
),


lap_deltas AS(
    SELECT *,
        lap_time_sec - LAG(lap_time_sec) OVER(
            PARTITION BY season, round_num, driver_id, stint_number
            ORDER BY lap_number
        ) as lap_delta
    FROM stints_with_lap_num
)


SELECT
    season,
    round_num,
    driver_id,
    stint_number,

    AVG(lap_delta) AS avg_lap_delta,
    AVG(lap_delta * lap_number) / NULLIF(AVG(lap_number * lap_number), 0) AS degradation_slope

FROM lap_deltas
WHERE lap_delta IS NOT NULL

GROUP BY 
    season,
    round_num,
    driver_id,
    stint_number
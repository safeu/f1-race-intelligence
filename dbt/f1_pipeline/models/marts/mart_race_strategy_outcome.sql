/*
=============================================================
Model: mart_race_strategy_outcome
=============================================================
Description:
    Wide table combining pit strategy + tyre degradation.
    Primary mart for team/driver strategy-focused dashboard visualizations.

Depends on:
    - int_pit_strategy
    - int_tyre_degradation
    - dim_drivers
=============================================================
*/

WITH strategy AS(
    SELECT * FROM {{ref('int_pit_strategy')}}
),

tyre_degradation AS (
    SELECT
        season,
        round_num,
        driver_id,
        AVG(avg_lap_delta) AS avg_lap_delta,
        AVG(degradation_slope) AS avg_degradation_slope
    FROM {{ ref('int_tyre_degradation') }}
    GROUP BY season, round_num, driver_id
),

drivers AS (
    SELECT * FROM {{ref('dim_drivers')}}
),

joined AS(
    SELECT
        s.season,
        s.round_num,
        s.driver_id,
        d.driver_code,
        CONCAT(d.first_name, ' ', d.last_name) AS driver_name,
        d.nationality,
        s.num_stops,
        ROUND(s.total_pit_duration, 3) AS total_pit_duration,
        ROUND(s.avg_pit_duration, 3) AS avg_pit_duration,
        ROUND(td.avg_lap_delta, 4) AS avg_lap_delta,
        ROUND(td.avg_degradation_slope, 4) AS avg_degradation_slope
    FROM strategy s 
    LEFT JOIN tyre_degradation td 
        ON s.season = td.season 
        AND s.round_num = td.round_num
        AND s.driver_id = td.driver_id
    LEFT JOIN drivers d
        ON s.driver_id = d.driver_id
)

SELECT * FROM joined
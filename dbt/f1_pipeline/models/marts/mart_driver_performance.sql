/*
=============================================================
Model: mart_driver_performance
=============================================================
Description:
    Wide table combining driver performance metrics per race.
    Primary mart for driver-focused dashboard visualizations.

Depends on:
    - int_driver_consistency
    - int_start_vs_finish
    - int_head_to_head
    - int_race_incidents
    - dim_drivers
=============================================================
*/

WITH consistency AS (
    SELECT * FROM {{ ref('int_driver_consistency') }}
),

start_vs_finish AS (
    SELECT * FROM {{ ref('int_start_vs_finish') }}
),

head_to_head AS (
    SELECT * FROM {{ ref('int_head_to_head') }}
),

incidents AS (
    SELECT * FROM {{ ref('int_race_incidents') }}
),

drivers AS (
    SELECT * FROM {{ ref('dim_drivers') }}
),

joined AS (
    SELECT
        svf.season,
        svf.round_num,
        svf.race_name,
        svf.driver_id,
        d.driver_code,
        CONCAT(d.first_name, ' ', d.last_name) AS driver_name,
        d.nationality,
        svf.constructor_id,
        svf.grid_position,
        svf.finish_position,
        svf.positions_gained,
        svf.points,
        svf.status,
        ROUND(c.avg_lap_time_sec, 3) AS avg_lap_time_sec,
        ROUND(c.stddev_lap_time_sec, 4) AS stddev_lap_time_sec,
        c.lap_count,
        ROUND(c.min_lap_time_sec, 3) AS min_lap_time_sec,
        ROUND(c.max_lap_time_sec, 3) AS max_lap_time_sec,
        h2h.teammate_id,
        h2h.teammate_finish,
        h2h.beat_teammate,
        i.did_not_finish
    FROM start_vs_finish svf
    LEFT JOIN consistency c
        ON svf.season = c.season
        AND svf.round_num = c.round_num
        AND svf.driver_id = c.driver_id
    LEFT JOIN head_to_head h2h
        ON svf.season = h2h.season
        AND svf.round_num = h2h.round_num
        AND svf.driver_id = h2h.driver_id
    LEFT JOIN incidents i
        ON svf.season = i.season
        AND svf.round_num = i.round_num
        AND svf.driver_id = i.driver_id
    LEFT JOIN drivers d
        ON svf.driver_id = d.driver_id
)

SELECT * FROM joined
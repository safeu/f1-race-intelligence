/*
=============================================================
Model: mart_championship_standings
=============================================================
Description:
    Wide table combining championship progression of drivers, and
    constructor progression of their teams.

Depends on:
    - int_championship_progression
    - int_constructor_performance
    - dim_drivers
    - dim_constructors
    - int_start_vs_finish (to access constructor_id)
=============================================================
*/

WITH drivers_progression AS (
    SELECT * FROM {{ref('int_championship_progression')}}
),

constructors_progression AS (
    SELECT * FROM {{ref('int_constructor_performance')}}
),

drivers AS (
    SELECT * FROM {{ref('dim_drivers')}}
),

constructors AS (
    SELECT * FROM {{ref('dim_constructors')}}
),

svf AS (
    SELECT season, round_num, driver_id, constructor_id FROM {{ref('int_start_vs_finish')}}
),

joined AS (
    SELECT
        dp.season,
        dp.round_num,
        dp.driver_id,
        d.driver_code,
        CONCAT(d.first_name, ' ', d.last_name) AS driver_name,
        dp.race_points AS driver_race_points,
        dp.cumulative_points AS cumulative_drivers_points,

        c.constructor_name,
        cp.constructor_id,
        cp.race_points AS constructor_race_points,
        cp.cumulative_points AS cumulative_constructors_points 
    FROM drivers_progression dp 
    JOIN svf 
        ON svf.driver_id = dp.driver_id
        AND svf.season = dp.season
        AND svf.round_num = dp.round_num
    JOIN constructors_progression cp 
        ON dp.season = cp.season
        AND dp.round_num = cp.round_num
        AND svf.constructor_id = cp.constructor_id
    LEFT JOIN drivers d
        ON dp.driver_id = d.driver_id
    LEFT JOIN constructors c
        ON cp.constructor_id = c.constructor_id
)

SELECT * FROM joined
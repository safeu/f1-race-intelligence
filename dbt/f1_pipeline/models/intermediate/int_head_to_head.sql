/*
=============================================================
Model: int_head_to_head
=============================================================
Description:
    Compares drivers against their teammates per race.
    Calculates whether a driver finished ahead of their teammate.

Depends on:
    - stg_races
    - stg_sprint_races

Key metrics:
    - finish_position
    - beat_teammate (TRUE/FALSE)
=============================================================
*/

-- Race RESULTS --
WITH race_results AS (
    SELECT
        season,
        round_num,
        JSON_VALUE(result, '$.Driver.driverId') AS driver_id,
        JSON_VALUE(result, '$.Constructor.constructorId') AS constructor_id,
        CAST(JSON_VALUE(result, '$.position') AS INT64) AS finish_position
    FROM {{ ref('stg_races') }},
    UNNEST(JSON_QUERY_ARRAY(results)) AS result
),

-- Remove duplicates in race table --
race_results_dedup AS (
    SELECT DISTINCT season, round_num, driver_id, constructor_id, finish_position
    FROM race_results
),

-- Pair drivers in race table --
paired AS (
    SELECT
        r1.season,
        r1.round_num,
        r1.driver_id,
        r1.finish_position,
        r2.driver_id AS teammate_id,
        r2.finish_position AS teammate_finish
    FROM race_results_dedup r1
    JOIN race_results_dedup r2
        ON r1.season = r2.season
        AND r1.round_num = r2.round_num
        AND r1.constructor_id = r2.constructor_id
        AND r1.driver_id != r2.driver_id
),

-- Sprint Race RESULTS --
sprint_race_results AS (
    SELECT
        season,
        round_num,
        JSON_VALUE(result, '$.Driver.driverId') AS driver_id,
        JSON_VALUE(result, '$.Constructor.constructorId') AS constructor_id,
        CAST(JSON_VALUE(result, '$.position') AS INT64) AS finish_position
    FROM {{ ref('stg_sprint_races') }},
    UNNEST(JSON_QUERY_ARRAY(sprint_results)) AS result
),

-- Remove duplicates in sprint race table --
sprint_results_dedup AS (
    SELECT DISTINCT season, round_num, driver_id, constructor_id, finish_position
    FROM sprint_race_results
),

-- Pair drivers in sprint race table --
sprint_paired AS (
    SELECT
        r1.season,
        r1.round_num,
        r1.driver_id,
        r1.finish_position,
        r2.driver_id AS teammate_id,
        r2.finish_position AS teammate_finish
    FROM sprint_results_dedup r1
    JOIN sprint_results_dedup r2
        ON r1.season = r2.season
        AND r1.round_num = r2.round_num
        AND r1.constructor_id = r2.constructor_id
        AND r1.driver_id != r2.driver_id
),

-- combine race and sprint races --
all_paired AS (
    SELECT * FROM paired
    UNION ALL
    SELECT * FROM sprint_paired
)


SELECT
    season,
    round_num,
    driver_id,
    teammate_id,
    finish_position,
    teammate_finish,
    CASE WHEN finish_position < teammate_finish THEN TRUE ELSE FALSE END AS beat_teammate
FROM all_paired
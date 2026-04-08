/*
=============================================================
Model: int_championship_progression
=============================================================
Description:
    Calculates cumulative points per driver per season
    across races. Useful to track championship progression.

Depends on:
    - stg_races

Key metrics:
    - race_points
    - cumulative_points
=============================================================
*/


-- Race RESULTS --
WITH race_results AS (
    SELECT
        season,
        round_num,
        result
    FROM {{ref('stg_races')}},
    UNNEST(json_query_array(results)) AS result
),

parsed AS(
    SELECT
        season,
        round_num,
        JSON_VALUE(result, '$.Driver.driverId') AS driver_id,
        CAST(JSON_VALUE(result, '$.points') AS FLOAT64) AS race_points
    FROM race_results
),


-- Sprint Race RESULTS --
sprint_results AS (
    SELECT
        season,
        round_num,
        result
    FROM {{ref('stg_sprint_races')}},
    UNNEST(json_query_array(sprint_results)) AS result
),

sprint_parsed AS (
    SELECT
        season,
        round_num,
        JSON_VALUE(result, '$.Driver.driverId') AS driver_id,
        CAST(JSON_VALUE(result, '$.points') AS FLOAT64) AS race_points
    FROM sprint_results
),

parsed_dedup AS (
    SELECT DISTINCT
        season,
        round_num,
        driver_id,
        race_points
    FROM parsed
),

sprint_dedup AS (
    SELECT DISTINCT
        season,
        round_num,
        driver_id,
        race_points
    FROM sprint_parsed
),


-- Combined RESULTS
all_results AS (
    SELECT * FROM parsed_dedup
    UNION ALL
    SELECT * FROM sprint_dedup
),


deduplicated AS (
    SELECT
        season,
        round_num,
        driver_id,
        SUM(race_points) AS race_points
    FROM all_results
    GROUP BY season, round_num, driver_id
)


SELECT
    season,
    round_num,
    driver_id,
    race_points,
    SUM(race_points) OVER(
        PARTITION BY season, driver_id
        ORDER BY round_num
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_points
FROM deduplicated
ORDER BY season, driver_id, round_num
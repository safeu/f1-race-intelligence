/*
=============================================================
Model: int_constructor_performance
=============================================================
Description:
    Calculates cumulative points per constructor per season
    accross races. Useful to track constructor performance

Depends on:
    - stg_races
    - stg_sprint_races

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
        JSON_VALUE(result, '$.Constructor.constructorId') AS constructor_id,
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
        JSON_VALUE(result, '$.Constructor.constructorId') AS constructor_id,
        CAST(JSON_VALUE(result, '$.points') AS FLOAT64) AS race_points
    FROM sprint_results
),

parsed_dedup AS (
    SELECT DISTINCT
        season,
        round_num,
        constructor_id,
        race_points
    FROM parsed
),

sprint_dedup AS (
    SELECT DISTINCT
        season,
        round_num,
        constructor_id,
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
        constructor_id,
        SUM(race_points) AS race_points
    FROM all_results
    GROUP BY season, round_num, constructor_id
)


SELECT
    season,
    round_num,
    constructor_id,
    race_points,
    SUM(race_points) OVER(
        PARTITION BY season, constructor_id
        ORDER BY round_num
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_points
FROM deduplicated
ORDER BY season, constructor_id, round_num
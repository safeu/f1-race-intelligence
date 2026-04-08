/*
=============================================================
Model: int_race_incidents
=============================================================
Description:
    Identifies race incidents per driver per race.
    Marks drivers who did not finish (DNF) or had unusual status.

Depends on:
    - stg_races
    - stg_sprint_races

Key metrics:
    - status
    - did_not_finish (TRUE/FALSE)
=============================================================
*/

WITH race_results AS (
    SELECT
        season,
        round_num,
        race_name,
        JSON_VALUE(result, '$.Driver.driverId') AS driver_id,
        JSON_VALUE(result, '$.status') AS status
    FROM {{ ref('stg_races') }},
    UNNEST(JSON_QUERY_ARRAY(results)) AS result
),

sprint_race_results AS (
    SELECT
        season,
        round_num,
        race_name,
        JSON_VALUE(result, '$.Driver.driverId') AS driver_id,
        JSON_VALUE(result, '$.status') AS status
    FROM {{ ref('stg_sprint_races') }},
    UNNEST(JSON_QUERY_ARRAY(sprint_results)) AS result
),

all_race_incidents AS (
    SELECT * FROM race_results
    UNION ALL
    SELECT * FROM sprint_race_results
),

deduped AS (
    SELECT DISTINCT season, round_num, race_name, driver_id, status
    FROM all_race_incidents
)

SELECT
    season,
    round_num,
    race_name,
    driver_id,
    status,
    CASE 
        WHEN status IN ('Finished', 'Lapped') THEN FALSE
        ELSE TRUE
    END AS did_not_finish
FROM deduped
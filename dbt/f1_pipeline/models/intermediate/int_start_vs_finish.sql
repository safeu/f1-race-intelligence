/*
=============================================================
Model: int_start_vs_finish
=============================================================
Description:
    Compares starting grid position vs finishing position per
    driver per race. Calculates positions gained or lost. 

    Note; Sprint Races NOT included

Depends on:
    - stg_races

Key metrics:
    - grid_position
    - finish_position
    - positions_gained
=============================================================
*/

WITH race_results AS (
    SELECT
        season,
        round_num,
        race_name,
        result
    FROM {{ ref('stg_races') }},
    UNNEST(JSON_QUERY_ARRAY(results)) AS result
),

parsed AS (
    SELECT
        season,
        round_num,
        race_name,
        JSON_VALUE(result, '$.Driver.driverId') AS driver_id,
        JSON_VALUE(result, '$.Constructor.constructorId') AS constructor_id,
        CAST(JSON_VALUE(result, '$.grid') AS INT64) AS grid_position,
        CAST(JSON_VALUE(result, '$.position') AS INT64) AS finish_position,
        CAST(JSON_VALUE(result, '$.points') AS FLOAT64) AS points,
        JSON_VALUE(result, '$.status') AS status
    FROM race_results
)

SELECT
    season,
    round_num,
    race_name,
    driver_id,
    constructor_id,
    grid_position,
    finish_position,
    points,
    status,
    grid_position - finish_position AS positions_gained
FROM parsed
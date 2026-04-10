/*
=============================================================
Model: dim_constructors
=============================================================
Description:
    Dimension table for constructor display information.
    Maps constructor_id to human-readable names and attributes.

Depends on:
    - stg_races
=============================================================
*/

WITH race_results AS (
    SELECT
        JSON_VALUE(result, '$.Constructor.constructorId') AS constructor_id,
        JSON_VALUE(result, '$.Constructor.name') AS constructor_name,
        JSON_VALUE(result, '$.Constructor.nationality') AS nationality
    FROM {{ ref('stg_races') }},
    UNNEST(JSON_QUERY_ARRAY(results)) AS result
),

unique_constructors AS (
    SELECT DISTINCT
        constructor_id,
        constructor_name,
        nationality
    FROM race_results
    WHERE constructor_id IS NOT NULL
)

SELECT * FROM unique_constructors
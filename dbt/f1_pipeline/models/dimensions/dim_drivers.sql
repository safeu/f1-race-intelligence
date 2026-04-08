/*
=============================================================
Model: dim_drivers
=============================================================
Description:
    Dimension table for driver display information.
    Maps driver_id to human-readable names, codes, and attributes.

Depends on:
    - stg_races
=============================================================
*/

WITH race_results AS (
    SELECT
        JSON_VALUE(result, '$.Driver.driverId') AS driver_id,
        JSON_VALUE(result, '$.Driver.code') AS driver_code,
        JSON_VALUE(result, '$.Driver.givenName') AS first_name,
        JSON_VALUE(result, '$.Driver.familyName') AS last_name,
        JSON_VALUE(result, '$.Driver.nationality') AS nationality,
        JSON_VALUE(result, '$.Driver.dateOfBirth') AS date_of_birth
    FROM {{ ref('stg_races') }},
    UNNEST(JSON_QUERY_ARRAY(results)) AS result
),

unique_drivers AS (
    SELECT DISTINCT
        driver_id,
        driver_code,
        first_name,
        last_name,
        nationality,
        date_of_birth
    FROM race_results
    WHERE driver_id IS NOT NULL
)

SELECT * FROM unique_drivers
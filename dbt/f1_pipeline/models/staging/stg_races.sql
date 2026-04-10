/*
=============================================================
Model: stg_races
=============================================================
Description:
    Staging script for races table. Kept things raw (like json format) to just
    handle it in intermediate models. To keep it consistent and the raw files/data
    accurate

*/

WITH source AS (
    SELECT * FROM {{ source('f1_raw', 'raw_races') }}
),

renamed AS (
    SELECT 
        cast(season AS INT64) AS season,
        cast(round AS INT64) AS round_num,
        race_name,
        circuit_id,
        cast(date AS DATE) AS date,
        results,
        ingested_at

    FROM source
),

deduplicated AS (
    SELECT
        season,
        round_num,
        race_name,
        circuit_id,
        date,
        results,
        MIN(ingested_at) AS ingested_at
    FROM renamed
    GROUP BY season, round_num, race_name, circuit_id, date, results
)

SELECT * FROM deduplicated
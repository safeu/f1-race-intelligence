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
)


SELECT * FROM renamed
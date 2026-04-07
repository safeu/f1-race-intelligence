WITH source AS (
    SELECT * FROM {{ source('f1_raw', 'raw_pit_stops') }}
),

renamed AS (
    SELECT
        cast(season AS INT64) as season,
        cast(round_num AS INT64) as round_num,
        cast(lap AS INT64) as lap,
        cast(stop AS INT64) as stop,
        driver_id,
        time,
        cast(duration AS FLOAT64) as duration,
        ingested_at

    FROM source
)

SELECT * FROM renamed
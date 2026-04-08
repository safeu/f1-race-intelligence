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

        CASE
            WHEN duration IS NULL OR duration = '' THEN NULL
            WHEN duration LIKE '%:%'
            THEN (CAST(SPLIT(duration, ':')[OFFSET(0)] AS FLOAT64) * 60) +
                CAST(SPLIT(duration, ':')[OFFSET(1)] AS FLOAT64)
            ELSE CAST(duration AS FLOAT64)
        END AS duration,

        ingested_at
    FROM source
),

final_renamed AS(
    SELECT 
        *,
        
        CASE 
            WHEN duration < 120 THEN TRUE 
            ELSE FALSE 
        END AS is_normal_stop

    FROM renamed
)

SELECT * FROM final_renamed
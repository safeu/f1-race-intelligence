/*
=============================================================
Model: stg_lap_times
=============================================================
Description:
    Staging script for lap times table. Kept it raw as much as possible

*/

WITH source AS (
    SELECT * FROM {{ source('f1_raw', 'raw_lap_times') }}
),

renamed AS (
    SELECT
        cast(season AS INT64) as season,
        cast(round_num AS INT64) as round_num,
        cast(lap_number AS INT64) as lap_number,
        driver_id,
        lap_time,
        cast(position AS INT64) as position,
        ingested_at

    FROM source
)

SELECT * FROM renamed
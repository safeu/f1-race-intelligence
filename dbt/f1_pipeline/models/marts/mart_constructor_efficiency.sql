/*
=============================================================
Model: mart_constructor_efficiency
=============================================================
Description:
    Constructor reliability and performance aggregated per season.
    Includes points, DNF rate, and pit stop efficiency.

Depends on:
    - int_constructor_performance
    - int_race_incidents
    - int_pit_strategy
    - int_start_vs_finish
    - dim_constructors
=============================================================
*/

WITH constructor_performance AS (
    SELECT * FROM {{ ref('int_constructor_performance') }}
),

-- use start_vs_finish as bridge to get constructor_id per driver per race
svf AS (
    SELECT DISTINCT
        season,
        round_num,
        driver_id,
        constructor_id
    FROM {{ ref('int_start_vs_finish') }}
),

race_incidents AS (
    SELECT
        ri.season,
        ri.round_num,
        ri.driver_id,
        ri.did_not_finish,
        svf.constructor_id
    FROM {{ ref('int_race_incidents') }} ri
    LEFT JOIN svf
        ON ri.season = svf.season
        AND ri.round_num = svf.round_num
        AND ri.driver_id = svf.driver_id
),

pit_strategy AS (
    SELECT
        ps.season,
        ps.round_num,
        ps.driver_id,
        ps.avg_pit_duration,
        svf.constructor_id
    FROM {{ ref('int_pit_strategy') }} ps
    LEFT JOIN svf
        ON ps.season = svf.season
        AND ps.round_num = svf.round_num
        AND ps.driver_id = svf.driver_id
),

constructors AS (
    SELECT * FROM {{ ref('dim_constructors') }}
),

-- get final season points per constructor
season_points AS (
    SELECT
        season,
        constructor_id,
        MAX(cumulative_points) AS total_season_points
    FROM constructor_performance
    GROUP BY season, constructor_id
),

-- aggregate incidents and pit stops at constructor+season level
constructor_stats AS (
    SELECT
        ri.season,
        ri.constructor_id,
        ROUND(AVG(CASE WHEN ri.did_not_finish THEN 1.0 ELSE 0.0 END), 3) AS dnf_rate,
        ROUND(AVG(ps.avg_pit_duration), 3) AS avg_pit_duration
    FROM race_incidents ri
    LEFT JOIN pit_strategy ps
        ON ri.season = ps.season
        AND ri.round_num = ps.round_num
        AND ri.constructor_id = ps.constructor_id
    GROUP BY ri.season, ri.constructor_id
)

SELECT
    cs.season,
    cs.constructor_id,
    c.constructor_name,
    sp.total_season_points,
    cs.dnf_rate,
    cs.avg_pit_duration
FROM constructor_stats cs
LEFT JOIN season_points sp
    ON cs.season = sp.season
    AND cs.constructor_id = sp.constructor_id
LEFT JOIN constructors c
    ON cs.constructor_id = c.constructor_id
ORDER BY cs.season, sp.total_season_points DESC
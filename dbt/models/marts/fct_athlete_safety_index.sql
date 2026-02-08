-- Athlete Safety Index Mart: WBGT calculations joined with stadium metadata
-- This table provides FIFA 2026 athlete safety monitoring data

with weather_with_stadium as (
    select
        w.city,
        w.temperature,
        w.humidity,
        w.wind_speed,
        w.feelslike_c,
        w.dewpoint_c,
        w.pressure_mb,
        w.vis_km,
        w.wbgt,
        w.wbgt_flag,
        w.recorded_at,
        s.stadium_id,
        s.stadium_name,
        s.city as stadium_city,
        s.country,
        s.lat,
        s.lon,
        s.elevation_m,
        s.capacity,
        s.grass_type,
        s.has_roof
    from {{ ref('int_weather__wbgt') }} w
    left join {{ ref('dim_stadiums') }} s on 
        round(w.lat::numeric, 2) = round(s.lat::numeric, 2)
        AND round(w.lon::numeric, 2) = round(s.lon::numeric, 2)
)

select 
    stadium_id,
    stadium_name,
    city,
    country,
    lat,
    lon,
    elevation_m,
    capacity,
    grass_type,
    has_roof,
    temperature,
    humidity,
    wind_speed,
    wbgt,
    wbgt_flag,
    recorded_at
from weather_with_stadium

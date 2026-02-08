-- Weather Observations Fact Table: All weather data with stadium context
-- General-purpose fact table for comprehensive weather monitoring

with weather_with_stadium as (
    select
        w.city,
        w.temperature,
        w.humidity,
        w.wind_speed,
        w.wind_dir,
        w.precip_mm,
        w.cloud,
        w.uv,
        w.feelslike_c,
        w.dewpoint_c,
        w.pressure_mb,
        w.vis_km,
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
    from {{ ref('stg_weatherapi__current') }} w
    left join {{ ref('dim_stadiums') }} s on w.city = s.city
)

select 
    s.stadium_id,
    s.stadium_name,
    w.city,
    s.country,
    s.lat,
    s.lon,
    s.elevation_m,
    s.capacity,
    s.grass_type,
    s.has_roof,
    w.temperature,
    w.humidity,
    w.wind_speed,
    w.wind_dir,
    w.precip_mm,
    w.cloud,
    w.uv,
    w.feelslike_c,
    w.dewpoint_c,
    w.pressure_mb,
    w.vis_km,
    w.recorded_at
from weather_with_stadium w

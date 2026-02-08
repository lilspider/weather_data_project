-- Weather Observations Fact Table: All weather data with stadium context
-- General-purpose fact table for comprehensive weather monitoring

with weather_with_stadium as (
    select
        w.id,
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
    left join {{ ref('dim_stadiums') }} s on 
        round(w.lat::numeric, 2) = round(s.lat::numeric, 2)
        AND round(w.lon::numeric, 2) = round(s.lon::numeric, 2)
)

select 
    id as weather_observation_id,
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
    wind_dir,
    precip_mm,
    cloud,
    uv,
    feelslike_c,
    dewpoint_c,
    pressure_mb,
    vis_km,
    recorded_at
from weather_with_stadium

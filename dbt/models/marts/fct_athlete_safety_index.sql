-- Athlete Safety Index Mart: WBGT calculations joined with stadium metadata
-- Joins on lat/lon proximity for precise stadium matching

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
    w.wbgt,
    w.wbgt_flag,
    w.recorded_at
from {{ ref('int_weather__wbgt') }}  w
left join {{ ref('dim_stadiums') }}  s
    on round(w.lat::numeric, 2) = round(s.lat::numeric, 2)
    and round(w.lon::numeric, 2) = round(s.lon::numeric, 2)

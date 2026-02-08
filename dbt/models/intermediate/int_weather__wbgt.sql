-- Intermediate: Calculate Wet Bulb Globe Temperature (WBGT) for athlete safety monitoring
-- Passes through all staging columns + adds calculated wbgt and wbgt_flag

select
    id,
    city,
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
    weather_description,
    lat,
    lon,
    recorded_at,

    -- WBGT approximation
    round(
        (0.7 * (humidity / 100.0 * temperature)
       + 0.2 * (temperature + wind_speed * 0.1)
       + 0.1 * temperature)::numeric
    , 2) as wbgt,

    -- FIFA safety flag
    case
        when (0.7 * (humidity / 100.0 * temperature) + 0.2 * (temperature + wind_speed * 0.1) + 0.1 * temperature) < 25.6 then 'Green'
        when (0.7 * (humidity / 100.0 * temperature) + 0.2 * (temperature + wind_speed * 0.1) + 0.1 * temperature) <= 27.7 then 'Yellow'
        when (0.7 * (humidity / 100.0 * temperature) + 0.2 * (temperature + wind_speed * 0.1) + 0.1 * temperature) <= 29.3 then 'Orange'
        when (0.7 * (humidity / 100.0 * temperature) + 0.2 * (temperature + wind_speed * 0.1) + 0.1 * temperature) <= 31.0 then 'Red'
        else 'Black'
    end as wbgt_flag

from {{ ref('stg_weatherapi__current') }}

-- Intermediate: Calculate Wet Bulb Globe Temperature (WBGT) for athlete safety monitoring
-- WBGT formula: 0.7 * (humidity / 100.0 * temp_c) + 0.2 * (temp_c + wind_kph * 0.1) + 0.1 * temp_c

with weather_data as (
    select
        city,
        temperature,
        humidity,
        wind_speed,
        recorded_at
    from {{ ref('stg_weatherapi__current') }}
),

wbgt_calculated as (
    select
        city,
        temperature,
        humidity,
        wind_speed,
        recorded_at,
        -- WBGT calculation for athlete heat stress monitoring
        (0.7 * (humidity / 100.0 * temperature) + 0.2 * (temperature + wind_speed * 0.1) + 0.1 * temperature) as wbgt,
        -- FIFA safety flag classification
        case 
            when (0.7 * (humidity / 100.0 * temperature) + 0.2 * (temperature + wind_speed * 0.1) + 0.1 * temperature) < 25.6 then 'Green'
            when (0.7 * (humidity / 100.0 * temperature) + 0.2 * (temperature + wind_speed * 0.1) + 0.1 * temperature) between 25.6 and 27.7 then 'Yellow'
            when (0.7 * (humidity / 100.0 * temperature) + 0.2 * (temperature + wind_speed * 0.1) + 0.1 * temperature) between 27.8 and 29.3 then 'Orange'
            when (0.7 * (humidity / 100.0 * temperature) + 0.2 * (temperature + wind_speed * 0.1) + 0.1 * temperature) between 29.4 and 31.0 then 'Red'
            else 'Black'
        end as wbgt_flag,
        recorded_at
    from weather_data
)

select 
    city,
    temperature,
    humidity,
    wind_speed,
    wbgt,
    wbgt_flag,
    recorded_at
from wbgt_calculated

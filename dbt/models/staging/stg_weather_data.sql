-- Staging: De-duplicate raw weather readings by city and hour
-- Extract fields from WeatherAPI.com JSON structure
with src as (
    select
        id,
        city,
        -- Extract from WeatherAPI JSON structure when available, otherwise use legacy fields
        case 
            when json_data is not null then (json_data->'query'->'current'->>'temp_c')::numeric
            else temperature::numeric
        end as temperature,
        
        case 
            when json_data is not null then (json_data->'query'->'current'->>'humidity')::float
            else null
        end as humidity,
        
        case 
            when json_data is not null then (json_data->'query'->'current'->>'wind_kph')::float
            else null
        end as wind_speed,
        
        case 
            when json_data is not null then json_data->'query'->'current'->'condition'->>'text'
            else weather_descriptions
        end as weather_description,
        
        recorded_at,
        date_trunc('hour', recorded_at) as hour_bucket,
        recorded_at::date as date_bucket,
        json_data
    from dev.raw_weather_data
), ranked as (
    select *, row_number() over (partition by city, hour_bucket order by recorded_at desc, id desc) as rn
    from src
)
select 
    id, 
    city, 
    temperature,
    humidity,
    wind_speed,
    weather_description,
    recorded_at
from ranked
where rn = 1

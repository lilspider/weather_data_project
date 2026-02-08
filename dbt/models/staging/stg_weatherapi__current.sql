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
            when json_data is not null then (json_data->'query'->'current'->>'wind_degree')::int
            else null
        end as wind_dir,
        
        case 
            when json_data is not null then (json_data->'query'->'current'->>'precip_mm')::float
            else null
        end as precip_mm,
        
        case 
            when json_data is not null then (json_data->'query'->'current'->>'cloud')::int
            else null
        end as cloud,
        
        case 
            when json_data is not null then (json_data->'query'->'current'->>'uv')::float
            else null
        end as uv,
        
        case 
            when json_data is not null then (json_data->'query'->'current'->>'feelslike_c')::numeric
            else null
        end as feelslike_c,
        
        case 
            when json_data is not null then (json_data->'query'->'current'->>'dewpoint_c')::numeric
            else null
        end as dewpoint_c,
        
        case 
            when json_data is not null then (json_data->'query'->'current'->>'pressure_mb')::float
            else null
        end as pressure_mb,
        
        case 
            when json_data is not null then (json_data->'query'->'current'->>'vis_km')::float
            else null
        end as vis_km,
        
        case 
            when json_data is not null then json_data->'query'->'current'->'condition'->>'text'
            else weather_descriptions
        end as weather_description,
        
        -- Extract stadium coordinates for precise matching
        case 
            when json_data is not null then (json_data->'query'->'location'->>'lat')::numeric
            else null
        end as lat,
        
        case 
            when json_data is not null then (json_data->'query'->'location'->>'lon')::numeric
            else null
        end as lon,
        
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
    recorded_at
from ranked
where rn = 1

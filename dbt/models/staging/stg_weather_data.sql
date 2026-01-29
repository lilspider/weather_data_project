-- Staging: De-duplicate raw weather readings using ROW_NUMBER
with src as (
    select
        id,
        city,
        temperature::numeric as temperature,
        weather_descriptions,
        recorded_at
    from dev.raw_weather_data
), ranked as (
    select *, row_number() over (partition by city, recorded_at::date order by recorded_at desc, id desc) as rn
    from src
)
select id, city, temperature, weather_descriptions, recorded_at
from ranked
where rn = 1

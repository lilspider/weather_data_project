-- Daily average temperature per city
with base as (
    select
        city,
        recorded_at::date as day,
        temperature::numeric as temperature
    from {{ ref('stg_weatherapi__current') }}
)
select
    city,
    day,
    round(avg(temperature)::numeric, 2) as avg_temp
from base
group by city, day
order by city, day

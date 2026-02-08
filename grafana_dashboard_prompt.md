# Grafana Weather Dashboard Creation Prompt

## Context
I need to create a professional, modern Grafana dashboard for a weather data pipeline project. The dashboard should visualize real-time weather data from multiple cities worldwide with geomap and heatmap capabilities.

## Current Setup
- **Grafana Version**: Latest (running in Docker on port 3000)
- **Database**: PostgreSQL with weather data in `dev` schema
- **Data Source**: PostgreSQL connection to `postgres:5432/airflow_db`
- **Available Tables**:
  - `dev.raw_weather_data` - Raw JSON data with coordinates
  - `dev.stg_weather_data` - Processed staging data
  - `dev.daily_average` - Daily aggregated data

## Data Structure
### Raw Weather Data (dev.raw_weather_data)
```sql
SELECT 
    city,
    temperature,
    weather_descriptions,
    recorded_at,
    json_data::text as weather_json
FROM dev.raw_weather_data;
```

JSON structure contains:
```json
{
  "query": {
    "q": "New York",
    "location": {
      "name": "New York",
      "region": "New York", 
      "country": "United States of America",
      "lat": 40.7142,
      "lon": -74.0064,
      "tz_id": "America/New_York",
      "localtime": "2026-02-07 20:23"
    },
    "current": {
      "temp_c": -13.9,
      "temp_f": 7.0,
      "humidity": 41,
      "wind_kph": 36.4,
      "wind_mph": 22.6,
      "condition": {
        "text": "Partly cloudy",
        "icon": "//cdn.weatherapi.com/weather/64x64/night/116.png",
        "code": 1003
      },
      "pressure_mb": 1016.0,
      "visibility_km": 16.0,
      "uv": 0.0
    }
  }
}
```

### Staging Data (dev.stg_weather_data)
```sql
SELECT 
    city,
    temperature,
    humidity,
    wind_speed,
    weather_description,
    recorded_at
FROM dev.stg_weather_data;
```

### Cities Currently Monitored
- New York (40.7142, -74.0064)
- London (51.5074, -0.1278) 
- Tokyo (35.6762, 139.6503)
- Paris (48.8566, 2.3522)
- Sydney (-33.8688, 151.2093)

## Requirements

### 1. Dashboard Layout & Design
- **Modern, clean design** with dark theme
- **Responsive layout** that works on different screen sizes
- **Professional color scheme** suitable for weather data
- **Clear typography** and good contrast
- **6-8 panels** arranged in a logical grid layout

### 2. Required Panels

#### A. World Geomap Panel (Main Feature)
- **Panel Type**: Geomap (World Map)
- **Data Points**: Cities with coordinates extracted from JSON
- **Visualization**: 
  - Circle markers for each city
  - Color coding by temperature (blue=cold, red=hot)
  - Size variation by temperature magnitude
  - Tooltips showing city name, temperature, weather condition
- **Features**:
  - Zoom and pan capabilities
  - Legend showing temperature scale
  - Real-time updates (refresh every 5 minutes)

#### B. Temperature Heatmap Panel
- **Panel Type**: Heatmap
- **Data**: Temperature trends over time by city
- **X-axis**: Time (last 24 hours)
- **Y-axis**: Cities
- **Color gradient**: Blue (cold) to Red (hot)

#### C. Current Conditions Table
- **Panel Type**: Table
- **Data**: Latest weather readings for all cities
- **Columns**: City, Temperature, Weather, Humidity, Wind Speed, Last Updated
- **Sorting**: By temperature (coldest to hottest)
- **Conditional formatting**: Temperature color coding

#### D. Temperature Gauge Panel
- **Panel Type**: Gauge/Stat
- **Data**: Average temperature across all cities
- **Features**: 
  - Current average temperature
  - Min/Max indicators
  - Trend arrow (compared to previous hour)

#### E. Wind Speed Panel
- **Panel Type**: Bar Chart
- **Data**: Wind speed by city
- **Features**: 
  - Horizontal bars
  - Color coding by wind intensity
  - Units in both km/h and mph

#### F. Weather Conditions Panel
- **Panel Type**: Pie Chart or Stat Panel
- **Data**: Distribution of weather conditions
- **Features**: 
  - Show count of each weather type
  - Weather icons if possible
  - Percentages

#### G. Time Series Panel
- **Panel Type**: Time Series Graph
- **Data**: Temperature trends over last 24 hours
- **Features**:
  - Multiple lines (one per city)
  - Interactive tooltips
  - Y-axis temperature range

#### H. Database Stats Panel
- **Panel Type**: Stat
- **Data**: Database statistics
- **Metrics**: 
  - Total records
  - Last update time
  - Data freshness indicator

### 3. Technical Requirements

#### PostgreSQL Queries Needed
```sql
-- For Geomap (extract coordinates from JSON)
SELECT 
    city,
    (json_data::json->'query'->'location'->>'lat')::float as latitude,
    (json_data::json->'query'->'location'->>'lon')::float as longitude,
    temperature,
    weather_description,
    recorded_at
FROM dev.raw_weather_data 
WHERE recorded_at >= NOW() - INTERVAL '1 hour';

-- For Temperature Heatmap
SELECT 
    city,
    temperature,
    DATE_TRUNC('hour', recorded_at) as hour_bucket
FROM dev.stg_weather_data 
WHERE recorded_at >= NOW() - INTERVAL '24 hours'
ORDER BY hour_bucket, city;

-- For Current Conditions
SELECT 
    city,
    temperature,
    weather_description,
    humidity,
    wind_speed,
    recorded_at
FROM dev.stg_weather_data 
WHERE recorded_at = (SELECT MAX(recorded_at) FROM dev.stg_weather_data);
```

### 4. Grafana Configuration Best Practices
- **Data Source**: PostgreSQL with proper connection pooling
- **Refresh Intervals**: 
  - Real-time panels: 1-5 minutes
  - Historical panels: 15-30 minutes
- **Time Ranges**: 
  - Default: Last 6 hours
  - Options: Last hour, 24 hours, 7 days
- **Alerting**: Set up alerts for extreme temperatures
- **Annotations**: Mark data pipeline runs

### 5. Dashboard Variables
- **City Selection**: Single/multi-select for filtering by city
- **Time Range**: Quick time range selectors
- **Refresh Interval**: Adjustable refresh rate

### 6. Performance Considerations
- **Query Optimization**: Use proper indexing on timestamp columns
- **Data Limits**: Limit queries to reasonable time ranges
- **Caching**: Enable Grafana query caching
- **Database Connection**: Use connection pooling

### 7. Visual Design Guidelines
- **Color Palette**: 
  - Cold temperatures: Blues (#0066CC, #003D7A)
  - Warm temperatures: Oranges/Reds (#FF6B35, #C92A2A)
  - Neutral: Grays (#495057, #868E96)
- **Typography**: Clean, readable fonts
- **Spacing**: Consistent padding and margins
- **Icons**: Weather icons where appropriate

## Deliverables Needed
1. **Complete Grafana dashboard JSON** that can be imported
2. **PostgreSQL queries** for each panel
3. **Configuration files** for data source provisioning
4. **Step-by-step instructions** for importing and setup
5. **Troubleshooting guide** for common issues

## Technical Constraints
- Must work with Grafana 10.x
- PostgreSQL data source only
- No external plugins beyond what's available in standard Grafana
- Dashboard should be self-contained and importable

## Success Criteria
1. **Functional geomap** with accurate city coordinates
2. **Real-time data updates** working properly
3. **Professional appearance** suitable for production use
4. **Responsive design** that works on different screen sizes
5. **Good performance** with fast query response times
6. **Easy maintenance** with clear documentation

Please provide the complete solution including all configuration files, queries, and setup instructions.

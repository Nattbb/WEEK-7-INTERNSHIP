# Weather Data ETL Pipeline & Automation

## Project Overview
This project extracts real-time weather metrics from multiple cities, cleans and formats the structure into standardized data types, and persists the results into CSV and SQLite formats for analytical reporting.

## Data Source
- **API**: [OpenWeather API](https://openweathermap.org/api) (Current Weather Data endpoint)

## Pipeline Architecture (ETL)
1. **Extract**: Queries the REST API using Python's `requests` module to collect raw JSON payloads.
2. **Transform**: Normalizes nested JSON fields, formats timestamps, converts metric units, and loads structural data into a Pandas DataFrame.
3. **Load**: Stores clean data directly into `weather_data.csv` and streams it into a SQLite table (`weather_pipeline.db`).

## Tools & Libraries Used
- **Language**: Python 3.x
- **Libraries**: `pandas`, `requests`, `sqlite3`, `datetime`
- **IDE**: VS Code / Jupyter Notebook

## Key Insights
- Temperature variations across target cities during execution.
- Identification of high-humidity urban microclimates.

## How to Run
1. Clone this repository.
2. Install requirements: `pip install pandas requests`
3. Add your OpenWeather API key to `etl_pipeline.py`.
4. Run: `python etl_pipeline.py`

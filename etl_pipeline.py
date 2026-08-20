import sqlite3
from datetime import datetime
import pandas as pd
import requests

# Project Configuration
API_KEY = "010538ff5f2eab01ef6b720e51185786"
CITIES = ["Nairobi", "Lagos", "Johannesburg", "Cairo", "Accra"]
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather(cities_list):
    """Fetch raw weather data for a list of target cities."""
    raw_results = []
    print("--- STEP 1: EXTRACTING DATA ---")

    for city in cities_list:
        payload = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }

        try:
            res = requests.get(BASE_URL, params=payload)
            if res.status_code == 200:
                raw_results.append(res.json())
                print(f"[SUCCESS] Pulled latest data for {city}")
            else:
                print(
                    f"[WARNING] Could not get data for {city}. Code: {res.status_code}")
        except Exception as err:
            print(f"[ERROR] Connection issue for {city}: {err}")

    return raw_results


def process_weather_data(raw_data):
    """Clean and structure raw JSON responses into a dataframe."""
    print("\n--- STEP 2: TRANSFORMING DATA ---")
    formatted_data = []

    for entry in raw_data:
        info = {
            "city_name": entry.get("name"),
            "temp_celsius": entry["main"]["temp"],
            "feels_like_celsius": entry["main"]["feels_like"],
            "humidity_pct": entry["main"]["humidity"],
            "weather_condition": entry["weather"][0]["description"].title(),
            "wind_speed_ms": entry["wind"]["speed"],
            "fetch_time": datetime.fromtimestamp(entry["dt"]).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        }
        formatted_data.append(info)

    df = pd.DataFrame(formatted_data)

    df["temp_celsius"] = df["temp_celsius"].astype(float)
    df["humidity_pct"] = df["humidity_pct"].astype(int)
    df["fetch_time"] = pd.to_datetime(df["fetch_time"])

    print(f"Successfully processed {len(df)} records.")
    return df


def save_dataset(df):
    """Save processed data to both CSV and SQLite storage."""
    print("\n--- STEP 3: LOADING DATA ---")

    csv_filename = "weather_report.csv"
    df.to_csv(csv_filename, index=False)
    print(f"Data saved to local CSV file: '{csv_filename}'")

    db_name = "weather_database.db"
    conn = sqlite3.connect(db_name)
    df.to_sql("city_weather", conn, if_exists="append", index=False)
    conn.close()
    print(f"Data appended to SQLite table 'city_weather' in '{db_name}'")


def generate_summary(df):
    """Print quick metrics for reporting."""
    print("\n--- STEP 4: QUICK DATA INSIGHTS ---")

    hottest = df.loc[df["temp_celsius"].idxmax()]
    most_humid = df.loc[df["humidity_pct"].idxmax()]

    print(
        f"Hottest City: {hottest['city_name']} ({hottest['temp_celsius']}°C)")
    print(
        f"Highest Humidity: {most_humid['city_name']} ({most_humid['humidity_pct']}%)")

    print("\nOverall Averages across cities:")
    print(f"- Temp: {df['temp_celsius'].mean():.2f}°C")
    print(f"- Humidity: {df['humidity_pct'].mean():.2f}%")
    print(f"- Wind Speed: {df['wind_speed_ms'].mean():.2f} m/s")


if __name__ == "__main__":
    weather_json = fetch_weather(CITIES)

    if weather_json:
        clean_df = process_weather_data(weather_json)
        save_dataset(clean_df)
        generate_summary(clean_df)
    else:
        print("Pipeline aborted due to missing extraction data.")

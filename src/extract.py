import urllib3
import pandas as pd
import requests
import os
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_weather(lat, lon, api_key):
    if not lat or not lon:
        return None, None
    
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data['main']['temp'], data['main']['humidity']
        else:
            print(f"Weather API Error - Status Code: {resp.status_code}, Message: {resp.text}")
            return None, None
    except Exception as e:
        print(f"Weather API Request Error: {e}")
    return None, None

def extract_air4thai_data():
    url = "https://air4thai.pcd.go.th/services/getNewAQI_JSON.php"
    
    weather_api_key = os.getenv("OPENWEATHER_API_KEY")
    if not weather_api_key:
        print("⚠️ Warning: OPENWEATHER_API_KEY not found in .env!")

    try:
        print("Extracting data from Air4Thai and OpenWeatherMap...")
        response = requests.get(url, timeout=15, verify=False)
        response.raise_for_status()
        data = response.json()
        stations = data.get("stations", [])

        raw_list = []
        for station in stations:
            area = station.get("areaTH", "")
            name_th = station.get("nameTH", "")

            # กรองเฉพาะสถานีในเขตกรุงเทพฯ
            if "กรุงเทพ" in name_th or "กรุงเทพ" in area:
                aqi_data = station.get("AQILast", {})
                pm25_data = aqi_data.get("PM25", {})
                
                lat = station.get("lat")
                lon = station.get("long")
                
                # 🌟 ดึงอุณหภูมิและความชื้น
                temp, humidity = None, None
                if weather_api_key and lat and lon:
                    temp, humidity = get_weather(lat, lon, weather_api_key)
                    # หน่วงเวลา 0.2 วินาที ป้องกัน OpenWeatherMap บล็อกจากการยิง API รัวไป (Free tier limit 60 calls/min)
                    time.sleep(0.2) 

                raw_list.append({
                    "station_id": station.get("stationID"),
                    "station_name": name_th,
                    "district_name": area,
                    "latitude": lat,
                    "longitude": lon,
                    "pm25": pm25_data.get("value", None),
                    "temp": temp,             # เพิ่มอุณหภูมิ
                    "humidity": humidity,     # เพิ่มความชื้น
                    "recorded_date": aqi_data.get("date"),
                    "recorded_time": aqi_data.get("time"),
                })

        df_raw = pd.DataFrame(raw_list)
        print(f"Extracted {len(df_raw)} raw records with weather data.")
        return df_raw

    except Exception as e:
        print(f"Error during extraction: {e}")
        return pd.DataFrame()
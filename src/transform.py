from datetime import datetime
import pandas as pd
import numpy as np

def transform_data(df):
  if df.empty:
    print("DataFrame is empty, skipping transformation.")
    return pd.DataFrame()

  print("Starting data transformation...")
  df_clean = df.copy()

  # 1. แปลง Data Type เป็นตัวเลข
  df_clean["pm25"] = pd.to_numeric(df_clean["pm25"], errors="coerce")
  df_clean["temp"] = pd.to_numeric(df_clean["temp"], errors="coerce")         # 🌟 เพิ่ม temp
  df_clean["humidity"] = pd.to_numeric(df_clean["humidity"], errors="coerce") # 🌟 เพิ่ม humidity
  df_clean["latitude"] = pd.to_numeric(df_clean["latitude"], errors="coerce")
  df_clean["longitude"] = pd.to_numeric(df_clean["longitude"], errors="coerce")

  # 2. จัดการฟิลด์วันที่และเวลา
  current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  df_clean["recorded_at"] = current_timestamp
  df_clean["record_date"] = datetime.now().strftime("%Y-%m-%d")

  # 3. 🌟 เพิ่ม temp กับ humidity เข้าไปในลิสต์คอลัมน์ที่จะใช้
  columns_to_keep = [
      "station_id",
      "station_name",
      "district_name",
      "latitude",
      "longitude",
      "pm25",
      "temp",       
      "humidity",   
      "recorded_at",
      "record_date" 
  ]
  df_clean = df_clean[columns_to_keep]

  # 4. สกัดชื่อเขต
  df_clean["district_name"] = df_clean["district_name"].str.extract(r'(เขต[ก-๙]+)')

  # 5. ลบแถวที่ไม่มีข้อมูลพิกัดทิ้ง
  df_clean = df_clean.dropna(subset=["latitude", "longitude"])

  # 6. แปลงค่า NaN ทั้งหมดให้เป็น None 
  df_clean = df_clean.replace({np.nan: None})

  print(f"Transformed successfully. Ready records: {len(df_clean)}")
  return df_clean
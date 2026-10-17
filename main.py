import os
from dotenv import load_dotenv
from src.extract import extract_air4thai_data
from src.load import load_to_supabase
from src.transform import transform_data

# โหลดค่าจาก .env เฉพาะตอนรันบนเครื่อง Local
load_dotenv()


def run_pipeline():
  print("=== Starting Daily Air Quality ETL Pipeline ===")

  # 1. Extract
  df_raw = extract_air4thai_data()

  # 2. Transform
  df_transformed = transform_data(df_raw)

  # 3. Load
  load_to_supabase(df_transformed)

  print("=== Pipeline Finished ===")


if __name__ == "__main__":
  run_pipeline()
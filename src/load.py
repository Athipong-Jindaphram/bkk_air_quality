import os
import pandas as pd
from supabase import create_client

def load_to_supabase(df):
  """บันทึกข้อมูลลงฐานข้อมูล Supabase"""
  if df.empty:
    print("No data to load into Supabase.")
    return

  supabase_url = os.getenv("SUPABASE_URL")
  supabase_key = os.getenv("SUPABASE_KEY")

  if not supabase_url or not supabase_key:
    raise ValueError(
        "Supabase credentials missing! Check environment variables."
    )

  supabase = create_client(supabase_url, supabase_key)
  records = df.to_dict(orient="records")

  try:
    print(f"Loading {len(records)} records to Supabase...")
    
    # 🌟 ใช้ upsert แทน insert โดยระบุคอลัมน์ที่ใช้เช็คซ้ำ (on_conflict)
    response = supabase.table("bkk_air_quality").upsert(
        records, 
        on_conflict="station_id, record_date"
    ).execute()
    
    print("Successfully loaded data into Supabase!")
  except Exception as e:
    print(f"Error loading data to Supabase: {e}")
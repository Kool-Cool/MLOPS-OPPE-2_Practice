import pandas as pd
import os
from pathlib import Path
from datetime import datetime, timedelta

def create_parquet_for_feast(input_csv_path: str, output_parquet_path: str):
    """
    Reads a raw transaction CSV, adds required columns for Feast
    (transaction_id, event_timestamp), and saves it as a Parquet file.

    Args:
        input_csv_path (str): Path to the raw input CSV file.
        output_parquet_path (str): Path to save the output Parquet file.
    """
    print(f"--- Preparing {input_csv_path} for Feast ---")
   
    try:
        df = pd.read_csv(input_csv_path)
    except FileNotFoundError:
        print(f"❌ Error: Data file not found at {input_csv_path}")
        return

    # Add a unique ID for each transaction
    if 'transaction_id' not in df.columns:
        df['transaction_id'] = df.index
        print("✅ Added 'transaction_id' column.")

    # Convert the 'Time' column from seconds to a datetime object
    if 'event_timestamp' not in df.columns:
        base_date = datetime(2022, 1, 1)
        df['event_timestamp'] = df['Time'].apply(lambda sec: base_date + timedelta(seconds=int(sec)))
        print("✅ Converted 'Time' to realistic 'event_timestamp'.")
    # Ensure the output directory exists
    output_dir = Path(output_parquet_path).parent
    os.makedirs(output_dir, exist_ok=True)
   
    # Save the processed DataFrame as a Parquet file
    df.to_parquet(output_parquet_path)
   
    print(f"💾 Successfully saved Feast-ready data to: {output_parquet_path}")
    print("---------------------------------------------------\n")

if __name__ == "__main__":
    # Define paths for your v0 and v1 data
    input_path = "data/transactions.csv"    
   
    # Define output paths for the new Parquet files
    output_path = "data/transactions.parquet"    

    # Process both datasets
    create_parquet_for_feast(input_path, output_path)

import pandas as pd
from feast import FeatureStore
from datetime import datetime

def materialize_features():
    """
    Connects to the feature store, reads the timestamp range from the
    source Parquet file, and materializes the features into the online store.
    """
    print("--- Starting Feature Materialization ---")
   
    # Load the feature store from the current directory
    store = FeatureStore(repo_path=".")

    # Load the source Parquet data to determine the time range
    # The path is relative to the root of the project, so we go up one level.
    data_path = "../data/transactions.parquet"
    try:
        df = pd.read_parquet(data_path)
    except FileNotFoundError:
        print(f"❌ Error: Data file not found at {data_path}")
        return

    if df.empty or 'event_timestamp' not in df.columns:
        raise ValueError("❌ Data is empty or missing 'event_timestamp' column")

    # Ensure the timestamp column is in the correct format
    df['event_timestamp'] = pd.to_datetime(df['event_timestamp'])

    # Get the start and end time for materialization
    start_time = df['event_timestamp'].min()
    end_time = df['event_timestamp'].max()
   
    print(f"Materializing features from {start_time} to {end_time}...")

    # Materialize the features for the specified time range.
    # materialize_incremental is used to load data between a start and end date.
    store.materialize_incremental(end_date=end_time)

    print("✅ Feature materialization complete.")
    print("--------------------------------------\n")

if __name__ == "__main__":
    materialize_features()


import pandas as pd
import joblib
import os
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from feast import FeatureStore

def test_artifact_exists():
    """Tests if the essential model artifact from training exists."""
    assert os.path.exists("artifacts/model.pkl"), "Model artifact 'model.pkl' not found."
def test_model_performance():
    """
    Tests if the trained model's F1-score on the test set (retrieved from Feast)
    is above a reasonable threshold.
    """
    # 1. Load the trained model
    model = joblib.load("artifacts/model.pkl")    
    # 2. Connect to the feature store
    store = FeatureStore(repo_path="feature_repo")

    # 3. Load the raw data to get entity IDs for the test set
    raw_data = pd.read_parquet("data/transactions.parquet")
    
    # Re-create the exact same train/test split on the entity data
    _, test_entity_df = train_test_split(
        raw_data[["transaction_id", "event_timestamp", "Class"]],
        test_size=0.2,
        random_state=42,
        stratify=raw_data["Class"]
    )
    # 4. Retrieve features for the test set from Feast
    feature_names = [f"transaction_features:{f}" for f in model.feature_names_in_]
    test_df = store.get_historical_features(
        entity_df=test_entity_df,
        features=feature_names,
    ).to_df()

    # 5. Prepare data and make predictions
    X_test = test_df.drop(columns=["transaction_id", "event_timestamp", "Class"])
    y_test = test_df["Class"]
    
    predictions = model.predict(X_test)
    f1 = f1_score(y_test, predictions)
    
    print(f"Model F1-Score on Feast-generated test set: {f1:.4f}")
    
    # Set a reasonable minimum performance threshold
    assert f1 > 0.1, f"F1 Score ({f1}) is below the 0.1 threshold."
####this is as per the feast

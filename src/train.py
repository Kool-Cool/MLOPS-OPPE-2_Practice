  GNU nano 5.4                                      src/train.py                                               
        }
        model = DecisionTreeClassifier(**params)
        model.fit(X_train, y_train)       
        # Evaluate model performance using F1-score, which is good for imbalanced data
        y_pred = model.predict(X_val)
        f1 = f1_score(y_val, y_pred)
        print(f"Validation F1-Score: {f1:.4f}")       
        # Log parameters and metrics to MLflow
        mlflow.log_params(params)
        mlflow.log_metric("f1_score", f1)       
        # Log the model to MLflow for tracking and registration
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            registered_model_name="fraud-detection-dt"
        )
        print(f"Model logged to MLflow. Run ID: {run.info.run_id}")
        # --- Save the final model locally for the API ---
        os.makedirs("artifacts", exist_ok=True)
        model_path = "artifacts/model.pkl"
        joblib.dump(model, model_path)
        print(f"Model artifact saved locally to: {model_path}")
        # --- Upload the final model directly to GCS ---
        bucket_name = "instance-20251130-103503-bucket" # Your bucket name
        destination_path = "production_models/model.pkl"
        upload_to_gcs(bucket_name, model_path, destination_path)
if __name__ == "__main__":
    # Make sure your MLflow server is running and accessible
    # Replace with your server's IP address

    mlflow.set_tracking_uri("http://35.185.53.51:5000") #<-- Example IP
    mlflow.set_experiment("Fraud_Detection_Training")
    train_model()

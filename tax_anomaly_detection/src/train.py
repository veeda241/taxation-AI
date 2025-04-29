import joblib
import os
from sklearn.ensemble import IsolationForest
from src.preprocess import load_data, preprocess_features

def train_model(X):
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    model.fit(X)
    return model

def save_artifacts(model, scaler, model_dir="models/"):
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(model, os.path.join(model_dir, "model.pkl"))
    joblib.dump(scaler, os.path.join(model_dir, "scaler.pkl"))
    print("[+] Model and Scaler saved.")

def train_pipeline(data_path, features):
    df = load_data(data_path)
    X_scaled, scaler = preprocess_features(df, features)
    model = train_model(X_scaled)
    save_artifacts(model, scaler)


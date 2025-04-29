import joblib
from src.preprocess import load_data

def load_artifacts(model_path="models/model.pkl", scaler_path="models/scaler.pkl"):
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler

def predict_anomalies(df, features, model, scaler):
    X_scaled = scaler.transform(df[features])
    predictions = model.predict(X_scaled)
    df['anomaly'] = predictions  # -1 = anomaly, 1 = normal
    return df


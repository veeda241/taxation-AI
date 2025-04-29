import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_data(file_path):
    """Load dataset from CSV."""
    return pd.read_csv(file_path)

def preprocess_features(df, feature_columns):
    """Scale selected features."""
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[feature_columns])
    return X_scaled, scaler


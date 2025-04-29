from src.train import train_pipeline
from src.predict import load_artifacts, predict_anomalies
from src.preprocess import load_data
import glob
import os

# Automatically find the first CSV file in /data/
data_files = glob.glob(os.path.join('data', '*.csv'))
if not data_files:
    raise FileNotFoundError("❌ No CSV files found in the /data/ folder. Please add a dataset.")
DATA_PATH = data_files[0]

FEATURES = [
    'total_income',
    'total_expenses',
    'tax_paid',
    'tax_due',
    'tax_refund_claimed',
    'declarations_of_assets',
    'foreign_income',
    'tax_credits_claimed',
    'charitable_donations',
    'high_value_transactions'
]

if __name__ == "__main__":
    print(f"[+] Using dataset: {DATA_PATH}")  # Print which file is picked
    mode = input("Enter mode (train/predict): ").strip().lower()

    if mode == 'train':
        print("[*] Starting training pipeline...")
        train_pipeline(DATA_PATH, FEATURES)

    elif mode == 'predict':
        print("[*] Starting prediction pipeline...")
        model, scaler = load_artifacts()
        df = load_data(DATA_PATH)
        result = predict_anomalies(df, FEATURES, model, scaler)

        anomalies = result[result['anomaly'] == -1]
        print(f"[+] Detected {len(anomalies)} anomalies.")
        print(anomalies)

    else:
        print("❌ Invalid mode. Please choose 'train' or 'predict'.")

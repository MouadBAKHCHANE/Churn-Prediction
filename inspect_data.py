import pandas as pd
import os

files = ["Telco_Churn_Enrichi_GCP.csv", "WA_Fn-UseC_-Telco-Customer-Churn.csv"]

for f in files:
    if os.path.exists(f):
        print(f"\n--- Analyzing {f} ---")
        try:
            df = pd.read_csv(f)
            print("Shape:", df.shape)
            print("\nColumns:", df.columns.tolist())
            print("\nFirst 3 rows:")
            print(df.head(3))
            print("\nInfo:")
            print(df.info())
        except Exception as e:
            print(f"Error reading {f}: {e}")
    else:
        print(f"{f} not found.")
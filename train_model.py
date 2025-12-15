import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.preprocessing import LabelEncoder
import joblib

def train_churn_model():
    print("Loading data...")
    df = pd.read_csv("Telco_Churn_Enrichi_GCP.csv")
    
    # Preprocessing
    print("Preprocessing...")
    # Drop ID
    df = df.drop('customerID', axis=1)
    
    # Encode Categorical Variables
    le = LabelEncoder()
    # Identify categorical columns
    cat_cols = df.select_dtypes(include=['object']).columns
    
    # Keep track of mappings if needed, but for now just encode
    for col in cat_cols:
        df[col] = le.fit_transform(df[col])
        
    # Split Data
    X = df.drop('Churn', axis=1)
    y = df['Churn']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Model
    print("Training Random Forest...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    
    # Evaluate
    print("Evaluating...")
    y_pred = rf.predict(X_test)
    y_prob = rf.predict_proba(X_test)[:, 1]
    
    print("\nClassification Report:")
    report = classification_report(y_test, y_pred)
    print(report)
    
    # Save Report
    with open("model_performance.txt", "w") as f:
        f.write(report)
        f.write(f"\nROC AUC Score: {roc_auc_score(y_test, y_prob):.4f}")
    
    # Save Model and Encoders for Dashboard
    print("Saving model and encoders...")
    joblib.dump(rf, "rf_model.pkl")
    
    # We need to save the encoders to properly transform input in the dashboard
    # Retraining the encoders to ensure we capture all mappings cleanly for the dashboard
    encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col]) # Re-fit on full data for consistency in dashboard dropdowns
        encoders[col] = le
    joblib.dump(encoders, "encoders.pkl")

    # Feature Importance
    print("Generating Feature Importance Plot...")
    importances = rf.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    plt.figure(figsize=(10, 6))
    plt.title("Feature Importances (Top 10)")
    plt.bar(range(10), importances[indices][:10], align="center")
    plt.xticks(range(10), [X.columns[i] for i in indices[:10]], rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('feature_importance.png')
    plt.close()
    
    # Confusion Matrix
    print("Generating Confusion Matrix...")
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.savefig('confusion_matrix.png')
    plt.close()
    
    print("Done. Artifacts saved: feature_importance.png, confusion_matrix.png, model_performance.txt")

if __name__ == "__main__":
    train_churn_model()

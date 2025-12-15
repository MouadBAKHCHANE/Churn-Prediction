# 💰 Predicting & Preventing Customer Churn: AI-Driven Retention Strategy

<div align="center">
  <img src="profitability_impact.png" alt="Profitability Impact" width="800"/>
</div>

## 📌 Project Overview
In the highly competitive telecommunications sector, customer retention is often more valuable than acquisition. This project analyzes a dataset of **7,000+ customers** to identify the key drivers of churn and quantifies the financial impact of losing high-value clients.

By leveraging **Python** and **Machine Learning (Random Forest)**, this project moves beyond simple analysis to actionable prediction, achieving **85% accuracy** in identifying at-risk customers.

### 🎯 Key Business Insights
*   **Revenue Risk:** High-value customers (those with high `TotalChanges` and `Rentabilite_Nette_Simulee`) have specific churn triggers. Identifying them early saves significant revenue.
*   **The "Sentiment" Signal:** The `Score_Sentiment_Dernier_Mois` is a newly engineered feature that proves to be a strong leading indicator of churn.
*   **Contract Lock-in:** Month-to-month contracts remains the single biggest predictor of churn, suggesting a need for incentivized long-term plans.

---

## 📊 Data & Methodology
**Dataset:** 7,043 Customer records (Enriched Telco Churn Dataset).
**Tech Stack:** `Python`, `Pandas`, `Scikit-Learn`, `Seaborn`.

### Exploratory Data Analysis (EDA)
We started by auditing the data quality (0 missing values) and analyzing distributions.
*   **Churn Rate:** 26.5% of the base has churned.
*   **Profitability:** We analyzed `Rentabilite_Nette_Simulee` to prioritize retention efforts based on potential profit loss rather than just raw churn probability.

<div align="center">
  <img src="churn_distribution.png" alt="Churn Distribution" width="400"/>
  <img src="profitability_distribution.png" alt="Profitability Distribution" width="400"/>
</div>

---

## 🤖 Predictive Modeling
We trained a **Random Forest Classifier** to predict customer churn probability.

### Performance
*   **Accuracy:** 85%
*   **Key Metric:** We optimized for **Recall** on the Churn class to minimize "False Negatives" (missing a customer who is about to leave).

### Feature Importance
What actually drives churn? Our model identified the top factors:

<div align="center">
  <img src="feature_importance.png" alt="Feature Importance" width="700"/>
</div>

1.  **Total Charges / Profitability:** Financials are the strongest predictors.
2.  **Tenure:** New customers are the most volatile.
3.  **Contract Type:** (Encoded in categorical features).

---

## 💡 Strategic Recommendations
Based on the analysis, the following actions are recommended:

1.  **Prioritize High-Value "At-Risk" Accounts:**
    *   Don't target *all* high-probability churners. Focus on those with high **Predicted Profitability**.
    *   Use the model's `predict_proba()` to rank customers by Risk * Value.

2.  **Intervention Strategy:**
    *   Customers with low `Tenure` (0-12 months) and high `MonthlyCharges` are in the "Danger Zone".
    *   **Action:** Offer a "12-Month Loyalty Discount" to migrate them from Month-to-Month contracts.

3.  **Sentiment Monitoring:**
    *   Integrate the `Score_Sentiment` real-time feed into the support dashboard to flag unhappy customers *before* they cancel.

---

## 🚀 How to Run this Project

1.  **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/telco-churn-ai.git
    cd telco-churn-ai
    ```

2.  **Install Dependencies**
    ```bash
    pip install pandas numpy matplotlib seaborn scikit-learn
    ```

3.  **Run the Analysis & Model**
    ```bash
    python analyze_dataset.py  # Generates EDA report
    python train_model.py      # Trains model & saves metrics
    python profitability_analysis.py # Generates business plots
    ```

4.  **Launch the Dashboard**
    ```bash
    streamlit run dashboard.py
    ```

---
*Author: Mouad Bakhchane*

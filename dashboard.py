import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

# Load Assets
@st.cache_resource
def load_assets():
    model = joblib.load("rf_model.pkl")
    encoders = joblib.load("encoders.pkl")
    df = pd.read_csv("Telco_Churn_Enrichi_GCP.csv")
    return model, encoders, df

try:
    model, encoders, df = load_assets()
except Exception as e:
    st.error(f"Error loading assets: {e}")
    st.stop()

# --- SIDEBAR ---
st.sidebar.title("📱 Telco Churn AI")
st.sidebar.image("https://img.icons8.com/color/96/000000/data-configuration.png", width=80) 
page = st.sidebar.radio("Navigate", ["Analysis Dashboard", "Churn Predictor"])

st.sidebar.markdown("---")
st.sidebar.markdown("Built with 🧠 by Mouad Bakhchane")

# --- PAGE 1: ANALYSIS DASHBOARD ---
if page == "Analysis Dashboard":
    st.title("📊 Customer Retention Audit")
    
    # KPIs
    churn_rate = (df['Churn'].value_counts(normalize=True)['Yes'] * 100)
    total_rev_risk = df[df['Churn'] == 'Yes']['TotalCharges'].sum()
    avg_sentiment = df['Score_Sentiment_Dernier_Mois'].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Churn Rate", f"{churn_rate:.1f}%", "-2.1%")
    col2.metric("Revenue at Risk", f"${total_rev_risk:,.0f}", "High")
    col3.metric("Avg Sentiment", f"{avg_sentiment:.2f}", "Stable")
    
    st.markdown("---")
    
    # Interactive Plots
    st.subheader("🔍 Deep Dive Analysis")
    
    col_filter = st.selectbox("Select Category to Analyze:", ['Contract', 'PaymentMethod', 'InternetService', 'gender'])
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Calculate churn rate by category
    analysis = df.groupby(col_filter)['Churn'].value_counts(normalize=True).unstack()
    if 'Yes' in analysis.columns:
        sns.barplot(x=analysis.index, y=analysis['Yes'], palette="Reds", ax=ax)
        ax.set_ylabel("Churn Probability")
        ax.set_title(f"Churn Risk by {col_filter}")
        for container in ax.containers:
            ax.bar_label(container, fmt='%.2f')
    
    st.pyplot(fig)
    
    st.markdown("### 💰 Profitability Impact")
    st.image("profitability_impact.png", caption="Net Profitability of Retained vs Churned Customers")

# --- PAGE 2: CHURN PREDICTOR ---
elif page == "Churn Predictor":
    st.title("🔮 Real-Time Churn Simulator")
    st.markdown("Adjust customer parameters to see how they impact retention probability.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        tenure = st.slider("Tenure (Months)", 0, 72, 12)
        monthly_charges = st.slider("Monthly Charges ($)", 18.0, 118.0, 70.0)
        total_charges = st.number_input("Total Charges ($)", 0.0, 10000.0, 1000.0)
        sentiment = st.slider("Sentiment Score (-1 to 1)", -1.0, 1.0, 0.1)
        
    with col2:
        contract = st.selectbox("Contract Type", df['Contract'].unique())
        internet = st.selectbox("Internet Service", df['InternetService'].unique())
        payment = st.selectbox("Payment Method", df['PaymentMethod'].unique())
        acq_cost = st.slider("Acquisition Cost ($)", 0.0, 1000.0, 200.0)
        
    # Prepare Input
    input_data = pd.DataFrame({
        'tenure': [tenure],
        'MonthlyCharges': [monthly_charges],
        'TotalCharges': [total_charges],
        'Score_Sentiment_Dernier_Mois': [sentiment],
        'Cout_Acquisition_Client': [acq_cost],
        # Add dummy values for other numeric features the model expects but we don't adjust
        'SeniorCitizen': [0],
        'Rentabilite_Nette_Simulee': [0] # Placeholder
    })
    
    # Add Categoricals
    cat_mapping = {
        'Contract': contract,
        'InternetService': internet,
        'PaymentMethod': payment,
        'gender': 'Male', # Default
        'Partner': 'No',
        'Dependents': 'No',
        'PhoneService': 'Yes',
        'MultipleLines': 'No',
        'OnlineSecurity': 'No',
        'OnlineBackup': 'No',
        'DeviceProtection': 'No',
        'TechSupport': 'No',
        'StreamingTV': 'No',
        'StreamingMovies': 'No',
        'PaperlessBilling': 'Yes'
    }
    
    # We need to construct the FULL feature vector expected by the model
    # This involves ensuring all columns are present and encoded correctly
    
    # 1. Start with a template row from the original DF to get structure
    template = df.drop(['Churn', 'customerID'], axis=1).iloc[0].copy()
    
    # 2. Update with our inputs
    template['tenure'] = tenure
    template['MonthlyCharges'] = monthly_charges
    template['TotalCharges'] = total_charges
    template['Score_Sentiment_Dernier_Mois'] = sentiment
    
    for col, val in cat_mapping.items():
        template[col] = val
        
    # 3. Create DataFrame and Encode
    input_df = pd.DataFrame([template])
    
    # Encode using saved encoders
    for col, le in encoders.items():
        if col in input_df.columns:
            try:
                # Handle unknown labels
                input_df[col] = input_df[col].apply(lambda x: le.transform([x])[0] if x in le.classes_ else 0) 
            except:
                pass

    if st.button("Predict Churn Risk"):
        try:
            prob = model.predict_proba(input_df)[0][1]
            st.markdown("---")
            st.metric("Probability of Churn", f"{prob*100:.1f}%")
            
            if prob > 0.5:
                st.error("⚠️ High Risk Customer! Suggest Intervention.")
            else:
                st.success("✅ Safe Customer.")
                
        except Exception as e:
            st.error(f"Prediction Error: {e}")

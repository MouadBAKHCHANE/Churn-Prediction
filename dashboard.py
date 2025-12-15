import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib

# Page Config
st.set_page_config(
    page_title="RetainAI Dashboard",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern Dark Mode
st.markdown("""
<style>
    /* Global Background */
    .stApp {
        background-color: #0E1117;
    }
    
    /* Card Style - Dark */
    .metric-card {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 12px;
        box_shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        border: 1px solid #303030;
        margin-bottom: 20px;
    }
    
    .metric-title {
        color: #A0A0A0;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-value {
        color: #FFFFFF;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 5px 0;
    }
    
    .metric-delta {
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .metric-delta.positive { color: #00E676; }
    .metric-delta.negative { color: #FF5252; }
    
    /* Headers */
    h1, h2, h3 {
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #262730;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #2962FF;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #0039CB;
        box-shadow: 0 4px 12px rgba(41, 98, 255, 0.2);
    }
    
</style>
""", unsafe_allow_html=True)


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
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/data-configuration.png", width=60)
    st.title("RetainAI")
    st.markdown("Intelligence Suite")
    
    st.markdown("---")
    
    page = st.radio("Navigate", ["📊 Overview & Insights", "🔮 Churn Simulator"], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("### Settings")
    st.checkbox("Dark Mode", value=True, disabled=True, help="Dark Mode active")
    
    st.markdown("---")
    st.markdown("Built with 🧠 by Mouad Bakhchane")

# --- HELPER: METRIC CARD ---
def metric_card(title, value, delta=None, delta_color="normal"):
    delta_html = ""
    if delta:
        color_class = "positive" if delta_color == "green" else "negative"
        arrow = "↑" if delta_color == "green" else "↓"
        delta_html = f'<span class="metric-delta {color_class}">{arrow} {delta}</span>'
        
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


# --- PAGE 1: OVERVIEW & INSIGHTS ---
if page == "📊 Overview & Insights":
    st.title("Executive Overview")
    st.markdown("Real-time monitoring of customer retention and financial health.")
    
    # KPIs Row
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate Metrics
    churn_rate = (df['Churn'].value_counts(normalize=True)['Yes'] * 100)
    total_rev_risk = df[df['Churn'] == 'Yes']['TotalCharges'].sum()
    avg_sentiment = df['Score_Sentiment_Dernier_Mois'].mean()
    high_value_risk = len(df[(df['Rentabilite_Nette_Simulee'] > 2000) & (df['Churn'] == 'Yes')])

    with col1:
        metric_card("Churn Rate", f"{churn_rate:.1f}%", "2.1% vs Last Month", "green") # Mock delta
    with col2:
        metric_card("Revenue at Risk", f"${total_rev_risk:,.0f}", "Critical Impact", "red")
    with col3:
        metric_card("Avg Sentiment", f"{avg_sentiment:.2f}", "Stable", "green")
    with col4:
        metric_card("High Value Losses", f"{high_value_risk}", "Customers > $2k Net", "red")

    st.markdown("### 🔍 Deep Dive Analysis")
    
    # Layout: Chart Left (2/3), Insights Right (1/3)
    c1, c2 = st.columns([2, 1])
    
    with c1:
        tab1, tab2 = st.tabs(["Churn by Category", "Profitability Distribution"])
        
        with tab1:
            col_filter = st.selectbox("Select Category:", ['Contract', 'InternetService', 'PaymentMethod'], key="cat_filter")
            
            # Prepare Data for Plotly
            churn_counts = df.groupby([col_filter, 'Churn']).size().reset_index(name='Count')
            # Calculate percentages
            total_counts = df.groupby(col_filter).size().reset_index(name='Total')
            churn_counts = churn_counts.merge(total_counts, on=col_filter)
            churn_counts['Percentage'] = (churn_counts['Count'] / churn_counts['Total']) * 100
            
            fig = px.bar(
                churn_counts, 
                x=col_filter, 
                y='Count', 
                color='Churn', 
                barmode='group',
                text_auto=True,
                color_discrete_map={'No': '#2962FF', 'Yes': '#FF3D00'},
                title=f"Customer Distribution by {col_filter}"
            )
            # Dark Mode Plotly Updates
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", 
                paper_bgcolor="rgba(0,0,0,0)",
                font={'color': '#FAFAFA'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with tab2:
            fig2 = px.histogram(
                df, 
                x="Rentabilite_Nette_Simulee", 
                color="Churn", 
                nbins=40,
                marginal="box",
                title="Profitability Distribution: Churned vs Retained",
                color_discrete_map={'No': '#2962FF', 'Yes': '#FF3D00'},
                opacity=0.7
            )
            fig2.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", 
                paper_bgcolor="rgba(0,0,0,0)",
                font={'color': '#FAFAFA'}
            )
            st.plotly_chart(fig2, use_container_width=True)

    with c2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">💡 AI Insights</div>
            <br>
        """, unsafe_allow_html=True)
        
        # Dynamic Commentary Logic
        st.markdown("**1. Contract Risk**")
        month_to_month_churn = df[df['Contract'] == 'Month-to-month']['Churn'].value_counts(normalize=True).get('Yes', 0)
        st.caption(f"Month-to-month users tend to churn at a rate of **{month_to_month_churn*100:.1f}%**, making them the highest risk segment.")
        
        st.markdown("**2. Fiber Optic Alert**")
        fiber_churn = df[df['InternetService'] == 'Fiber optic']['Churn'].value_counts(normalize=True).get('Yes', 0)
        st.caption(f"Fiber Optic users have a **{fiber_churn*100:.1f}%** churn rate. Investigate technical support tickets for this segment.")
        
        st.markdown("**3. Payment Friction**")
        check_churn = df[df['PaymentMethod'] == 'Electronic check']['Churn'].value_counts(normalize=True).get('Yes', 0)
        st.caption(f"Users paying via Electronic Check expire at **{check_churn*100:.1f}%**. Push for Auto-Pay adoption.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 2: CHURN SIMULATOR ---
elif page == "🔮 Churn Simulator":
    st.title("Predictive Intelligence")
    st.markdown("Simulate customer scenarios to identify retention opportunities.")
    
    col_input, col_result = st.columns([1, 1])
    
    with col_input:
        st.subheader("Customer Profile")
        with st.container(border=True):
            tenure = st.slider("Tenure (Months)", 0, 72, 12)
            monthly_charges = st.slider("Monthly Charges ($)", 18.0, 118.0, 70.0)
            total_charges = st.number_input("Total Charges ($)", 0.0, 10000.0, 1000.0)
            sentiment = st.slider("Sentiment Score (-1.0 to 1.0)", -1.0, 1.0, 0.1)
            
            st.divider()
            
            contract = st.selectbox("Contract Type", df['Contract'].unique())
            internet = st.selectbox("Internet Service", df['InternetService'].unique())
            payment = st.selectbox("Payment Method", df['PaymentMethod'].unique())
            acq_cost = st.slider("Acquisition Cost ($)", 0.0, 1000.0, 200.0)
    
    # PREDICTION LOGIC
    input_data = pd.DataFrame({
        'tenure': [tenure],
        'MonthlyCharges': [monthly_charges],
        'TotalCharges': [total_charges],
        'Score_Sentiment_Dernier_Mois': [sentiment],
        'Cout_Acquisition_Client': [acq_cost],
        'SeniorCitizen': [0], 'Rentabilite_Nette_Simulee': [0] # Placeholders
    })
    
    cat_mapping = {
        'Contract': contract, 'InternetService': internet, 'PaymentMethod': payment,
        'gender': 'Male', 'Partner': 'No', 'Dependents': 'No', 'PhoneService': 'Yes',
        'MultipleLines': 'No', 'OnlineSecurity': 'No', 'OnlineBackup': 'No',
        'DeviceProtection': 'No', 'TechSupport': 'No', 'StreamingTV': 'No', 
        'StreamingMovies': 'No', 'PaperlessBilling': 'Yes'
    }
    
    # Reconstruct Layout
    template = df.drop(['Churn', 'customerID'], axis=1).iloc[0].copy()
    template['tenure'] = tenure
    template['MonthlyCharges'] = monthly_charges
    template['TotalCharges'] = total_charges
    template['Score_Sentiment_Dernier_Mois'] = sentiment
    for col, val in cat_mapping.items():
        template[col] = val
        
    input_df = pd.DataFrame([template])
    
    # Encode
    for col, le in encoders.items():
        if col in input_df.columns:
            try:
                input_df[col] = input_df[col].apply(lambda x: le.transform([x])[0] if x in le.classes_ else 0) 
            except: pass

    # Predict
    prob = model.predict_proba(input_df)[0][1]
    
    with col_result:
        st.subheader("Risk Assessment")
        
        # Risk Gauge
        fig_gauge = px.pie(values=[prob, 1-prob], names=["Risk", "Safe"], hole=0.7, 
                           color_discrete_sequence=['#FF3D00', '#424242'])
        fig_gauge.update_layout(showlegend=False, margin=dict(t=0,b=0,l=0,r=0), height=200,
                                paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        st.markdown(f"<h2 style='text-align: center; color: {'#FF3D00' if prob > 0.5 else '#00E676'};'>{prob*100:.1f}% Risk</h2>", unsafe_allow_html=True)
        
        st.markdown("### 📋 Strategic Action Plan")
        
        if prob > 0.7:
             st.error("🚨 **High Risk Alert**")
             st.markdown("""
             **Recommendation: Immediate Retention Offer**
             *   **Action:** Offer 15% discount for 6 months.
             *   **Script:** "We noticed you might be looking elsewhere. We value you..."
             *   **Priority:** 🔥 Critical
             """)
        elif prob > 0.4:
            st.warning("⚠️ **Watchlist**")
            st.markdown("""
            **Recommendation: Value Enhancement**
            *   **Action:** Offer free upgrade to higher speed tier.
            *   **Priority:** 🔸 High
            """)
        else:
            st.success("✅ **Safe Customer**")
            st.markdown("""
            **Recommendation: Upsell Opportunity**
            *   **Action:** Suggest bundling 'Device Protection'.
            *   **Priority:** 🟢 Low
            """)
            
        with st.expander("See Technical Details"):
            st.json(input_data.to_dict(orient='records')[0])

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_profitability():
    df = pd.read_csv("Telco_Churn_Enrichi_GCP.csv")
    
    # We want to show "Profitability Risk" - i.e., Average Profitability of Churned vs Retained customers
    # Or maybe "Total Profit" lost due to Churn.
    
    plt.figure(figsize=(8, 6))
    
    # Group by Churn and calculate MEAN profitability
    # (Using the French column names as identified earlier)
    # Rentabilite_Nette_Simulee is the net profitability
    
    avg_profit = df.groupby('Churn')['Rentabilite_Nette_Simulee'].mean().reset_index()
    
    sns.barplot(x='Churn', y='Rentabilite_Nette_Simulee', data=avg_profit, palette=['#4CAF50', '#F44336'])
    
    plt.title('Average Estimated Net Profitability: Churned vs Retained')
    plt.ylabel('Net Profitability ($)')
    plt.xlabel('Customer Churn Status')
    
    # Add labels
    for index, row in avg_profit.iterrows():
        plt.text(index, row.Rentabilite_Nette_Simulee, f"${row.Rentabilite_Nette_Simulee:.2f}", color='black', ha="center", va="bottom")

    plt.tight_layout()
    plt.savefig('profitability_impact.png')
    print("Saved profitability_impact.png")
    
    # Also, let's do a distribution plot to see if High Profit customers churn more?
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=df, x='Rentabilite_Nette_Simulee', hue='Churn', fill=True, common_norm=False, palette=['#4CAF50', '#F44336'])
    plt.title('Profitability Distribution by Churn Status')
    plt.xlabel('Net Profitability ($)')
    plt.savefig('profitability_distribution.png')
    print("Saved profitability_distribution.png")

if __name__ == "__main__":
    plot_profitability()

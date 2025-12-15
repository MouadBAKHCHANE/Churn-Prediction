import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys

def analyze():
    filename = "Telco_Churn_Enrichi_GCP.csv"
    report_file = "analysis_report.md"
    
    try:
        df = pd.read_csv(filename)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    with open(report_file, "w", encoding="utf-8") as f:
        f.write(f"# Analysis of {filename}\n\n")
        
        # Basic Info
        f.write("## 1. Dataset Overview\n")
        f.write(f"- **Rows:** {df.shape[0]}\n")
        f.write(f"- **Columns:** {df.shape[1]}\n\n")
        
        f.write("### Columns:\n")
        f.write(", ".join([f"`{c}`" for c in df.columns]) + "\n\n")
        
        # Missing Values
        f.write("## 2. Data Quality\n")
        missing = df.isnull().sum()
        missing = missing[missing > 0]
        if not missing.empty:
            f.write("### Missing Values:\n| Column | Missing Count | Percentage |\n|---|---|---|\n")
            for col, val in missing.items():
                pct = (val / len(df)) * 100
                f.write(f"| {col} | {val} | {pct:.2f}% |\n")
        else:
            f.write("No missing values found.\n")
        f.write("\n")
        
        # Duplicates
        dupes = df.duplicated().sum()
        f.write(f"**Duplicate Rows:** {dupes}\n\n")
        
        # Target Analysis
        target_col = None
        for col in df.columns:
            if 'churn' in col.lower():
                target_col = col
                break
        
        if target_col:
            f.write(f"## 3. Target Variable Analysis ({target_col})\n")
            val_counts = df[target_col].value_counts()
            f.write("| Value | Count | Percentage |\n|---|---|---|\n")
            for val, count in val_counts.items():
                pct = (count / len(df)) * 100
                f.write(f"| {val} | {count} | {pct:.2f}% |\n")
            f.write("\n")
            
            # Plot
            try:
                plt.figure(figsize=(6, 4))
                sns.countplot(x=target_col, data=df)
                plt.title(f'Distribution of {target_col}')
                plt.savefig('churn_distribution.png')
                plt.close()
                f.write("![Churn Distribution](churn_distribution.png)\n\n")
            except Exception as e:
                f.write(f"*(Could not generate plot: {e})*\n\n")
        
        # Numeric Summary
        f.write("## 4. Numeric Features Summary\n")
        desc = df.describe().transpose()
        # Convert to markdown table manually or use to_markdown if available (pandas > 1.0)
        try:
            f.write(desc.to_markdown())
        except:
             f.write(desc.to_string())
        f.write("\n\n")

        # Correlation
        f.write("## 5. Correlations\n")
        # Select numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
        
        # Identify non-numeric columns that might be interesting to convert (like Target)
        if target_col and target_col not in numeric_df.columns:
            # Try to encode
            try:
                df['encoded_target'] = df[target_col].factorize()[0]
                numeric_df['encoded_target'] = df['encoded_target']
            except:
                pass
        
        if not numeric_df.empty:
            corr = numeric_df.corr()
            f.write("### Top Correlations:\n")
            # Unstack and sort
            corr_pairs = corr.unstack().sort_values(ascending=False)
            # Remove self correlations (1.0) and duplicates
            corr_pairs = corr_pairs[corr_pairs < 1.0] 
            # Drop duplicates (A-B is same as B-A) - messy to do easily, so just print top 10 distinct
            
            f.write("| Feature 1 | Feature 2 | Correlation |\n|---|---|---|\n")
            seen = set()
            count = 0
            for index, value in corr_pairs.items():
                if count >= 10: break
                (a, b) = index
                if (b, a) not in seen:
                    seen.add((a, b))
                    f.write(f"| {a} | {b} | {value:.4f} |\n")
                    count += 1
            f.write("\n")
            
            try:
                plt.figure(figsize=(10, 8))
                sns.heatmap(corr, annot=False, cmap='coolwarm')
                plt.title('Correlation Matrix')
                plt.tight_layout()
                plt.savefig('correlation_matrix.png')
                plt.close()
                f.write("![Correlation Matrix](correlation_matrix.png)\n\n")
            except Exception as e:
                 f.write(f"*(Could not generate heatmap: {e})*\n")
        
    print(f"Analysis complete. Report saved to {report_file}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        print(f"Fatal error: {e}")

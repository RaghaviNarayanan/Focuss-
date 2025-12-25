import pandas as pd
import yagmail
from pathlib import Path
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def run_summary_email():
    # 🔁 Load CSV
    file_path = Path(r"D:\vscode\Focus_extension\url_log.csv")
    df = pd.read_csv(file_path)

    if df.empty:
        print("No browsing data to summarize.")
        return

    # =========================
    # 🔹 DATA PREPROCESSING
    # =========================

    # Handle missing values
    df.dropna(inplace=True)

    # Encode target labels
    label_encoder = LabelEncoder()
    df['category_encoded'] = label_encoder.fit_transform(df['category'])

    # Feature selection
    X = df[['time_spent']]  # feature
    y = df['category_encoded']  # label

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

   

    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=5,
        random_state=42
    )

    rf_model.fit(X_train, y_train)

    # Predict categories
    df['predicted_category'] = label_encoder.inverse_transform(
        rf_model.predict(X)
    )

 

    counts = df['predicted_category'].value_counts()
    productive = counts.get('Productive', 0)
    distracting = counts.get('Distracting', 0)
    neutral = counts.get('Neutral', 0)
    total = len(df)

    summary = f"""
📊 Focus Daily Report (ML Enhanced)

Total Sites Visited: {total}
✅ Productive: {productive}
❌ Distracting: {distracting}
➖ Neutral: {neutral}

📈 Insights generated using Random Forest classification.
Keep improving your focus! 💪
"""

   

    APP_PASSWORD = "cbhghlznjkdfwumb"  # move to env variable in real use

    try:
        yag = yagmail.SMTP("raghavinarayanan2005@gmail.com", APP_PASSWORD)
        yag.send(
            to="raghavinarayanan2005@gmail.com",
            subject="📈 Focus – Daily Browsing Summary (ML Powered)",
            contents=[summary]
        )
        print("✅ Summary Email Sent")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return


    df.iloc[0:0].to_csv(file_path, index=False)
    print("🧹 CSV Cleared")

if __name__ == "__main__":
    run_summary_email()

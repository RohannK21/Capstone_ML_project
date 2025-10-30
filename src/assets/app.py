from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
from extractor import extract_website_features
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)
CORS(app)  # ✅ allow requests from frontend

# Load model and preprocessing assets
X_columns = joblib.load("X_columns.pkl")
scaler = joblib.load("scaler.pkl")
model = joblib.load("website_classifier.pkl")


def extract_features_for_prediction(url):
    """Extract features from a URL and prepare dataframe for prediction"""
    features = extract_website_features(url, labels={"secure_label": 1})
    df_features = pd.DataFrame([features])

    # One-hot encode categorical columns
    df_features = pd.get_dummies(df_features, columns=["ssl_issuer", "organization_name", "tld_type"])

    # Align columns with training features
    for col in X_columns:
        if col not in df_features.columns:
            df_features[col] = 0

    df_features = df_features[X_columns]
    return df_features


@app.route('/predict', methods=['POST'])
def predict_website():
    data = request.get_json()
    url = data.get("url", "")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    df_features = extract_features_for_prediction(url)
    df_scaled = scaler.transform(df_features)
    pred = model.predict(df_scaled)[0]
    prob = model.predict_proba(df_scaled)[0][pred]

    result = {
        "url": url,
        "prediction": "SAFE" if pred == 1 else "MALICIOUS",
        "confidence": round(prob * 100, 2)
    }
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)

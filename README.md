Phishing URL Detection & Risk Assessment Platform

A machine learning–powered platform that analyzes URLs to detect phishing attempts and assess their risk level, combining a trained XGBoost classifier with real-time threat intelligence from VirusTotal and Google Safe Browsing.

Features


ML-based phishing detection — classifies URLs as legitimate or phishing using a trained model.
URL feature extraction — parses structural, lexical, and domain-based features from raw URLs (e.g. URL length, use of IP address, special characters, subdomain count, HTTPS usage).
XGBoost classification — gradient-boosted decision tree model for high-accuracy predictions.
VirusTotal integration — cross-checks URLs against VirusTotal's multi-engine scan results.
Google Safe Browsing integration — verifies URLs against Google's known threat lists.
Risk scoring — combines model output and threat-intel signals into a single, interpretable risk score.


Tech Stack

ComponentTechnologyLanguagePythonWeb FrameworkFlaskML / ModelingScikit-learn, XGBoostData ProcessingPandasThreat IntelligenceVirusTotal API, Google Safe Browsing API

Adjust the structure above to match your actual repository layout.



Getting Started

Prerequisites


Python 3.9+
API keys for VirusTotal and Google Safe Browsing


Installation

bashgit clone <repo-url>
cd phishing-url-detection

python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

pip install -r requirements.txt

Configuration

Create a .env file in the project root with your API credentials:

VIRUSTOTAL_API_KEY=your_virustotal_api_key
GOOGLE_SAFE_BROWSING_API_KEY=your_google_api_key


Never commit your .env file or API keys to version control.



Dataset

Datasets are not included in this repository due to size limitations. To run the project, download a phishing/legitimate URL dataset (e.g. from PhishTank or UCI ML Repository) and place it in the data/ folder, matching the format expected by Train_model.ipynb.

Training the Model

Run the notebook to train and export the classifier:

bashjupyter notebook Train_model.ipynb

This will generate the trained model artifact used by the Flask app at runtime (e.g. models/xgboost_model.pkl).

Running the App

bashpython app.py

By default the app runs at http://localhost:5000. Submit a URL through the web interface or API endpoint to receive a phishing prediction and risk score.

How It Works


Feature extraction — the input URL is parsed into a set of numerical/categorical features.
ML prediction — the XGBoost model outputs a phishing probability based on those features.
Threat intelligence lookup — the URL is checked against VirusTotal and Google Safe Browsing in parallel.
Risk scoring — the ML prediction and threat-intel results are combined into a final risk score and verdict (e.g. Safe / Suspicious / Malicious).


Roadmap


 Add browser extension for real-time URL checking
 Support batch URL scanning via CSV upload
 Add model explainability (e.g. SHAP values) to risk reports
 Dockerize the application for easier deployment


Contributing

Contributions are welcome. Please open an issue to discuss significant changes before submitting a pull request.

License

2026 - (c) Nguyen Huy Hai Minh

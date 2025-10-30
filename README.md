🛡️ Website Security Classifier

A Python-based Machine Learning project that classifies websites as SAFE or MALICIOUS using domain, SSL, WHOIS, and HTML-based features.
Built with a Random Forest model, it enables both dataset generation and real-time prediction through a React-based web interface.

⚙️ Features :
-🌐 HTTPS & SSL validation
-🕒 Domain age and WHOIS details
-🧩 URL structure & TLD analysis
-🧠 HTML elements (iframes, forms, external links)
-🔑 Keyword detection (login, privacy policy, contact)
-🧾 Security headers: HSTS, CSP, X-Frame-Options, CSP, etc.

Target column: secure_label
1 → SAFE
0 → MALICIOUS

📊 Dataset
1000 total websites (500 safe + 500 malicious)
Safe sites from top-ranked domains i.e. Alexa-top-1m.csv from Kaggle 
Malicious sites from phishing/malware datasets from Kaggle 
Each website was scraped and analyzed to extract real-time SSL, WHOIS, and HTML features

🔧 Data Generation Workflow
extractor.py → Extracts security features from a single website
scrappy.py → Uses extractor.py + urls_to_scan.txt to scrape multiple sites and create website_security_dataset.csv

🧰 Installation
Install required dependencies:
pip install flask flask-cors pandas tqdm joblib requests beautifulsoup4 python-whois scikit-learn

If python-whois fails:
pip install whois

🚀 How to Run
You can either:

🧪 Option 1 — Run the Notebook
Open and execute the .ipynb file to train or test the model directly in Jupyter Notebook / Google Colab.

💻 Option 2 — Run the Web App
Start the Flask backend (app.py)
Open the React frontend and run:
npm install
npm run dev

Enter a URL to check if it’s SAFE or MALICIOUS in real time.
🌐 Example URLs
Safe: google.com, wikipedia.org, github.com
Malicious: fakebank-login.com, phishingsite-example.com, maliciousexample.com

# If you liked this project, a star on this GitHub repo would be appreciated :)

🛡️ Website Security Classifier

A Python-based Machine Learning project that classifies websites as SAFE or MALICIOUS using domain, SSL, WHOIS, and HTML-based features.
Built with a Random Forest model, this tool enables easy testing and dataset generation for any URL.

⚙️ Features
🌐 HTTPS & SSL validation
🕒 Domain age and WHOIS details
🧩 URL structure & TLD analysis
🧠 HTML elements (iframes, forms, external links)
🔑 Keyword detection (login, privacy policy, contact)
🧾 Security headers: HSTS, CSP, X-Frame-Options, etc.

Target column: secure_label
1 → SAFE
0 → MALICIOUS

📊 Dataset
1000 total websites (500 ✅ safe + 500 ❌ malicious)
Safe sites were taken from top-ranked domains
Malicious ones came from phishing/malware datasets
Each of the 500 websites was scraped and analyzed to extract live SSL, WHOIS, and HTML features

🔧 How Data is Generated
extractor.py → Extracts security features from a single website
scrappy.py → Uses extractor.py + urls_to_scan.txt (list of sites) to automatically scrape multiple websites and generate a dataset file (website_security_dataset.csv)

🧰 Installation
Install all required packages:
pip install flask flask-cors pandas tqdm joblib requests beautifulsoup4 python-whois scikit-learn

If python-whois fails:
pip install whois

🚀 Usage
Train and test the Random Forest classifier
Predict whether a given URL is safe or malicious
View model confidence and accuracy metrics

🌐 Example URLs

Safe: google.com, wikipedia.org, github.com
Malicious: fakebank-login.com, phishingsite-example.com

⭐ If you liked this project, a star on GitHub would be appreciated!

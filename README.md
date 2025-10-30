# Website Security Classifier

A Python-based Machine Learning project to classify websites as SAFE or MALICIOUS using domain, SSL, WHOIS, and HTML features. Built with a Random Forest model and designed for easy testing of any URL.

---

## Features

The classifier uses the following features for each website:

* HTTPS presence
* SSL validity and expiry
* Domain age and WHOIS information
* URL structure details
* Top-level domain type
* HTML elements such as iframes, forms, and external links
* Presence of login, privacy policy, and contact keywords
* Number of suspicious keywords in content
* Security headers like HSTS, X-Frame-Options, CSP, and X-Content-Type-Options

The target column is `secure_label`:

* 1 → SAFE
* 0 → MALICIOUS

---

## Dataset

* Contains features for 1000 websites (500 safe + 500 malicious)
* Safe websites are collected from top-ranked sites, and malicious websites are collected from phishing/malicious datasets

---

## Installation

* Install required Python packages such as pandas, scikit-learn, joblib, requests, BeautifulSoup, python-whois, tldextract, and tqdm
* The project can be run locally or on Google Colab

---

## Usage

The project allows users to:

* Train a Random Forest model on the dataset
* Evaluate the model’s accuracy and performance
* Predict whether a given URL is safe or malicious
* View the model’s confidence in its predictions

---

## Example Websites to Test

**SAFE websites:**

* google.com
* wikipedia.org
* github.com

**MALICIOUS / PHISHING websites:**

* fakebank-login.com
* phishingsite-example.com

---

If you liked this idea, upvotes will be appreciated :)
======

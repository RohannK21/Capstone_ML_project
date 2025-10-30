<<<<<<< HEAD
# Website Security Classifier

A Python-based machine learning project to classify websites as SAFE or MALICIOUS using domain, SSL, WHOIS, and HTML features. Built with a Random Forest model and designed for easy testing of any URL.

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
=======
# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
>>>>>>> 3e91093 (Initial commit of React app)

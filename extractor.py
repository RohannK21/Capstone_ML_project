import requests
import ssl
import socket
import whois
import re
import time
import logging
from datetime import datetime, timezone
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

# ---------------- Setup ---------------- #
logging.basicConfig(filename='errors.log', level=logging.ERROR)
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})  # Reuse session to speed up requests


# ---------------- Feature extraction functions ---------------- #

# --- Security Features --- #
def get_ssl_info(domain, url):
    if not url.startswith('https'):
        return {"has_https": 0, "ssl_valid": 0, "ssl_expiry_days": 0, "ssl_issuer": ""}

    try:
        context = ssl.create_default_context()
        conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=domain)
        conn.settimeout(5)
        conn.connect((domain, 443))
        cert = conn.getpeercert()
        conn.close()

        not_after = cert.get('notAfter')
        ssl_expiry_days = 0
        if not_after:
            expiry_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z').replace(tzinfo=timezone.utc)
            ssl_expiry_days = (expiry_date - datetime.now(timezone.utc)).days

        issuer = ""
        try:
            issuer = dict(x[0] for x in cert.get('issuer', ())).get('organizationName', '') or ""
        except Exception:
            issuer = ""

        return {
            "has_https": 1,
            "ssl_valid": 1,
            "ssl_expiry_days": ssl_expiry_days,
            "ssl_issuer": issuer
        }
    except Exception:
        return {"has_https": 0, "ssl_valid": 0, "ssl_expiry_days": 0, "ssl_issuer": ""}


def get_security_headers(url):
    try:
        r = session.get(url, timeout=5, allow_redirects=True)
        headers = r.headers
        return {
            "has_hsts_header": int("Strict-Transport-Security" in headers),
            "has_x_frame_options": int("X-Frame-Options" in headers),
            "has_csp": int("Content-Security-Policy" in headers),
            "has_x_content_type_options": int("X-Content-Type-Options" in headers)
        }
    except Exception:
        return {"has_hsts_header": 0, "has_x_frame_options": 0, "has_csp": 0, "has_x_content_type_options": 0}


# --- Trustworthiness Features --- #
def get_domain_info(domain):
    try:
        w = whois.whois(domain)
        creation = w.creation_date

        if isinstance(creation, list):
            creation = creation[0]
        if isinstance(creation, str):
            try:
                creation = datetime.strptime(creation, "%Y-%m-%d")
            except Exception:
                creation = None

        domain_age_days = 0
        whois_available = 0
        if creation:
            if creation.tzinfo is None:
                creation = creation.replace(tzinfo=timezone.utc)
            else:
                creation = creation.astimezone(timezone.utc)
            domain_age_days = (datetime.now(timezone.utc) - creation).days
            whois_available = 1

        org_name = ""
        try:
            if isinstance(w, dict):
                org_name = w.get('org') or w.get('organization') or ""
            else:
                org_name = getattr(w, 'org', None) or getattr(w, 'organization', None) or ""
        except Exception:
            org_name = ""

        return {
            "domain_age_days": domain_age_days,
            "whois_info_available": whois_available,
            "organization_name": org_name or ""
        }
    except Exception:
        return {"domain_age_days": 0, "whois_info_available": 0, "organization_name": ''}


# --- URL Features (security + trust hints) --- #
def get_url_features(url):
    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path
    has_ip = int(bool(re.match(r'(\d{1,3}\.){3}\d{1,3}', domain)))
    tld = parsed.netloc.split('.')[-1] if '.' in parsed.netloc else 'unknown'

    return {
        "url_length": len(url),
        "num_dots": url.count('.'),
        "num_hyphens": url.count('-'),
        "has_ip_in_url": has_ip,
        "num_special_chars": sum(url.count(c) for c in ['@', '?', '=', '%', '&']),
        "tld_type": tld
    }


# --- Malicious / Content Features --- #
def get_content_features(url):
    try:
        r = session.get(url, timeout=5, verify=True, allow_redirects=True)
        soup = BeautifulSoup(r.text, 'html.parser')

        num_iframes = len(soup.find_all('iframe'))
        num_forms = len(soup.find_all('form'))
        external_links = [a for a in soup.find_all('a', href=True) if urlparse(a['href']).netloc and urlparse(a['href']).netloc != urlparse(url).netloc]
        num_external_links = len(external_links)
        text_lower = r.text.lower()

        suspicious_keywords = ["malware", "phishing", "click here", "free money", "adult", "xxx"]
        num_suspicious_keywords = sum(text_lower.count(word) for word in suspicious_keywords)

        has_login_keyword = int(any(word in text_lower for word in ["login", "signin", "account"]))
        has_privacy_policy = int("privacy" in text_lower)
        has_contact_page = int("contact" in text_lower)

        return {
            "num_iframes": num_iframes,
            "num_forms": num_forms,
            "num_external_links": num_external_links,
            "has_login_keyword": has_login_keyword,
            "has_privacy_policy": has_privacy_policy,
            "has_contact_page": has_contact_page,
            "num_suspicious_keywords": num_suspicious_keywords
        }
    except Exception:
        return {
            "num_iframes": 0,
            "num_forms": 0,
            "num_external_links": 0,
            "has_login_keyword": 0,
            "has_privacy_policy": 0,
            "has_contact_page": 0,
            "num_suspicious_keywords": 0
        }


# --- Combine all features --- #
def extract_website_features(url, labels=None):
    if not url.startswith('http'):
        url = 'https://' + url
    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path

    features = {"Website": url}
    features.update(get_ssl_info(domain, url))          # Security
    features.update(get_domain_info(domain))           # Trust
    features.update(get_url_features(url))             # Security + Trust hints
    features.update(get_content_features(url))         # Malicious / Content
    features.update(get_security_headers(url))         # Security headers

    # Optional multi-labels for ML if known
    if labels:
        features.update(labels)

    return features


# ---------------- Main execution ---------------- #
if __name__ == "__main__":
    input_csv = "top_sites.csv"    # CSV without header, first column: rank, second: website
    output_csv = "website_features_full.csv"

    df_urls = pd.read_csv(input_csv, header=None, names=["Website"])
    website_list = df_urls['Website'].tolist()[:400]

    all_features = []
    for url in tqdm(website_list, desc="Extracting features"):
        try:
            features = extract_website_features(url)
            all_features.append(features)
        except Exception as e:
            logging.error(f"Error for {url}: {e}")
        time.sleep(0.5) 

    df_features = pd.DataFrame(all_features)
    df_features.to_csv(output_csv, index=False)
    print(f"\n✅ Feature CSV saved at '{output_csv}' with {len(df_features)} websites.")

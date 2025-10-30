import os
import time
import pandas as pd
from tqdm import tqdm
from extractor import extract_website_features 
import logging

# ---------------- Setup ---------------- #
logging.basicConfig(filename='dataset_errors.log', level=logging.ERROR)
INPUT_FILE = "urls_to_scan.txt"
OUTPUT_FILE = "website_security_dataset.csv"
CACHE_SAVE_EVERY = 10   # save every 10 sites
DELAY = 0.5             # polite delay (avoid bans)

# ---------------- Helper functions ---------------- #
def load_urls_with_labels(file_path):
    """Load 1000 URLs and assign labels:
       1 = Secure (Alexa)
       0 = Insecure/Malicious (Phish)"""
    with open(file_path, "r", encoding="utf8") as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]
    if len(urls) < 1000:
        print(f"⚠️ Only {len(urls)} URLs found. Proceeding anyway.")
    labels = [1 if i < 500 else 0 for i in range(len(urls))]  # first 500 Alexa, next 500 Phish
    return list(zip(urls, labels))

def save_partial(df, output_file):
    """Save dataset safely (append or create)."""
    if os.path.exists(output_file):
        df_existing = pd.read_csv(output_file)
        df_combined = pd.concat([df_existing, df]).drop_duplicates(subset=["Website"], keep="last")
        df_combined.to_csv(output_file, index=False)
    else:
        df.to_csv(output_file, index=False)

# ---------------- Main ---------------- #
if __name__ == "__main__":
    urls_labels = load_urls_with_labels(INPUT_FILE)
    print(f"🌐 Loaded {len(urls_labels)} URLs (500 secure + 500 malicious)")

    # Resume support: skip already collected
    done_urls = set()
    if os.path.exists(OUTPUT_FILE):
        done_df = pd.read_csv(OUTPUT_FILE)
        done_urls = set(done_df["Website"].tolist())
        print(f"🔁 Resuming from {len(done_urls)} already processed URLs")

    all_features = []
    for i, (url, label) in enumerate(tqdm(urls_labels, desc="Collecting dataset")):
        if url in done_urls:
            continue
        try:
            features = extract_website_features(url, labels={"secure_label": label})
            all_features.append(features)
        except Exception as e:
            logging.error(f"Error processing {url}: {e}")
        time.sleep(DELAY)

        # periodic save
        if len(all_features) % CACHE_SAVE_EVERY == 0 and all_features:
            temp_df = pd.DataFrame(all_features)
            save_partial(temp_df, OUTPUT_FILE)
            all_features.clear()

    # Final save
    if all_features:
        final_df = pd.DataFrame(all_features)
        save_partial(final_df, OUTPUT_FILE)

    print(f"\n✅ Dataset successfully built and saved as '{OUTPUT_FILE}'.")

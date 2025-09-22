import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("EXPLORIUM_API_KEY")
BASE_URL = "https://api.explorium.ai/v1/integrations/explore"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def fetch_all_features(urls: list[str]) -> pd.DataFrame:
    records = []
    for url in urls:
        try:
            payload = {"url": url}
            r = requests.post(BASE_URL, headers=HEADERS, json=payload, timeout=30)
            r.raise_for_status()
            features = r.json().get("features", {})
            records.append({"company_url": url, **features})
        except Exception:
            records.append({"company_url": url})
    return pd.DataFrame(records)

if __name__ == "__main__":
    from sequoia_scraper import get_companies_df
    df = get_companies_df()
    print(fetch_all_features(df["company_url"].tolist()).head())

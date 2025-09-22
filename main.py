import os
import pandas as pd
from sequoia_scraper import get_companies_df
from explorium_client import fetch_all_features
from deepseek_enrichment import enrich_df

def save(df: pd.DataFrame, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved {path}")

def main():
    # 1. Scrape Sequoia portfolio
    companies = get_companies_df().head(20)  # only first 20 companies
    save(companies, "data/raw/companies")

    # 2. Explorium enrichment for 20 companies
    features = fetch_all_features(companies["company_url"].tolist())
    save(features, "data/raw/explorium_features")

    # 3. DeepSeek analysis for 20 companies
    enriched = enrich_df(features)
    save(enriched, "data/enriched/final_analysis")

    print("Pipeline complete for 20 companies.")

if __name__ == "__main__":
    main()

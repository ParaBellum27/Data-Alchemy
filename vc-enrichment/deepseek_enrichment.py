import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("DEEPSEEK_API_KEY")
URL = "https://api.deepseek.com/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

def call_deepseek(prompt: str) -> str:
    payload = {"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}], "max_tokens": 500, "temperature": 0.2}
    for i in range(3):
        try:
            r = requests.post(URL, headers=HEADERS, json=payload, timeout=30)
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"].strip()
        except Exception:
            time.sleep(2 ** i)
    return "ERROR"

def enrich_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["category"] = ""
    df["rank_score"] = ""
    df["insights"] = ""
    for idx, row in df.iterrows():
        feats = {k: v for k, v in row.items() if k != "company_url"}
        text = "\n".join(f"{k}: {v}" for k, v in feats.items())
        df.at[idx, "category"] = call_deepseek(f"Classify industry:\n\n{text}")
        df.at[idx, "rank_score"] = call_deepseek(f"Rank 1–10 growth potential:\n\n{text}")
        df.at[idx, "insights"] = call_deepseek(f"Provide 2–3 insights:\n\n{text}")
        time.sleep(1)
    return df

if __name__ == "__main__":
    sample = pd.DataFrame([{"company_url": "https://example.com", "feature1": 1}])
    print(enrich_df(sample))

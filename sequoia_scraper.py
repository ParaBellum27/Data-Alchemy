import requests
import xml.etree.ElementTree as ET
import pandas as pd

SITEMAP_URL = "https://www.sequoiacap.com/company-sitemap.xml"
HEADERS = {"User-Agent": "DataAlchemyBot/1.0"}

def get_companies_df() -> pd.DataFrame:
    resp = requests.get(SITEMAP_URL, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    urls = [
        elem.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text
        for elem in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}url")
    ]
    names = [url.rstrip("/").split("/")[-1].replace("-", " ").title() for url in urls]
    return pd.DataFrame({"company_name": names, "company_url": urls})

if __name__ == "__main__":
    print(get_companies_df().head())

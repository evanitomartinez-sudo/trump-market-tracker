import re
import requests
from bs4 import BeautifulSoup
from config import TRUTH_BASE_URL, TRUTH_ACCOUNT_ID, POLL_LIMIT

def clean_html(html):
    return BeautifulSoup(html or "", "html.parser").get_text(" ", strip=True)

def fetch_posts():
    url = f"{TRUTH_BASE_URL}/api/v1/accounts/{TRUTH_ACCOUNT_ID}/statuses"
    r = requests.get(
        url,
        params={"limit": POLL_LIMIT},
        headers={"User-Agent": "TrumpMarketTracker/1.0"},
        timeout=20,
    )
    r.raise_for_status()
    return r.json()

def normalize(post):
    text = clean_html(post.get("content", ""))
    tickers = sorted(set(re.findall(r"\$([A-Z]{1,5})\b", text.upper())))
    return {
        "id": str(post["id"]),
        "created_at": post.get("created_at"),
        "url": post.get("url") or f"{TRUTH_BASE_URL}/@realDonaldTrump",
        "text": text,
        "tickers": tickers,
    }

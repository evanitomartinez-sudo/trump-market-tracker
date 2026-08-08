import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup


FEED_URL = "https://www.trumpstruth.org/feed"


def clean_html(html):
    return BeautifulSoup(html or "", "html.parser").get_text(
        " ",
        strip=True
    )


def fetch_posts():
    response = requests.get(
        FEED_URL,
        headers={
            "User-Agent": "Mozilla/5.0 TrumpMarketTracker/1.0"
        },
        timeout=20,
    )

    response.raise_for_status()

    root = ET.fromstring(response.content)

    posts = []

    for item in root.findall(".//item"):
        title = item.findtext("title") or ""
        description = item.findtext("description") or ""
        link = item.findtext("link") or ""
        pub_date = item.findtext("pubDate") or ""
        guid = item.findtext("guid") or link

        text = clean_html(description)

        if not text:
            text = clean_html(title)

        posts.append({
            "id": guid,
            "created_at": pub_date,
            "url": link,
            "content": text,
        })

    return posts


def normalize(post):
    import re

    text = clean_html(post.get("content", ""))

    tickers = sorted(
        set(
            re.findall(
                r"\$([A-Z]{1,5})\b",
                text.upper()
            )
        )
    )

    return {
        "id": str(post["id"]),
        "created_at": post.get("created_at"),
        "url": post.get("url"),
        "text": text,
        "tickers": tickers,
    }

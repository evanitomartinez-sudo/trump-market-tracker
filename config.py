import os
from dotenv import load_dotenv

load_dotenv()

TRUTH_BASE_URL = os.getenv(
    "TRUTH_BASE_URL",
    "https://truthsocial.com"
).rstrip("/")

TRUTH_ACCOUNT_ID = os.getenv(
    "TRUTH_ACCOUNT_ID",
    "107780257626128497"
)

POLL_LIMIT = int(os.getenv("POLL_LIMIT", "20"))
MIN_SCORE = int(os.getenv("MIN_SCORE", "3"))

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK", "")

WATCHLIST = {
    "NVDA",
    "AMD",
    "INTC",
    "MU",
    "AVGO",
    "TSM",
    "PLTR",
    "AAPL",
    "MSFT",
    "GOOGL",
    "AMZN",
    "META",
    "TSLA",
    "VST",
    "XOM",
    "CVX",
    "LMT",
    "RTX",
    "BA",
    "DJT",
}

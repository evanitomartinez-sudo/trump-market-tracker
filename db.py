import sqlite3
from pathlib import Path

DB_PATH = Path("data/tracker.db")
DB_PATH.parent.mkdir(exist_ok=True)


def connect():
    con = sqlite3.connect(DB_PATH)

    con.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            created_at TEXT,
            url TEXT,
            text TEXT,
            score INTEGER,
            tickers TEXT,
            alerted INTEGER DEFAULT 0
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id TEXT PRIMARY KEY,
            trade_date TEXT,
            disclosure_date TEXT,
            issuer TEXT,
            ticker TEXT,
            transaction_type TEXT,
            amount_range TEXT,
            source_url TEXT
        )
    """)

    con.commit()
    return con


def post_seen(post_id):
    con = connect()

    row = con.execute(
        "SELECT 1 FROM posts WHERE id=?",
        (post_id,)
    ).fetchone()

    con.close()

    return row is not None


def save_post(post):
    con = connect()

    con.execute("""
        INSERT OR IGNORE INTO posts
        (id, created_at, url, text, score, tickers, alerted)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        post["id"],
        post.get("created_at"),
        post.get("url"),
        post.get("text"),
        post.get("score", 0),
        ",".join(post.get("tickers", [])),
        int(post.get("alerted", False))
    ))

    con.commit()
    con.close()


def save_trade(trade):
    con = connect()

    con.execute("""
        INSERT OR IGNORE INTO trades
        (
            id,
            trade_date,
            disclosure_date,
            issuer,
            ticker,
            transaction_type,
            amount_range,
            source_url
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        trade["id"],
        trade.get("trade_date"),
        trade.get("disclosure_date"),
        trade.get("issuer"),
        trade.get("ticker"),
        trade.get("transaction_type"),
        trade.get("amount_range"),
        trade.get("source_url")
    ))

    con.commit()
    con.close()

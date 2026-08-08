from truth import fetch_posts, normalize
from scoring import score_post
from db import post_seen, save_post
from alerts import broadcast
from config import MIN_SCORE
from market_analysis import analyze_markets, format_market_analysis


def format_alert(post, score, reasons, watched):
    level = (
        "🔴 CRITICAL"
        if score >= 8
        else "🟠 HIGH"
        if score >= 6
        else "🟡 MEDIUM"
    )

    tickers = (
        ", ".join(f"${x}" for x in post["tickers"])
        or "aucun"
    )

    watched_text = (
        ", ".join(f"${x}" for x in watched)
        or "aucun"
    )

    market_results = analyze_markets(post["text"])
    market_view = format_market_analysis(market_results)

    return (
        f"{level} — TRUMP MARKET ALERT\n\n"
        f"🕐 {post.get('created_at') or 'date inconnue'}\n\n"
        f"{post['text']}\n\n"
        f"📊 Impact score: {score}/10\n"
        f"🎯 Tickers détectés: {tickers}\n"
        f"👀 Watchlist: {watched_text}\n"
        f"🧠 Raisons: {', '.join(reasons) if reasons else '—'}\n"
        f"\n📌 Market view:\n"
        f"{market_view}\n"
        f"\n🔗 {post['url']}"
    )


def main():
    posts = fetch_posts()

    for raw in reversed(posts):
        post = normalize(raw)

        if post_seen(post["id"]):
            continue

        score, reasons, watched = score_post(
            post["text"],
            post["tickers"]
        )

        post["score"] = score
        post["alerted"] = score >= MIN_SCORE

        if score >= MIN_SCORE:
            message = format_alert(
                post,
                score,
                reasons,
                watched
            )

            broadcast(message)

        save_post(post)


if __name__ == "__main__":
    main()

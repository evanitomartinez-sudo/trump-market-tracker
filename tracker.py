from truth import fetch_posts, normalize
from scoring import score_post
from db import post_seen, save_post
from alerts import broadcast
from config import MIN_SCORE


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

    return (
        f"{level} — TRUMP MARKET ALERT\n\n"
        f"🕐 {post.get('created_at') or 'date inconnue'}\n\n"
        f"{post['text']}\n\n"
        f"📊 Impact score: {score}/10\n"
        f"🎯 Tickers détectés: {tickers}\n"
        f"👀 Watchlist: {watched_text}\n"
        f"🧠 Raisons: {', '.join(reasons) if reasons else '—'}\n\n"
        f"🔗 {post['url']}"
    )


def main():

    # TEST TEMPORAIRE TELEGRAM
    broadcast("✅ Trump Market Tracker opérationnel")

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

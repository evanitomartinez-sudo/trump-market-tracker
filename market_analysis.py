def analyze_markets(text):
    text = text.lower()

    results = {
        "XAUUSD": {"score": 0, "reasons": []},
        "USD": {"score": 0, "reasons": []},
        "NASDAQ": {"score": 0, "reasons": []},
        "SP500": {"score": 0, "reasons": []},
        "OIL": {"score": 0, "reasons": []},
        "BITCOIN": {"score": 0, "reasons": []},
    }

    # --- GEOPOLITICAL RISK ---

    geopolitical = [
        "iran",
        "war",
        "attack",
        "military",
        "missile",
        "sanctions",
        "nuclear",
        "conflict",
        "russia",
        "ukraine",
    ]

    if any(word in text for word in geopolitical):

        results["XAUUSD"]["score"] += 3
        results["XAUUSD"]["reasons"].append(
            "geopolitical risk"
        )

        results["OIL"]["score"] += 2
        results["OIL"]["reasons"].append(
            "geopolitical supply risk"
        )

        results["NASDAQ"]["score"] -= 2
        results["NASDAQ"]["reasons"].append(
            "risk-off"
        )

        results["SP500"]["score"] -= 2
        results["SP500"]["reasons"].append(
            "risk-off"
        )

    # --- TARIFFS / TRADE WAR ---

    trade_words = [
        "tariff",
        "tariffs",
        "trade war",
        "china",
        "duties",
    ]

    if any(word in text for word in trade_words):

        results["XAUUSD"]["score"] += 2
        results["XAUUSD"]["reasons"].append(
            "trade uncertainty"
        )

        results["NASDAQ"]["score"] -= 2
        results["NASDAQ"]["reasons"].append(
            "tariff risk"
        )

        results["SP500"]["score"] -= 1
        results["SP500"]["reasons"].append(
            "trade uncertainty"
        )

    # --- FED / RATES ---

    dovish = [
        "lower rates",
        "cut rates",
        "rate cut",
        "rates are too high",
        "powell should cut",
    ]

    if any(word in text for word in dovish):

        results["XAUUSD"]["score"] += 3
        results["XAUUSD"]["reasons"].append(
            "lower-rate expectations"
        )

        results["USD"]["score"] -= 3
        results["USD"]["reasons"].append(
            "lower-rate expectations"
        )

        results["NASDAQ"]["score"] += 2
        results["NASDAQ"]["reasons"].append(
            "lower-rate expectations"
        )

        results["SP500"]["score"] += 2
        results["SP500"]["reasons"].append(
            "lower-rate expectations"
        )

    # --- OIL ---

    if "oil" in text or "opec" in text:

        results["OIL"]["score"] += 3
        results["OIL"]["reasons"].append(
            "direct oil reference"
        )

    # --- CRYPTO ---

    crypto_positive = [
        "bitcoin",
        "crypto",
        "digital asset",
        "strategic bitcoin reserve",
    ]

    if any(word in text for word in crypto_positive):

        results["BITCOIN"]["score"] += 3
        results["BITCOIN"]["reasons"].append(
            "crypto policy/reference"
        )

    return results


def direction(score):

    if score >= 3:
        return "🟢 BULLISH"

    if score >= 1:
        return "🟢 Slightly bullish"

    if score <= -3:
        return "🔴 BEARISH"

    if score <= -1:
        return "🔴 Slightly bearish"

    return "⚪ NEUTRAL"


def format_market_analysis(results):

    lines = []

    important_markets = [
        "XAUUSD",
        "USD",
        "NASDAQ",
        "SP500",
        "OIL",
        "BITCOIN",
    ]

    for market in important_markets:

        data = results[market]

        if data["score"] == 0:
            continue

        reasons = ", ".join(data["reasons"])

        lines.append(
            f"{market}: "
            f"{direction(data['score'])} "
            f"({reasons})"
        )

    if not lines:
        return "⚪ Aucun impact macro évident détecté."

    return "\n".join(lines)

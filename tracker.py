from alerts import broadcast
from market_analysis import analyze_markets, format_market_analysis


def main():

    test_post = (
        "Iran must immediately stop its actions. "
        "New sanctions will be announced and oil markets "
        "must remain stable. The Fed should cut rates."
    )

    results = analyze_markets(test_post)
    market_view = format_market_analysis(results)

    message = (
        "🧪 TEST — TRUMP MARKET ALERT\n\n"
        f"{test_post}\n\n"
        "📌 Market view:\n"
        f"{market_view}\n\n"
        "⚠️ Message de test uniquement."
    )

    broadcast(message)


if __name__ == "__main__":
    main()

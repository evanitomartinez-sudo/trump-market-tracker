from config import WATCHLIST

KEYWORDS = {
    "tariff": 5, "tariffs": 5, "china": 4, "iran": 5,
    "sanctions": 5, "war": 5, "oil": 4, "energy": 3,
    "fed": 4, "interest rate": 4, "rates": 3,
    "semiconductor": 4, "chips": 3, "bitcoin": 4,
    "crypto": 4, "defense": 3, "nato": 3, "trade": 3,
    "intel": 4, "nvidia": 4, "micron": 4, "palantir": 4,
}

def score_post(text, tickers):
    low = text.lower()
    score = 0
    reasons = []

    for word, pts in KEYWORDS.items():
        if word in low:
            score += pts
            reasons.append(word)

    watched = sorted(set(tickers) & WATCHLIST)
    score += 2 * len(watched)
    score = min(score, 10)

    return score, reasons, watched

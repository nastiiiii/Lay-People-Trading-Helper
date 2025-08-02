import random

def generate_news(shock_frequency: str) -> tuple[str, str]:
    base = {
        "low": 0.05,
        "medium": 0.15,
        "high": 0.3
    }.get(shock_frequency, 0.15)

    roll = random.random()
    if roll < base:
        sentiment = random.choice(["fear", "greed"])
        headline = random.choice([
            "Market falls amid fears of recession.",
            "Investors panic after inflation data release.",
            "Economy shows strong growth signs.",
            "Tech stocks rally after earnings reports.",
            "Federal Reserve hints at interest rate cuts."
        ])
        return sentiment, headline

    return "neutral", "No major financial news today."

from services.agents.base_agent import BaseAgent
from services.finbert_cust_sandbox import analyze_sentiment


class AITraderAgent(BaseAgent):
    def decide(self, context):
        headline = context.get("headline", "")
        sentiment = analyze_sentiment(headline)

        if sentiment == "positive":
            return "buy"
        elif sentiment == "negative":
            return "sell"
        return "hold"

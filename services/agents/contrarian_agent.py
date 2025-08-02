from services.agents.base_agent import BaseAgent


class ContrarianAgent(BaseAgent):
    def decide(self, context):
        sentiment = context.get("sentiment", "neutral")
        if sentiment == "greed":
            return "sell"
        elif sentiment == "fear":
            return "buy"
        return "hold"

from services.agents.base_agent import BaseAgent


class EmotionalAgent(BaseAgent):
    def decide(self, context):
        history = context['price_history']
        sentiment = context.get('sentiment', 'neutral')

        if len(history) >= 2 and history[-1] < 0.95 * history[-2]:
            return "sell"  # panic from price drop

        if sentiment == "fear":
            return "sell"
        elif sentiment == "greed":
            return "buy"

        return "hold"

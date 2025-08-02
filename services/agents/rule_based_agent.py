
import numpy as np

from services.agents.base_agent import BaseAgent


class RuleBasedAgent(BaseAgent):
    def decide(self, context):
        history = context["price_history"]
        if len(history) < 10:
            return "hold"

        ma_5 = np.mean(history[-5:])
        ma_10 = np.mean(history[-10:])
        if ma_5 > ma_10:
            return "buy"
        elif ma_5 < ma_10:
            return "sell"
        return "hold"

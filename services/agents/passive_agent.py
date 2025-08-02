
import random

from services.agents.base_agent import BaseAgent


class PassiveAgent(BaseAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0

    def decide(self, context):
        self.counter += 1
        if self.counter % 20 == 0:
            return random.choice(["buy", "sell"])
        return "hold"

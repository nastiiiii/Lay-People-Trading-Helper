class BaseAgent:
    def __init__(self, trader_type: str, aggressiveness: float, reaction_speed: float):
        self.trader_type = trader_type
        self.aggressiveness = aggressiveness
        self.reaction_speed = reaction_speed

    def decide(self, market_context: dict) -> str:
        """Override in subclasses to return 'buy', 'sell', or 'hold'."""
        raise NotImplementedError

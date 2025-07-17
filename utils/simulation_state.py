from typing import Dict
from threading import Lock
from uuid import UUID

class SimulationState:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(SimulationState, cls).__new__(cls)
                cls._instance._data = {}  # {session_id: {stock_symbol: current_price}}
            return cls._instance

    def update_price(self, session_id: UUID, stock_symbol: str, price: float):
        self._data.setdefault(session_id, {})[stock_symbol] = price

    def get_price(self, session_id: UUID, stock_symbol: str) -> float:
        return self._data.get(session_id, {}).get(stock_symbol)

    def clear_session(self, session_id: UUID):
        if session_id in self._data:
            del self._data[session_id]

from typing import Dict
from threading import Lock
from uuid import UUID
import numpy as np
import torch
import torch.nn as nn
from sklearn.preprocessing import MinMaxScaler

from db.database import SessionLocal
from models.stock import Stock
from models.sandboxSession import SandboxSession

class LSTMModel(nn.Module):
    def __init__(self, input_size=1, hidden_size=32, output_size=1):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return out

class SimulationState:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(SimulationState, cls).__new__(cls)
                cls._instance._data = {}  # {session_id: {stock_symbol: current_price}}
                cls._instance._history = {} # {session_id: {stock_symbol: [price1, price2, ...]}}
            return cls._instance

    def update_price(self, session_id: UUID, stock_symbol: str, price: float):
        self._data.setdefault(session_id, {})[stock_symbol] = price
        self._history.setdefault(session_id, {}).setdefault(stock_symbol, []).append(price)

    def get_price(self, session_id: UUID, stock_symbol: str) -> float:
        return self._data.get(session_id, {}).get(stock_symbol)

    def clear_session(self, session_id: UUID):
        self._data.pop(session_id, None)
        self._history.pop(session_id, None)

    def get_price_history(self, session_id: UUID, stock_symbol: str) -> list:
        return self._history.get(session_id, {}).get(stock_symbol, [])

    def predict_next_price(self, session_id: UUID, stock_symbol: str, window_size=10):
        db = SessionLocal()
        try:
            session = db.query(SandboxSession).filter_by(session_id=session_id).first()
            stock = db.query(Stock).filter_by(stock_symbol=stock_symbol).first()

            if not session or not stock or not stock.historical_prices:
                return None

            delta_days = (session.current_date - session.start_date).days
            if delta_days < window_size + 1:
                return None

            history = stock.historical_prices[:delta_days + 1]

            prices = np.array(history).reshape(-1, 1)
            scaler = MinMaxScaler()
            scaled_prices = scaler.fit_transform(prices)

            X = []
            y = []
            for i in range(window_size, len(scaled_prices)):
                X.append(scaled_prices[i - window_size:i])
                y.append(scaled_prices[i])

            X = torch.tensor(X, dtype=torch.float32)
            y = torch.tensor(y, dtype=torch.float32)

            model = LSTMModel()
            loss_fn = nn.MSELoss()
            optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

            model.train()
            for epoch in range(30):
                optimizer.zero_grad()
                output = model(X)
                loss = loss_fn(output, y)
                loss.backward()
                optimizer.step()

            last_window = scaled_prices[-window_size:]
            last_window_tensor = torch.tensor(last_window.reshape(1, window_size, 1), dtype=torch.float32)

            model.eval()
            with torch.no_grad():
                predicted_scaled = model(last_window_tensor).numpy()

            predicted_price = scaler.inverse_transform(predicted_scaled)[0][0]
            return float(predicted_price)
        finally:
            db.close()

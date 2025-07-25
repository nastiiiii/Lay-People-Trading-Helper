from random import random, choice
from uuid import UUID

import httpx

from env import CLAUDE_API_KEY, url, headers
from utils.simulation_state import SimulationState

BIAS_LIBRARY = [
    {
        "type": "confirmation",
        "advice": lambda stock: f"Everyone says {stock} will skyrocket! You should totally buy it now!",
        "rationale": "The advisor selectively focuses on information that confirms prior beliefs."
    },
    {
        "type": "loss_aversion",
        "advice": lambda stock: f"You've already lost money on {stock}. Selling now would just make it real. Hold on!",
        "rationale": "Avoids realizing a loss due to emotional discomfort."
    },
    {
        "type": "bandwagon",
        "advice": lambda stock: f"Everyone's buying {stock} lately. You should too!",
        "rationale": "The advisor is following the crowd rather than doing analysis."
    },
    {
        "type": "overconfidence",
        "advice": lambda stock: f"{stock} has been strong all week — it can't go down now! Buy with confidence!",
        "rationale": "Assumes they can predict the market without error."
    }
]

def get_sandbox_advice(db, session_id: UUID, stock_symbol: str,action: str) -> dict:
    current_price = SimulationState().get_price(session_id, stock_symbol)
    if current_price is None:
        return {
            "error": "No current price available for this stock in the active simulation."
        }

    is_biased = random() < 0.5

    if is_biased:
        bias = choice(BIAS_LIBRARY)
        return {
            "advice_text": bias["advice"](stock_symbol),
            "is_biased": True,
            "bias_type": bias["type"],
            "rationale": bias["rationale"]
        }
    else:
        advice = ""
        if action == "buy":
            if current_price < 100:
                advice = f"{stock_symbol} is currently cheap at ${current_price:.2f}. Consider researching its fundamentals before buying."
            elif current_price > 300:
                advice = f"{stock_symbol} is trading high at ${current_price:.2f}. Only buy if you expect strong future growth."
            else:
                advice = f"{stock_symbol} is moderately priced at ${current_price:.2f}. Consider market trends and long-term value."
            rationale = "Encourages price-aware, data-driven investing."
        else:  # SELL
            if current_price > 250:
                advice = f"{stock_symbol} is at a high of ${current_price:.2f}. Selling could help you lock in gains."
            else:
                advice = f"{stock_symbol} is at ${current_price:.2f}. Consider if it's below your sell target or if market conditions have changed."
            rationale = "Considers current price and strategic sell timing."

        return {
            "advice_text": advice,
            "is_biased": False,
            "rationale": rationale
        }


def get_claude_advice(session_id, stock_symbol, action, current_price, portfolio):
    portfolio_summary = f"Cash balance: ${portfolio['cash_balance']:.2f}\n"
    holdings = portfolio.get("stock_holdings", [])
    if holdings:
        portfolio_summary += "Stock holdings:\n"
        for stock in holdings:
            portfolio_summary += (
                f"- {stock['stock_symbol']}: {stock['quantity']} shares at ${stock['current_price']:.2f}\n"
            )
    else:
        portfolio_summary += "No stock holdings.\n"

    prompt = (
        f"I am a simulated trading assistant. Here is the user's current portfolio:\n"
        f"{portfolio_summary}\n"
        f"The current price of {stock_symbol} is ${float(current_price):.2f}. "
        f"The user is considering to {action.upper()}.\n"
        f"What would you advise them, and why?"
    )

    data = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = httpx.post(url, headers=headers, json=data,timeout=30.0)

    if response.status_code == 200:
        text = response.json()['content'][0]['text']
        return {
            "advice_text": text.strip(),
            "is_biased": False,
            "rationale": "Claude's advice based on user portfolio and stock context."
        }
    else:
        raise Exception(f"Claude API error {response.status_code}: {response.text}")

import time
import random
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from db.database import DATABASE_URL
from models.marketAgentDef import MarketAgentDefinition
from models.marketSimConfig import MarketSimulationConfig
from models.marketTickLog import MarketTickLog
from services.agents.ai_trader_agent import AITraderAgent
from services.agents.contrarian_agent import ContrarianAgent
from services.agents.emotional_agent import EmotionalAgent
from services.agents.passive_agent import PassiveAgent
from services.agents.rule_based_agent import RuleBasedAgent
from utils.market_news import generate_news

latest_news = {}  # {simulation_id: {"headline": "...", "sentiment": "..."}}
user_states = {}  # simulation_id -> {"balance": float, "holdings": float, "last_price": float}
user_trade_queues = {}  # simulation_id -> list of trades


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def run_market_simulation(simulation_id):
    sim_id_str = str(simulation_id)

    if sim_id_str not in user_states:
        user_states[sim_id_str] = {
            "balance": 100.0,
            "holdings": 0.0,
            "last_price": 0.0
        }

    if sim_id_str not in user_trade_queues:
        user_trade_queues[sim_id_str] = []

    db = SessionLocal()
    try:
        config = db.query(MarketSimulationConfig).filter_by(id=simulation_id).first()
        if not config:
            print("[SIM] Config not found.")
            return

        agent_defs = db.query(MarketAgentDefinition).filter_by(config_id=config.id).all()

        # Step 1: Build agent pool
        agents = []
        for agent_def in agent_defs:
            for _ in range(agent_def.count):
                if agent_def.trader_type == "emotional":
                    agent = EmotionalAgent(
                        trader_type="emotional",
                        aggressiveness=agent_def.aggressiveness,
                        reaction_speed=agent_def.reaction_speed
                    )
                elif agent_def.trader_type == "rule_based":
                    agent = RuleBasedAgent(
                        trader_type="rule_based",
                        aggressiveness=agent_def.aggressiveness,
                        reaction_speed=agent_def.reaction_speed
                    )
                elif agent_def.trader_type == "contrarian":
                    agent = ContrarianAgent(
                        trader_type="contrarian",
                        aggressiveness=agent_def.aggressiveness,
                        reaction_speed=agent_def.reaction_speed
                    )
                elif agent_def.trader_type == "passive":
                    agent = PassiveAgent(
                        trader_type="passive",
                        aggressiveness=agent_def.aggressiveness,
                        reaction_speed=agent_def.reaction_speed
                    )
                elif agent_def.trader_type == "ai":
                    agent = AITraderAgent(
                        trader_type="ai",
                        aggressiveness=agent_def.aggressiveness,
                        reaction_speed=agent_def.reaction_speed
                    )
                else:
                    continue
                agents.append(agent)

        # Step 2: Initialize market
        price = 100.0
        price_history = [price]
        tick = 0
        SENTIMENT_MAP = {"neutral": 0.0, "fear": -1.0, "greed": 1.0}

        while tick < 100:  # Run for 100 ticks for now
            buy_pressure = 0.0
            sell_pressure = 0.0
            sentiment = generate_news(config.shock_frequency)
            print(f"[TICK {tick}] News event: {sentiment}")
            sentiment, headline = generate_news(config.shock_frequency)
            latest_news[config.id] = {
                "headline": headline,
                "sentiment": sentiment
            }

            context = {
                "price_history": price_history,
                "sentiment": sentiment
            }

            user_state = user_states[sim_id_str]
            queue = user_trade_queues[sim_id_str]

            for trade in list(queue):
                if trade["action"] == "buy" and user_state["balance"] >= price:
                    user_state["balance"] -= price
                    user_state["holdings"] += 1
                    user_state["last_price"] = price
                    print(f"[USER TRADE] Bought at {price}")
                elif trade["action"] == "sell" and user_state["holdings"] > 0:
                    user_state["balance"] += price
                    user_state["holdings"] -= 1
                    user_state["last_price"] = price
                    print(f"[USER TRADE] Sold at {price}")
                queue.remove(trade)

            def agent_decision(agent):
                if random.random() < agent.reaction_speed:
                    action = agent.decide(context)
                    return action, agent.aggressiveness
                return "hold", 0.0

            with ThreadPoolExecutor(max_workers=20) as executor:
                results = list(executor.map(agent_decision, agents))

            for action, weight in results:
                if action == "buy":
                    buy_pressure += weight
                elif action == "sell":
                    sell_pressure += weight

            net_pressure = buy_pressure - sell_pressure
            delta = net_pressure * 0.1  # market sensitivity factor
            price += delta
            price = max(price, 1.0)  # prevent crash below 0
            price_history.append(price)

            # --------- LOG THE TICK HERE ----------
            log = MarketTickLog(
                simulation_id=config.id,
                tick_number=tick,
                price=float(price),
                buy_pressure=float(buy_pressure),
                sell_pressure=float(sell_pressure),
                sentiment=float(SENTIMENT_MAP[context["sentiment"]]),
                timestamp=datetime.utcnow()  # optional if model has default
            )
            db.add(log)
            # Commit every few ticks for performance; adjust as needed
            if tick % 10 == 0:
                db.commit()
            # --------------------------------------

            print(f"[TICK {tick}] Price: {round(price, 2)} | Buy: {buy_pressure:.2f} | Sell: {sell_pressure:.2f}")
            tick += 1
            time.sleep(10)  # 1-second ticks

        # Final commit to flush remaining logs
        db.commit()
    finally:
        db.close()


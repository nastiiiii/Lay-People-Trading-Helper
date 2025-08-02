from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from uuid import UUID
import threading

from db.database import get_db
from models.marketAgentDef import MarketAgentDefinition
from models.marketSimConfig import MarketSimulationConfig
from models.marketTickLog import MarketTickLog
from schema import MarketSimulationConfigCreate, MarketTickLogResponse
from services.market_tick_engine import run_market_simulation, user_trade_queues, user_states, latest_news

router = APIRouter(prefix="/market-simulation", tags=["Market Simulation"])


@router.post("/configure")
def configure_market_simulation(config_data: MarketSimulationConfigCreate, db: Session = Depends(get_db)):
    config = MarketSimulationConfig(
        user_id=config_data.user_id,
        market_type=config_data.market_type,
        shock_frequency=config_data.shock_frequency,
        noise_level=config_data.noise_level
    )
    db.add(config)
    db.commit()
    db.refresh(config)

    for agent in config_data.agents:
        agent_def = MarketAgentDefinition(
            config_id=config.id,
            trader_type=agent.trader_type,
            count=agent.count,
            aggressiveness=agent.aggressiveness,
            reaction_speed=agent.reaction_speed
        )
        db.add(agent_def)

    db.commit()
    return {"message": "Market simulation configured", "simulation_id": config.id}


@router.post("/start/{simulation_id}")
def start_market_simulation(simulation_id: UUID):
    thread = threading.Thread(target=run_market_simulation, args=(simulation_id,), daemon=True)
    thread.start()
    return {"message": "Market simulation started", "simulation_id": simulation_id}


@router.get("/ticks/{simulation_id}", response_model=list[MarketTickLogResponse])
def get_market_ticks(simulation_id: UUID, db: Session = Depends(get_db)):
    logs = (
        db.query(MarketTickLog)
        .filter_by(simulation_id=simulation_id)
        .order_by(MarketTickLog.tick_number)
        .all()
    )
    return [
        MarketTickLogResponse(
            tick=log.tick_number,
            price=log.price,
            buy_pressure=log.buy_pressure,
            sell_pressure=log.sell_pressure,
            sentiment=log.sentiment,
            timestamp=log.timestamp
        )
        for log in logs
    ]


@router.post("/trade/{simulation_id}")
def submit_user_trade(simulation_id: UUID, action: str = Body(...)):
    if action not in ["buy", "sell"]:
        raise HTTPException(status_code=400, detail="Invalid action")
    sim_id_str = str(simulation_id)
    if sim_id_str not in user_trade_queues:
        raise HTTPException(status_code=404, detail="Simulation not running")
    user_trade_queues[sim_id_str].append({"action": action})
    return {"message": f"Trade submitted: {action}"}


@router.get("/portfolio/{simulation_id}")
def get_user_portfolio(simulation_id: UUID):
    sim_id_str = str(simulation_id)
    state = user_states.get(sim_id_str)
    if not state:
        raise HTTPException(status_code=404, detail="No portfolio found")
    return {
        "balance": state["balance"],
        "holdings": state["holdings"],
        "value": state["balance"] + (state["holdings"] * state["last_price"])
    }


@router.get("/news/{simulation_id}")
def get_latest_news(simulation_id: UUID):
    sim_id_str = str(simulation_id)
    news = latest_news.get(sim_id_str)
    if not news:
        raise HTTPException(status_code=404, detail="No news found for this simulation.")
    return news

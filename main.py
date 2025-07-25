from fastapi import FastAPI

from db.database import Base, engine
from routers import user, trade, stock, bias, nudge, behavior, sandbox, bias_detector

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(trade.router)
app.include_router(stock.router)
app.include_router(bias.router)
app.include_router(nudge.router)
app.include_router(behavior.router)
app.include_router(sandbox.router)

app.include_router(bias_detector.router)
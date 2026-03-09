from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine, Base
import app.models
from app.routers import users, game, shop

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Capybara Game API",
    lifespan=lifespan
)

app.include_router(users.router)
app.include_router(game.router)
app.include_router(shop.router)

@app.get("/ping")
async def ping():
    return {"status": "ok", "db": "ready"}
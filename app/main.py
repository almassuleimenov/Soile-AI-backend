from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <--- ИМПОРТИРУЕМ CORS
from app.database import engine, Base
import app.models
from app.routers import users, game, shop


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Capybara Game API", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем запросы с любых сайтов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем любые методы (GET, POST)
    allow_headers=["*"],  # Разрешаем любые заголовки
)

app.include_router(users.router)
app.include_router(game.router)
app.include_router(shop.router)


@app.get("/ping")
async def ping():
    return {"status": "ok", "db": "ready"}

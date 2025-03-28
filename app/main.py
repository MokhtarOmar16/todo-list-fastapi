# app/main.py
from fastapi import FastAPI
from app.db.database import engine
from app.db.base import Base
from app.api.routes import api_router

app = FastAPI(title="FastAPI ToDo App")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(api_router, prefix="/api")

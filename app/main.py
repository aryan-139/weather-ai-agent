from fastapi import FastAPI
from app.routes.weather import router as weather_router
from app.routes.chat import router as chat_router

app = FastAPI(title="Weather AI Agent")

app.include_router(weather_router, prefix="/weather")
app.include_router(chat_router, prefix="/chat") 
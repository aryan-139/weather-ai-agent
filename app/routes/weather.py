from fastapi import APIRouter, Query
from app.services.weather_api import get_weather_data

router = APIRouter()

@router.get("/")
def get_weather(city: str = Query(..., description="City name")):
    return get_weather_data(city)

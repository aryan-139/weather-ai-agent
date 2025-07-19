# In app/routes/chat.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import json
from app.services.weather_api import get_weather_data

# --- Assumed Setup ---
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "deepseek-coder"
PROMPT= f"""
You are an expert intent classifier. Analyze the user's message.
Your task is to identify if the user's intent is 'weather' or 'other'.
If the intent is 'weather', extract the city or location mentioned.

You MUST respond ONLY with a JSON object with two keys: "intent" and "location".
- The "intent" value must be either "weather" or "other".
- The "location" value should be the location mentioned by the user. If no location is mentioned, set it to null. """

class ChatRequest(BaseModel):
    message: str
# --------------------
router = APIRouter()
@router.post("/")
def chat_with_ollama(payload: ChatRequest):
    try:
        classifier_prompt = PROMPT + f"""
User message: "{payload.message}"
"""
        classifier_response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": [{"role": "user", "content": classifier_prompt}],
                "format": "json",
                "stream": False
            },
            timeout=30
        )
        classifier_response.raise_for_status()

        result_content = classifier_response.json()["message"]["content"]
        classification = json.loads(result_content)
        intent = classification.get("intent")
        location = classification.get("location")

        if intent != "weather":
            return {"message": "Only weather related queries will be entertained."}

        city = location if location else "Bengaluru"
        print(f"Classified intent: {intent}, Location: {city}")

        # call the weather API and get the coordinates 
        if intent=="weather":
            weather_data_function_calling= get_weather_data(city)
        
        weather_data= weather_data_function_calling
        return weather_data

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Error contacting Ollama: {e}")
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse or validate LLM response: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
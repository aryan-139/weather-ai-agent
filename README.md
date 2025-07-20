# Weather AI Agent 🤖🌦️

A simple yet powerful FastAPI application that acts as an intelligent agent for weather-related queries. It uses an Ollama-hosted LLM for natural language understanding and the OpenWeatherMap API to fetch real-time weather data.

-----

## ✨ Features

  * **AI-Powered Intent Classification**: Leverages a local LLM (via Ollama) to understand user queries and determine if they are asking for weather information.
  * **Location Extraction**: Automatically extracts the city or location from the user's message.
  * **Real-time Weather Data**: Fetches current weather data from the OpenWeatherMap API.
  * **Structured JSON Responses**: Returns well-formatted JSON data, making it easy for client applications to consume.
  * **Default Location**: Defaults to a pre-configured location ("Bengaluru") if no specific location is mentioned in the query.
  * **Asynchronous Ready**: Built on FastAPI, ready for high-performance, asynchronous workloads.

-----

## ⚙️ Architecture Flow

The application follows a simple, robust workflow:

1.  A user sends a natural language query (e.g., "What's the weather like in Paris?") to the `/chat` endpoint.
2.  FastAPI forwards this query to a locally running Ollama instance.
3.  The LLM (`deepseek-coder` in this case) analyzes the message and returns a JSON object classifying the intent (`"weather"` or `"other"`) and extracting the location (`"Paris"`).
4.  If the intent is `"weather"`, the application calls the `get_weather_data` function with the extracted city.
5.  This function queries the OpenWeatherMap API for the weather information.
6.  The weather data is formatted into a clean JSON object, including timezone-aware timestamps for IST (Asia/Kolkata).
7.  The final formatted weather data is returned to the user.
8.  If the intent is not `"weather"`, a simple message is returned.

-----

## 🚀 Getting Started

### Prerequisites

  * **Python 3.8+**
  * **Ollama**: Ensure you have [Ollama](https://ollama.com/) installed and running on your local machine (`http://localhost:11434`).
  * **Ollama Model**: Pull the required model.
    ```bash
    ollama pull deepseek-coder
    ```
  * **OpenWeatherMap API Key**: You'll need a free API key from [OpenWeatherMap](https://openweathermap.org/api).

### Installation & Setup

1.  **Clone the repository:**

    ```bash
    git clone weather-ai-agent
    cd weather-ai-agent
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    # For Unix/macOS
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    Create a `requirements.txt` file with the following content and install it.

    ```text
    # requirements.txt
    fastapi
    uvicorn[standard]
    requests
    ```

    Then run:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure API Key:**
    In this code, the API key is hardcoded in `app/services/weather_api.py`. It's highly recommended to use environment variables for security.

### Running the Application

Once the setup is complete, run the application using Uvicorn:

```bash
uvicorn main:app --reload
```

The server will start, typically on `http://127.0.0.1:8000`.

-----

## 🛰️ API Endpoints

The primary endpoint for interacting with the agent is `/chat`.

### `POST /chat/`

This endpoint receives a user's message, classifies the intent, and returns weather data if applicable.

**Request Body:**

```json
{
  "message": "your natural language query here"
}
```

#### Example 1: Query with a specific location

**Request (cURL):**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/chat/' \
  -H 'Content-Type: application/json' \
  -d '{
    "message": "how is the weather in Tokyo?"
  }'
```

**Success Response (200 OK):**

```json
{
    "city": "Tokyo",
    "temperature": "28.5°C",
    "condition": "Clear sky",
    "retrieved_at": "10:08 PM, 19 Jul 2025",
    "minimum_temperature": "26.9°C",
    "maximum_temperature": "29.8°C",
    "coordinates": {
        "latitude": 35.6895,
        "longitude": 139.6917
    }
}
```

#### Example 2: Non-weather related query

**Request (cURL):**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/chat/' \
  -H 'Content-Type: application/json' \
  -d '{
    "message": "hello, how are you?"
  }'
```

**Response:**

```json
{
    "message": "Only weather related queries will be entertained."
}
```

-----

## 📁 Project Structure

```
.
├── app
│   ├── routes
│   │   ├── __init__.py
│   │   ├── chat.py       # Defines the /chat endpoint logic
│   │   └── weather.py    # Defines the (unused) /weather endpoint
│   ├── services
│   │   ├── __init__.py
│   │   └── weather_api.py # Contains get_weather_data function
│   └── __init__.py
├── main.py               # Main FastAPI app instantiation and router inclusion
└── requirements.txt      # Project dependencies
```

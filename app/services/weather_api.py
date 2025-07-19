import requests
from zoneinfo import ZoneInfo
from datetime import datetime

API_KEY = '9a4303c3daeb2b91ea3866815ceec7bc'

def format_timestamp_ist(unix_time: int) -> str:
    """Converts a UNIX timestamp to a formatted IST string using zoneinfo."""
    # 2. Create the timezone object directly from ZoneInfo
    ist_timezone = ZoneInfo("Asia/Kolkata")
    
    # Create a timezone-aware datetime object
    dt_object = datetime.fromtimestamp(unix_time, tz=ist_timezone)
    return dt_object.strftime("%-I:%M %p, %d %b %Y")

def get_weather_data(city: str)-> dict:
    print(f"Fetching weather data for city: {city}")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    print(response.status_code, response.text)  # Debugging line to check response status and content
    if response.status_code != 200:
        raise Exception(f"Error fetching weather data: {response.status_code} - {response.text}")
    data = response.json()
    print(f"Received weather data: {data}")  # Debugging line to check received data
    weather_info = {
        "city": data["name"],
        "temperature": f"{data['main']['temp']}°C",
        "condition": data["weather"][0]["description"].capitalize(),
        "retrieved_at": format_timestamp_ist(data["dt"]),
        "minimum_temperature": f"{data['main']['temp_min']}°C",
        "maximum_temperature": f"{data['main']['temp_max']}°C",
        "coordinates": {
            "latitude": data["coord"]["lat"],
            "longitude": data["coord"]["lon"]
        }
    }
    print(f"Processed weather data: {weather_info}")  # Debugging line to check processed data
    return weather_info

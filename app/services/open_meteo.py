import httpx


GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

class WeatherError(Exception):
    pass

def geocode_city(city: str) -> tuple[float, float, str]:

    """
    Şehrin enlem ve boylami
    """

    params = {"name": city, "count": 1, "language": "tr"}
    r = httpx.get(GEOCODE_URL, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    results = data.get("results") or []
    if not results:
        raise WeatherError(f"Şehir bulunamadi: {city}")
    top = results[0]
    return float(top["latitude"]), float(top["longitude"]), top.get("name", city)

def fetch_current_weather(lat: float, lon: float) -> dict:
    
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "wind_speed_10m"],
        "timezone": "auto",
    }
    r = httpx.get(WEATHER_URL, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    cur = data.get("current") or {}

    if not cur:
        raise WeatherError("Anlik veri alinamadi")
    return {
        "temperature": float(cur.get("temperature_2m")),
        "windspeed": float(cur.get("wind_speed_10m")),
        "observed_at": str(cur.get("time")),
    }
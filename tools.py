# tools.py
import requests
from datetime import datetime

def get_time(city: str):
    """
    Uses worldtimeapi.org via a quick city->timezone lookup with geocoding.
    Falls back gracefully if not found.
    """
    try:
        # 1) Geocode city -> lat/lon (Open-Meteo geocoding; no key)
        g = requests.get("https://geocoding-api.open-meteo.com/v1/search",
                         params={"name": city, "count": 1}).json()
        if not g.get("results"):
            return {"ok": False, "error": f"Couldn't find city '{city}'."}
        tz = g["results"][0]["timezone"]

        # 2) Query worldtimeapi
        t = requests.get(f"https://worldtimeapi.org/api/timezone/{tz}").json()
        return {"ok": True, "city": city, "timezone": tz, "datetime": t.get("datetime")}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def get_weather(city: str):
    """
    Uses Open-Meteo current weather. No API key required.
    """
    try:
        # 1) Geocode city -> lat/lon
        g = requests.get("https://geocoding-api.open-meteo.com/v1/search",
                         params={"name": city, "count": 1}).json()
        if not g.get("results"):
            return {"ok": False, "error": f"Couldn't find city '{city}'."}
        place = g["results"][0]
        lat, lon = place["latitude"], place["longitude"]

        # 2) Current weather
        w = requests.get("https://api.open-meteo.com/v1/forecast",
                         params={"latitude": lat, "longitude": lon, "current_weather": True}).json()
        cw = w.get("current_weather") or {}
        return {
            "ok": True,
            "city": place["name"],
            "country": place.get("country"),
            "lat": lat, "lon": lon,
            "temperature_c": cw.get("temperature"),
            "windspeed_kmh": cw.get("windspeed"),
            "weathercode": cw.get("weathercode"),
            "time_iso": cw.get("time"),
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}

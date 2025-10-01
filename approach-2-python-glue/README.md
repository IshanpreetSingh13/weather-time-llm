# Weather & Time Project – My Notes

This is my own small project where I connected a local LLM (**SmolLM2 in Ollama**) with live **weather** and **time** data.  
The idea was given by my company – they told me to "train" it on weather and time, but I realized instead of training,  
I can just use tools (APIs) and let the model summarize the results.

---

## What I Did
1. Created a new Python project folder `weather-time-llm`.
2. Set up a virtual environment (`python -m venv .venv`) and activated it.
3. Upgraded pip inside the venv.
4. Installed `requests` and `python-dotenv`.
5. Installed **Ollama** and pulled the `smollm2` model (can also use other tags if needed).
6. Wrote two tools:
   - `get_weather(city)` → calls Open-Meteo API to get temperature, wind, etc.
   - `get_time(city)` → calls WorldTimeAPI to get current time.
7. Wrote an `app.py` that:
   - Reads the user’s question (like *“weather in Brampton”* or *“time in Tokyo”*),
   - Decides which tool to call,
   - Feeds the tool’s JSON result into SmolLM2,
   - Prints back a nice friendly answer.

---

## How To Run
Examples:
```powershell
python app.py "weather in Brampton"
python app.py "time in Tokyo"
```

Sample output:
```
It’s currently about 19°C in Brampton with light winds around 7 km/h.
```

---

## My Understanding
- The tools fetch data from APIs,  
  and the model just rewrites it in plain English.  
- This is much cleaner and works fully local (except for API calls).

---

## Status Update (for team)
I finished the first working version.  
Right now, I can ask the app for **weather** or **time**, and it returns nice answers using SmolLM2.  
No fine-tuning was required – I just used Python glue code + APIs.  

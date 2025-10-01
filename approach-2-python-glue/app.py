import json, subprocess, sys
import requests
from tools import get_time, get_weather

SYSTEM_PROMPT = (
    "You are a helpful assistant. When tool results are provided, write a clear, short answer for users. "
    "If a city wasn't found, politely say so and suggest checking the spelling."
)

def call_ollama(model: str, prompt: str) -> str:
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=120,
    )
    r.raise_for_status()
    data = r.json()
    return (data.get("response") or "").strip()

def route(question: str):
    q = question.lower().strip()
    if "weather" in q:
        city = q.split("in")[-1].strip().strip("?") if " in " in q else q.replace("weather", "").strip()
        result = get_weather(city or "Brampton")
        toolname = "get_weather"
    elif "time" in q or "current time" in q:
        city = q.split("in")[-1].strip().strip("?") if " in " in q else q.replace("time", "").strip()
        result = get_time(city or "Brampton")
        toolname = "get_time"
    else:
        return "Ask me about the weather or the time, e.g. 'weather in Brampton' or 'time in Tokyo'."

    return toolname, result

def main():
    model = "smollm2"  
    if len(sys.argv) < 2:
        print("Usage: python app.py \"weather in Brampton\"")
        sys.exit(1)

    question = sys.argv[1]
    routed = route(question)
    if isinstance(routed, str):
        print(routed)
        return

    toolname, result = routed
    tool_json = json.dumps(result, ensure_ascii=False, indent=2)

    prompt = f"""{SYSTEM_PROMPT}

User question:
{question}

Tool used: {toolname}
Tool raw JSON:
{tool_json}

Write a concise, friendly answer for the user in plain English, including units where helpful.
"""
    try:
        answer = call_ollama(model, prompt)
        print(answer.strip())
    except Exception as e:
        print("Error calling model:", e)

if __name__ == "__main__":
    main()

import os, json, requests

GATEWAY_BASE_URL = os.getenv("GATEWAY_BASE_URL", "http://localhost:8765")
CHAT_URL = f"{GATEWAY_BASE_URL}/api/chat"
MODEL = os.getenv("MODEL_NAME", "smollm2")

SYSTEM = (
    "You are a helpful assistant. When the user asks for weather or local time, "
    "you MUST call the MCP tools named 'openweather' (or 'weather') and 'time' via the Gateway. "
    "Do not guess or fabricate data. Be concise and include units and local timestamps."
)

def ask(msg: str):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": msg}
        ],
        "tool_choice": "auto"
    }
    r = requests.post(CHAT_URL, json=payload, timeout=180)
    r.raise_for_status()
    print(json.dumps(r.json(), indent=2))

if __name__ == "__main__":
    ask("What's the local time in Brampton right now?")
    ask("What's the weather in Brampton today and tomorrow?")

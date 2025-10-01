# Approach 3 — MCP Gateway (Final Solution)

This was the **most robust and correct solution** because the LLM itself directly calls the MCP tools, instead of relying on Python as a middleman.

---

## 📌 Architecture

- **SmolLM2 (Ollama)** runs inside Docker.  
- **Time MCP Server** and **Weather MCP Server** run as separate Docker containers.  
- **MCP Gateway** in Docker connects the LLM to those servers.  
- A lightweight **Python relay (`chat.py`)** sends user queries → Gateway → LLM + MCP servers → structured answers.

---

## 📂 Project Structure

approach-3-MCP-Gateway/
├── .env # Environment variables (OpenWeather API key, model name, etc.)
├── chat.py # Python relay script to test queries via the Gateway
├── docker-compose.yml # Docker services: Ollama, MCP Gateway, Time + Weather servers
├── mcp-gateway.json # Gateway config for model + tool servers
├── requirements.txt # Python dependencies


---

## ⚙️ Setup Instructions

### 1. Python Environment
```bash
cd approach-3-MCP-Gateway
python -m venv .venv
.venv\Scripts\activate    # Windows
# OR
source .venv/bin/activate # Linux/Mac
pip install -r requirements.txt
2. Create .env File
Add this to a file called .env:

ini
Copy code
OPENWEATHER_API_KEY=your_api_key_here
MODEL_NAME=smollm2
Replace your_api_key_here with your real OpenWeather API key.

▶️ Running with Docker
Start everything:

bash
Copy code
docker compose up -d
Check running containers:

bash
Copy code
docker ps
Stop services:

bash
Copy code
docker compose down
View logs for debugging:

bash
Copy code
docker logs mcp-gateway --tail=100
💬 Running the Chat Script
Once containers are up and venv is activated:

bash
Copy code
python chat.py
This will send sample queries:

“What’s the local time in Brampton right now?”

“What’s the weather in Brampton today and tomorrow?”

##  ⚠️ Known Issues
Sometimes the MCP Gateway does not return tool results.

Error seen:

Empty tools list

Gateway connection errors

Root cause: Gateway not fully registering model + tools (ollama, time, openweather).

Troubleshooting steps:

bash
Copy code
docker ps                      # confirm all containers are running
docker logs mcp-gateway        # see gateway logs
docker logs ollama             # check if model is loaded
docker logs time               # verify time server is up
docker logs openweather        # verify weather server is up


✅ Benefits of Approach 3
Containerized: easy to set up and reproduce.

Direct LLM tool calls: no middleman deciding when to use APIs.

Modular: new MCP servers can be added later (finance, maps, news, etc.).


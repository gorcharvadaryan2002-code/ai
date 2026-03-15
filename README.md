# 24/7 AI Assistant App

This project is a lightweight **always-on AI assistant** you can run on your machine or server.

It exposes a local HTTP API for chat and remembers context between messages using a JSON memory file.

## Features

- Runs continuously as a web service
- Chat endpoint (`POST /chat`)
- Persistent memory for notes, tasks, and chat snippets
- Optional integration with **Ollama** for LLM responses
- Works without external APIs (fallback local assistant mode)

## How to use

### 1) Install and run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Server starts on `http://0.0.0.0:8000` by default.

---

### 2) Check service status

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status":"ok"}
```

---

### 3) Chat with your assistant

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"todo call mom tomorrow"}'
```

Example response:

```json
{
  "reply": "✅ Got it — I added this to your tasks: call mom tomorrow",
  "memory_count": 2
}
```

---

### 4) Save notes

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"note buy protein powder this weekend"}'
```

---

### 5) Ask for tasks or memory

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"what are my tasks"}'
```

```bash
curl http://localhost:8000/memory
```

---

### 6) Optional: enable Ollama

If you have Ollama running locally, edit `.env`:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1
```

Restart the app, then `/chat` responses will come from your model. If Ollama is unavailable, the app safely falls back to built-in local assistant behavior.

## Running 24/7

Use a process manager in production:

- `systemd` on Linux servers
- `pm2` or `supervisord`
- Docker with restart policy (`--restart unless-stopped`)

### Example systemd unit

Save this as `/etc/systemd/system/ai-assistant.service`:

```ini
[Unit]
Description=24/7 AI Assistant
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/path/to/ai
ExecStart=/path/to/ai/.venv/bin/python /path/to/ai/app.py
Restart=always
RestartSec=3
EnvironmentFile=/path/to/ai/.env

[Install]
WantedBy=multi-user.target
```

Then run:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-assistant
sudo systemctl start ai-assistant
sudo systemctl status ai-assistant
```

## Environment variables

- `HOST` (default: `0.0.0.0`)
- `PORT` (default: `8000`)
- `MEMORY_FILE` (default: `assistant_memory.json`)
- `OLLAMA_BASE_URL` (optional)
- `OLLAMA_MODEL` (optional)

# 24/7 AI Assistant App

This project is a lightweight **always-on AI assistant** you can run on your machine or server.

It exposes a local HTTP API for chat and remembers context between messages using a JSON memory file.

## Features

- Runs continuously as a web service
- Chat endpoint (`POST /chat`)
- Persistent memory for notes, tasks, and chat snippets
- Optional integration with **Ollama** for LLM responses
- Works without external APIs (fallback local assistant mode)

## Quick start

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. (Optional) Configure environment variables:

```bash
cp .env.example .env
```

4. Run the app:

```bash
python app.py
```

By default the server starts at `http://0.0.0.0:8000`.

## API

### `GET /health`
Returns service health.

### `POST /chat`
Send a message to your assistant.

Request JSON:

```json
{ "message": "remind me to drink water" }
```

Response JSON:

```json
{
  "reply": "✅ Got it — I added this to your tasks: drink water",
  "memory_count": 3
}
```

### `GET /memory`
Returns saved memory entries.

## Running 24/7

Use a process manager in production:

- `systemd` on Linux servers
- `pm2` or `supervisord`
- Docker with restart policy (`--restart unless-stopped`)

## Notes

- If `OLLAMA_BASE_URL` and `OLLAMA_MODEL` are set, the assistant will call Ollama for richer responses.
- If Ollama is not available, it still works in local fallback mode.

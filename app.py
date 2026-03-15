import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request

from assistant import AssistantConfig, PersonalAssistant

load_dotenv()

app = Flask(__name__)
assistant = PersonalAssistant(
    AssistantConfig(
        memory_file=os.getenv("MEMORY_FILE", "assistant_memory.json"),
        ollama_base_url=os.getenv("OLLAMA_BASE_URL", ""),
        ollama_model=os.getenv("OLLAMA_MODEL", ""),
    )
)


@app.get("/health")
def health() -> tuple:
    return jsonify({"status": "ok"}), 200


@app.get("/memory")
def memory() -> tuple:
    return jsonify({"entries": assistant.memory, "count": len(assistant.memory)}), 200


@app.post("/chat")
def chat() -> tuple:
    payload = request.get_json(silent=True) or {}
    message = (payload.get("message") or "").strip()

    if not message:
        return jsonify({"error": "message is required"}), 400

    reply = assistant.respond(message)
    return jsonify({"reply": reply, "memory_count": len(assistant.memory)}), 200


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    app.run(host=host, port=port)

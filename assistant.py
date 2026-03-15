import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class AssistantConfig:
    memory_file: str = "assistant_memory.json"
    ollama_base_url: str = ""
    ollama_model: str = ""


class PersonalAssistant:
    def __init__(self, config: AssistantConfig):
        self.config = config
        self.memory: List[Dict[str, Any]] = []
        self._load_memory()

    def _load_memory(self) -> None:
        if not os.path.exists(self.config.memory_file):
            return

        try:
            with open(self.config.memory_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                self.memory = json.loads(content) if content else []
        except (json.JSONDecodeError, OSError):
            self.memory = []

    def _save_memory(self) -> None:
        with open(self.config.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=2)

    def _remember(self, kind: str, content: str) -> None:
        self.memory.append({"kind": kind, "content": content, "timestamp": int(time.time())})
        self._save_memory()

    def _try_ollama(self, message: str) -> str:
        if not self.config.ollama_base_url or not self.config.ollama_model:
            raise RuntimeError("Ollama is not configured")

        url = f"{self.config.ollama_base_url.rstrip('/')}/api/chat"
        payload = {
            "model": self.config.ollama_model,
            "stream": False,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a personal AI assistant helping the user 24/7. Be concise and practical.",
                },
                {"role": "user", "content": message},
            ],
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("message", {}).get("content", "I had trouble generating a response.")

    def _fallback_reply(self, message: str) -> str:
        lower = message.lower().strip()

        if lower.startswith("note "):
            note = message[5:].strip()
            self._remember("note", note)
            return f"📝 Saved your note: {note}"

        if lower.startswith("todo ") or lower.startswith("task "):
            task = message.split(" ", 1)[1].strip()
            self._remember("task", task)
            return f"✅ Got it — I added this to your tasks: {task}"

        if "what are my tasks" in lower or "show tasks" in lower:
            tasks = [m["content"] for m in self.memory if m["kind"] == "task"]
            if not tasks:
                return "You have no saved tasks yet. Add one with: `todo <your task>`."
            return "Your tasks:\n- " + "\n- ".join(tasks)

        if "what do you remember" in lower or "show memory" in lower:
            if not self.memory:
                return "I don't have any saved memory yet."
            latest = self.memory[-5:]
            summary = [f"{item['kind']}: {item['content']}" for item in latest]
            return "Latest memory:\n- " + "\n- ".join(summary)

        return (
            "I'm online and ready 24/7. You can ask normal questions, or save things like:\n"
            "- `note buy groceries on friday`\n"
            "- `todo follow up with design team`"
        )

    def respond(self, message: str) -> str:
        self._remember("chat", message)

        try:
            return self._try_ollama(message)
        except (RuntimeError, urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            return self._fallback_reply(message)

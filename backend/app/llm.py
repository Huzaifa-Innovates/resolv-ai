import requests

from .config import (
    MAX_HISTORY_MESSAGES,
    MODEL_NAME,
    OLLAMA_URL,
    REQUEST_TIMEOUT,
    SYSTEM_PROMPT,
)


class LLMError(Exception):
    """Raised when we cannot get a response from the LLM."""

    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def ask_llm(user_message: str, history: list | None = None) -> str:
    """Send the conversation to Llama 3.2 via Ollama and return the reply text."""
    history = history or []

    # Keep only the most recent messages so the prompt stays small and fast
    recent = history[-MAX_HISTORY_MESSAGES:]

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for item in recent:
        messages.append({"role": item.role, "content": item.content})
    messages.append({"role": "user", "content": user_message})

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,  # wait for the full answer instead of streaming it
    }

    try:
        res = requests.post(OLLAMA_URL, json=payload, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.ConnectionError:
        raise LLMError(
            "Cannot connect to Ollama. Please make sure Ollama is running.", 503
        )
    except requests.exceptions.Timeout:
        raise LLMError("The AI model took too long to respond. Please try again.", 504)

    if res.status_code == 404:
        raise LLMError(
            f"Model '{MODEL_NAME}' not found. Run: ollama pull {MODEL_NAME}", 502
        )
    if res.status_code != 200:
        raise LLMError(f"Ollama returned an error (status {res.status_code}).", 502)

    try:
        return res.json()["message"]["content"].strip()
    except (KeyError, ValueError):
        raise LLMError("Received an unexpected response from Ollama.", 502)
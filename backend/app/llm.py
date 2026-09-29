import requests

from .config import MODEL_NAME, OLLAMA_URL, REQUEST_TIMEOUT, SYSTEM_PROMPT


class LLMError(Exception):
    """Raised when we cannot get a response from the LLM."""

    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def ask_llm(user_message: str) -> str:
    """Send a message to Llama 3.2 via Ollama and return the reply text."""
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
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
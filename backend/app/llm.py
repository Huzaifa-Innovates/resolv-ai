import logging

import requests

from .config import (
    MAX_HISTORY_MESSAGES,
    OLLAMA_GENERATE_URL,
    OLLAMA_URL,
    REQUEST_TIMEOUT,
    SYSTEM_PROMPT,
    load_model_settings,
)

logger = logging.getLogger("uvicorn.error")


class LLMError(Exception):
    """Raised when we cannot get a response from the LLM."""

    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def pick_models(user_message: str, settings: dict) -> list[str]:
    """Decide which models to try, in order. The user never sees this."""
    order = []
    fast = settings.get("fast_model")
    if (
        settings["use_fast_model_for_short_messages"]
        and fast
        and len(user_message) <= settings["short_message_max_chars"]
    ):
        order.append(fast)  # quick model for very short messages

    order.append(settings["default_model"])
    order.extend(settings["fallback_models"])
    return list(dict.fromkeys(order))  # remove duplicates, keep order


def preload_models() -> None:
    """Load the main models into memory at startup so the first reply is fast."""
    settings = load_model_settings()
    names = [settings["default_model"]]
    if settings["use_fast_model_for_short_messages"] and settings.get("fast_model"):
        names.append(settings["fast_model"])

    for name in dict.fromkeys(names):
        try:
            res = requests.post(
                OLLAMA_GENERATE_URL,
                json={"model": name, "keep_alive": settings["keep_alive"]},
                timeout=REQUEST_TIMEOUT,
            )
            if res.status_code == 200:
                logger.info("Preloaded model: %s", name)
            else:
                logger.warning("Could not preload model: %s (not installed?)", name)
        except requests.exceptions.RequestException:
            logger.warning("Could not preload model: %s", name)


def _call_ollama(model: str, messages: list, keep_alive: str) -> str:
    """Send one request to one model. Raises LLMError on any failure."""
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "keep_alive": keep_alive,
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
        raise LLMError(f"Model '{model}' is not installed. Run: ollama pull {model}", 502)
    if res.status_code != 200:
        raise LLMError(f"Ollama returned an error (status {res.status_code}).", 502)

    try:
        return res.json()["message"]["content"].strip()
    except (KeyError, ValueError):
        raise LLMError("Received an unexpected response from Ollama.", 502)


def ask_llm(user_message: str, history: list | None = None) -> str:
    """Pick a model automatically, call it, and fall back if it fails."""
    settings = load_model_settings()
    history = history or []
    recent = history[-MAX_HISTORY_MESSAGES:]

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for item in recent:
        messages.append({"role": item.role, "content": item.content})
    messages.append({"role": "user", "content": user_message})

    last_error = None
    for model in pick_models(user_message, settings):
        try:
            reply = _call_ollama(model, messages, settings["keep_alive"])
            logger.info("Answered with model: %s", model)
            return reply
        except LLMError as e:
            if e.status_code == 503:
                raise  # Ollama itself is off, so other models cannot help
            logger.warning("Model '%s' failed: %s Trying next model.", model, e.message)
            last_error = e

    raise last_error or LLMError("No model is configured.", 502)
import os

# Ollama connection only. Model settings and the system prompt
# are stored in the PostgreSQL database (table: app_settings).
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_URL = f"{OLLAMA_HOST}/api/chat"
OLLAMA_GENERATE_URL = f"{OLLAMA_HOST}/api/generate"
REQUEST_TIMEOUT = 120  # seconds per model attempt
MAX_HISTORY_MESSAGES = 10  # how many earlier messages to send to the LLM
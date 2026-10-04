import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .llm import LLMError, ask_llm, preload_models
from .schemas import ChatRequest, ChatResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Warm up models in the background so startup is not blocked
    threading.Thread(target=preload_models, daemon=True).start()
    yield


app = FastAPI(title="Resolv.ai Backend", lifespan=lifespan)

# Allow the React dev server to call this API from the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    """Simple endpoint to confirm the backend is running."""
    return {"status": "ok", "service": "Resolv.ai backend"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """Receive a user message, get an answer from the LLM, return it."""
    message = request.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    try:
        answer = ask_llm(message, request.history)
    except LLMError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

    return ChatResponse(response=answer)
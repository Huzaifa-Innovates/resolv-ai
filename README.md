# Resolv.ai: AI Customer Support Chatbot

Resolv.ai is an AI customer support chatbot for a fictional company, **Resolven Technologies**. It runs a real Large Language Model (**Llama 3.2**) **locally** through **Ollama**, so it needs no paid API and no internet connection once the model is downloaded.

> Resolven Technologies is fictional. All company details (services, hours, contact info) are made up for this demo and live in the system prompt.

## Features

- Real LLM responses from Llama 3.2 (no canned answers)
- Resolven Technologies support persona defined by a system prompt
- Politely declines questions unrelated to the company
- Loading indicator while the model generates a reply
- Clear chat button
- Friendly error messages when the backend or Ollama is unavailable
- Responsive, clean chat interface

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React (Vite), HTML, CSS, JavaScript, fetch API |
| Backend | Python, FastAPI, Uvicorn |
| LLM runtime | Ollama |
| Model | Llama 3.2 (3B) |
| Tools | VS Code, Git, GitHub |

## Architecture

```
React Frontend (localhost:5173)
        |  HTTP POST /chat  (JSON)
        v
FastAPI Backend (localhost:8000)
        |  HTTP POST /api/chat  (system prompt + user message)
        v
Ollama (localhost:11434)
        |
        v
Llama 3.2 (local LLM)
        |
        v
AI response returned back up the chain
```

**Flow:** the user types a message, React sends it to FastAPI, FastAPI adds the system prompt and forwards it to Ollama, Llama 3.2 generates a reply, and the reply travels back to the chat window.

## Project Structure

```
resolv-ai/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py      # settings + system prompt
│   │   ├── schemas.py     # request/response models
│   │   ├── llm.py         # talks to Ollama, handles errors
│   │   └── main.py        # FastAPI app and endpoints
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api.js         # all backend calls
│   │   ├── App.jsx        # chat UI and logic
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── index.html
│   └── package.json
├── .gitignore
└── README.md
```

## Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- Git
- Ollama (https://ollama.com/download)
- About 4 GB free RAM for the model (8 GB+ system RAM recommended)

Check your versions:

```bash
python --version
node --version
npm --version
git --version
ollama --version
```

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/resolv-ai.git
cd resolv-ai
```

### 2. Download the model (one time, about 2 GB)

```bash
ollama pull llama3.2
```

Make sure Ollama is running: open http://localhost:11434 and you should see "Ollama is running".

### 3. Backend setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

### 4. Frontend setup

```bash
cd frontend
npm install
```

## Running the Project

You need **three things running**: Ollama, the backend, and the frontend.

**Terminal 1: backend**

```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload
```

**Terminal 2: frontend**

```bash
cd frontend
npm run dev
```

Then open **http://localhost:5173**.

Interactive API docs are available at http://127.0.0.1:8000/docs.

## API

### `POST /chat`

Request:

```json
{ "message": "What services do you provide?" }
```

Response:

```json
{ "response": "Resolven Technologies offers..." }
```

Error responses:

| Status | Meaning |
|---|---|
| 422 | Invalid request (missing or empty message) |
| 502 | Ollama returned an error or the model is missing |
| 503 | Ollama is not running |
| 504 | The model took too long to respond |

### `GET /`

Health check. Returns `{"status": "ok", "service": "Resolv.ai backend"}`.

## How the Chatbot Behaves

The backend sends a **system prompt** to the LLM with every request. It defines the Resolv.ai persona, gives the model basic facts about Resolven Technologies, and tells it to politely decline unrelated questions. You can edit it in `backend/app/config.py`.

## Troubleshooting

| Problem | Fix |
|---|---|
| "Cannot connect to Ollama" | Start Ollama from the Start menu and check http://localhost:11434 |
| "Cannot reach the Resolv.ai backend" | Start the backend with `uvicorn app.main:app --reload` |
| First reply is very slow | Normal: the model is loading into RAM. Later replies are faster |
| Model not found (502) | Run `ollama pull llama3.2` |
| `uvicorn` not recognized | Activate the virtual environment first |
| CORS error in the browser | Make sure the frontend runs on port 5173 |

## Limitations

- No conversation memory: each message is answered independently
- Company knowledge lives in the system prompt, not in a knowledge base (no RAG)
- A small 3B model can occasionally ignore instructions or make mistakes
- Replies appear all at once instead of streaming word by word
- Speed depends on your laptop's CPU/GPU

## Future Improvements

- Conversation history so the bot remembers earlier messages
- Streaming responses
- RAG over real company documents
- User authentication and chat storage
- Docker and cloud deployment

## Git and GitHub Usage

Git tracks changes to the code locally. GitHub hosts the repository online.

```bash
git init                                # start tracking the folder
git add .                               # stage all files (respects .gitignore)
git commit -m "Initial commit"          # save a snapshot
git branch -M main                      # name the main branch
git remote add origin https://github.com/YOUR-USERNAME/resolv-ai.git
git push -u origin main                 # upload to GitHub
```

Later changes:

```bash
git add .
git commit -m "Describe your change"
git push
```

## Author

Your Name: Shaik Huzaifa
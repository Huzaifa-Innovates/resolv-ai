import { useEffect, useRef, useState } from "react";
import { sendMessage } from "./api";
import "./App.css";

const WELCOME_MESSAGE = {
  role: "ai",
  text: "Hi! I'm Resolv.ai, the virtual assistant for Resolven Technologies. How can I help you today?",
};

function App() {
  const [messages, setMessages] = useState([WELCOME_MESSAGE]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const bottomRef = useRef(null);

  // Auto-scroll to the newest message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function handleSend() {
    const text = input.trim();
    if (!text || loading) return;

    setMessages((prev) => [...prev, { role: "user", text }]);
    setInput("");
    setError("");
    setLoading(true);

    try {
      const reply = await sendMessage(text);
      setMessages((prev) => [...prev, { role: "ai", text: reply }]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter") {
      e.preventDefault();
      handleSend();
    }
  }

  function handleClear() {
    setMessages([WELCOME_MESSAGE]);
    setError("");
  }

  return (
    <div className="app">
      <div className="chat">
        <header className="header">
          <div className="brand">
            <div className="logo">R</div>
            <div>
              <h1>Resolv.ai</h1>
              <p>Resolven Technologies · Customer Support</p>
            </div>
          </div>
          <button className="clear-btn" onClick={handleClear}>
            Clear chat
          </button>
        </header>

        <main className="messages">
          {messages.map((m, i) => (
            <div key={i} className={`msg ${m.role}`}>
              {m.text}
            </div>
          ))}

          {loading && (
            <div className="msg ai typing" aria-label="Resolv.ai is typing">
              <span></span>
              <span></span>
              <span></span>
            </div>
          )}

          <div ref={bottomRef} />
        </main>

        {error && <div className="error">⚠️ {error}</div>}

        <div className="input-bar">
          <input
            type="text"
            placeholder="Ask about our services..."
            value={input}
            maxLength={2000}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={loading}
          />
          <button
            className="send-btn"
            onClick={handleSend}
            disabled={loading || !input.trim()}
          >
            {loading ? "Thinking..." : "Send"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
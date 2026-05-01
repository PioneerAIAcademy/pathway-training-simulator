import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import "./ChatPanel.css";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function ChatPanel({ open, onToggle }) {
  const [messages, setMessages] = useState([
    { from: "bot", text: "Hi! I'm here to help. Ask me anything about My Gatherings." }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSend(e) {
    e.preventDefault();
    const text = input.trim();
    if (!text || loading) return;

    setMessages((m) => [...m, { from: "user", text }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });
      const data = await res.json();
      setMessages((m) => [...m, { from: "bot", text: data.reply }]);
    } catch {
      setMessages((m) => [...m, { from: "bot", text: "Sorry, I couldn't reach the server. Please try again." }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      {!open && (
        <button className="chat-fab" onClick={onToggle} title="Ask a question">
          💬 Ask Question
        </button>
      )}

      <aside className={`chat-panel ${open ? "open" : ""}`}>
        <div className="chat-panel-header">
          <span>💬 Ask a Question</span>
          <button className="chat-panel-close" onClick={onToggle}>✕</button>
        </div>

        <div className="chat-messages">
          {messages.map((msg, i) => (
            <div key={i} className={`chat-bubble ${msg.from}`}>
              {msg.from === "bot"
                ? <ReactMarkdown>{msg.text}</ReactMarkdown>
                : msg.text}
            </div>
          ))}
          {loading && (
            <div className="chat-bubble bot chat-typing">
              <span /><span /><span />
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        <form className="chat-panel-form" onSubmit={handleSend}>
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your question…"
            disabled={loading}
          />
          <button type="submit" className="chat-panel-send" disabled={loading}>↑</button>
        </form>
      </aside>
    </>
  );
}

import { useState, useRef, useEffect } from "react";
import "./ChatPanel.css";

export default function ChatPanel({ open, onToggle }) {
  const [messages, setMessages] = useState([
    { from: "bot", text: "Hi! I'm here to help. Ask me anything about this simulation." }
  ]);
  const [input, setInput] = useState("");
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  function handleSend(e) {
    e.preventDefault();
    if (!input.trim()) return;
    setMessages((m) => [...m, { from: "user", text: input.trim() }]);
    setInput("");
    setTimeout(() => {
      setMessages((m) => [...m, { from: "bot", text: "Thanks for your question! AI responses coming soon." }]);
    }, 600);
  }

  return (
    <>
      {/* Floating chat bubble — only visible when panel is closed */}
      {!open && (
        <button className="chat-fab" onClick={onToggle} title="Ask a question">
          💬 Ask Question
        </button>
      )}

      {/* Panel — part of layout, pushes main content */}
      <aside className={`chat-panel ${open ? "open" : ""}`}>
        <div className="chat-panel-header">
          <span>💬 Ask a Question</span>
          <button className="chat-panel-close" onClick={onToggle}>✕</button>
        </div>

        <div className="chat-messages">
          {messages.map((msg, i) => (
            <div key={i} className={`chat-bubble ${msg.from}`}>
              {msg.text}
            </div>
          ))}
          <div ref={bottomRef} />
        </div>

        <form className="chat-panel-form" onSubmit={handleSend}>
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your question…"
          />
          <button type="submit" className="chat-panel-send">↑</button>
        </form>
      </aside>
    </>
  );
}

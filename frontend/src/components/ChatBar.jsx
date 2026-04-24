import { useState } from "react";
import "./ChatBar.css";

export default function ChatBar() {
  const [input, setInput] = useState("");
  const [reply, setReply] = useState(null);

  function handleSubmit(e) {
    e.preventDefault();
    if (!input.trim()) return;
    setReply("Not implemented yet.");
    setInput("");
  }

  return (
    <div className="chat-bar">
      {reply && (
        <div className="chat-reply">
          <strong>Assistant:</strong> {reply}
        </div>
      )}
      <form onSubmit={handleSubmit} className="chat-form">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question…"
        />
        <button type="submit" className="send-btn" title="Send">↑</button>
      </form>
    </div>
  );
}

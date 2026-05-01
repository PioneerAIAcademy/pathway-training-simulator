import { useEffect, useState } from "react";
import byuLogo from "../../images/pathway.png";
import "./Sidebar.css";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function Sidebar({
  open, onToggle, started, phase, simStep, totalSteps,
  selectedSim, onSimChange, onStart,
}) {
  const [simulations, setSimulations] = useState([]);

  useEffect(() => {
    fetch(`${API}/api/simulations`)
      .then((r) => r.json())
      .then((data) => {
        setSimulations(data);
        if (!selectedSim && data.length) onSimChange(data[0].id);
      });
  }, []);

  const total = totalSteps || 1;
  const progress = phase === "end" ? 1 : (simStep + 1) / total;
  const progressLabel =
    phase === "end"
      ? "Simulation complete"
      : `Step ${simStep + 1} of ${total}`;

  return (
    <aside className={`sidebar ${open ? "open" : "closed"}`}>
      <button
        className="sidebar-toggle"
        onClick={onToggle}
        title={open ? "Collapse sidebar" : "Expand sidebar"}
      >
        ☰
      </button>

      <div className="sidebar-inner">
        <div className="sidebar-logo">
          <img src={byuLogo} alt="BYU Pathway Worldwide" />
        </div>
        <hr />

        <span className="sidebar-label">Choose a simulation:</span>
        <select
          className="sidebar-select"
          value={selectedSim || ""}
          onChange={(e) => onSimChange(e.target.value)}
        >
          {simulations.map((s) => (
            <option key={s.id} value={s.id}>{s.name}</option>
          ))}
        </select>

        <button className="sidebar-start-btn" onClick={onStart}>
          ▶ Start Simulation
        </button>

        {started && (
          <div className="sidebar-footer">
            <div className="progress-label">{progressLabel}</div>
            <div className="progress-track">
              <div
                className="progress-fill"
                style={{ width: `${Math.round(progress * 100)}%` }}
              />
            </div>
          </div>
        )}
      </div>
    </aside>
  );
}

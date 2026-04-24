import { useState, useRef, useEffect } from "react";
import "./SettingsMenu.css";

export default function SettingsMenu({ theme, onThemeChange }) {
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  // Close when clicking outside
  useEffect(() => {
    function handleClick(e) {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    }
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  return (
    <div className="settings-menu" ref={ref}>
      <button
        className="settings-gear"
        onClick={() => setOpen((o) => !o)}
        title="Settings"
      >
        ⚙
      </button>

      {open && (
        <div className="settings-dropdown">
          {/* Theme section */}
          <div className="settings-section-label">Theme</div>
          <div className="theme-options">
            <button
              className={`theme-btn ${theme === "light" ? "active" : ""}`}
              onClick={() => onThemeChange("light")}
              title="Light"
            >
              ☀
            </button>
            <button
              className={`theme-btn ${theme === "dark" ? "active" : ""}`}
              onClick={() => onThemeChange("dark")}
              title="Dark"
            >
              ☽
            </button>
            <button
              className={`theme-btn ${theme === "system" ? "active" : ""}`}
              onClick={() => onThemeChange("system")}
              title="System"
            >
              🖥
            </button>
          </div>

        </div>
      )}
    </div>
  );
}

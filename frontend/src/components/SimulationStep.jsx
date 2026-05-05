import { useEffect, useState, useRef } from "react";
import "./SimulationStep.css";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function SimulationStep({ simId, simStep, onCorrect, onTotalSteps, onNavigate }) {
  const [steps, setSteps] = useState([]);
  const [error, setError] = useState(null);
  const [successToast, setSuccessToast] = useState(null);
  const imgRef = useRef(null);

  useEffect(() => {
    if (!simId) return;
    fetch(`${API}/api/simulations/${simId}/steps`)
      .then((r) => r.json())
      .then((data) => {
        setSteps(data);
        onTotalSteps(data.length);
      });
  }, [simId]);

  if (!steps.length) return <p className="loading">Loading…</p>;

  const step = steps[simStep];

  function handleClick(e) {
    if (!step.hotspot) return;
    const rect = imgRef.current.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width;
    const y = (e.clientY - rect.top) / rect.height;
    const { x1, y1, x2, y2 } = step.hotspot;

    if (x >= x1 && x <= x2 && y >= y1 && y <= y2) {
      setError(null);
      setSuccessToast(step.correct);
      setTimeout(() => {
        setSuccessToast(null);
        onCorrect(step.correct, steps.length);
      }, 1500);
    } else {
      setError(step.incorrect);
      setTimeout(() => setError(null), 2000);
    }
  }

  function handleContinue() {
    onCorrect(step.correct, steps.length);
  }

  return (
    <div className="sim-step">
      <p className="step-label">Step {simStep + 1} of {steps.length}</p>

      {error && <div className="error-toast">❌ {error}</div>}
      {successToast && <div className="success-toast">✅ {successToast}</div>}

      <div className="instruction">
        <span className="instruction-icon">📋</span>
        <span dangerouslySetInnerHTML={{ __html: step.intro_text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>") }} />
      </div>

      {step.slide_filename && (
        <div className="image-wrapper">
          <img
            ref={imgRef}
            src={`${API}/images/${step.slide_filename}`}
            alt={`Step ${simStep + 1}`}
            onClick={step.is_completion ? undefined : handleClick}
            style={{ cursor: step.is_completion ? "default" : "crosshair" }}
            draggable={false}
          />
        </div>
      )}

      {step.is_completion && (
        <button className="continue-btn" onClick={handleContinue}>
          Continue →
        </button>
      )}

      <div className="step-nav">
        <button
          className="nav-arrow"
          onClick={() => onNavigate(-1)}
          disabled={simStep === 0}
          title="Previous step"
        >‹</button>
        <span className="step-label">Step {simStep + 1} of {steps.length}</span>
        <button
          className="nav-arrow"
          onClick={() => onNavigate(1)}
          disabled={simStep === steps.length - 1}
          title="Next step"
        >›</button>
      </div>
    </div>
  );
}

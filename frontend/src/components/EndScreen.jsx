import "./EndScreen.css";

export default function EndScreen({ prevSuccess, onStartOver, onChooseSim }) {
  return (
    <div className="end-screen">
      {prevSuccess && (
        <div className="success-banner">✓ {prevSuccess}</div>
      )}

      <div className="end-card">
        <div className="check-circle">✓</div>
        <h2>Simulation Complete!</h2>
        <p>You finished all steps. Great work.</p>

        <div className="end-actions">
          <button className="btn-secondary" onClick={onStartOver}>Start Over</button>
          <button className="btn-primary" onClick={onChooseSim}>Choose Simulation</button>
        </div>
      </div>
    </div>
  );
}

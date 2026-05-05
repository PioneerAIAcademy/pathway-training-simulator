import { useState, useEffect } from "react";
import Sidebar from "./components/Sidebar";
import SimulationStep from "./components/SimulationStep";
import EndScreen from "./components/EndScreen";
import SettingsMenu from "./components/SettingsMenu";
import ChatPanel from "./components/ChatPanel";
import byuLogo from "../images/pathway-horizontal-logo.png";
import "./App.css";

export default function App() {
  const [started, setStarted] = useState(false);
  const [phase, setPhase] = useState("simulation");
  const [simStep, setSimStep] = useState(0);
  const [prevSuccess, setPrevSuccess] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [theme, setTheme] = useState("light");
  const [chatOpen, setChatOpen] = useState(false);
  const [selectedSim, setSelectedSim] = useState(null);
  const [totalSteps, setTotalSteps] = useState(1);

  useEffect(() => {
    const resolved =
      theme === "system"
        ? window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"
        : theme;
    document.documentElement.setAttribute("data-theme", resolved);
  }, [theme]);

  function startSim() {
    setStarted(true);
    setPhase("simulation");
    setSimStep(0);
    setPrevSuccess(null);
  }

  function handleStepCorrect(successMsg, total) {
    const next = simStep + 1;
    if (next >= total) {
      setPhase("end");
      setPrevSuccess(successMsg);
    } else {
      setSimStep(next);
      setPrevSuccess(successMsg);
    }
  }

  function handleReset() {
    setStarted(false);
    setPhase("simulation");
    setSimStep(0);
    setPrevSuccess(null);
  }

  function handleChooseSim() {
    setStarted(false);
    setPhase("simulation");
    setSimStep(0);
    setPrevSuccess(null);
    setSidebarOpen(true);
  }

  function handleNavigate(delta) {
    const next = simStep + delta;
    if (next >= 0 && next < totalSteps) {
      setSimStep(next);
      setPrevSuccess(null);
    }
  }

  function handleSimChange(simId) {
    setSelectedSim(simId);
    if (started) {
      setSimStep(0);
      setPrevSuccess(null);
      setPhase("simulation");
    }
  }

  const showChat = true;

  return (
    <div className="app-shell">
      <header className="top-bar">
        <div className="top-bar-inner">
          <a href="/" className="top-bar-logo-link">
            <img src={byuLogo} alt="BYU Pathway Worldwide" className="top-bar-logo" />
          </a>
          <div className="top-bar-title-wrap">
            <h1 className="top-bar-title">Software Training Simulator</h1>
          </div>
          <SettingsMenu theme={theme} onThemeChange={setTheme} />
        </div>
      </header>

      <div className="body-row">
        <Sidebar
          open={sidebarOpen}
          onToggle={() => setSidebarOpen((o) => !o)}
          started={started}
          phase={phase}
          simStep={simStep}
          totalSteps={totalSteps}
          selectedSim={selectedSim}
          onSimChange={handleSimChange}
          onStart={startSim}
        />

        <main className="main-content">
          {!started && (
            <div className="welcome">
              <div className="welcome-card">
                <h1>Software Training Simulator</h1>
                <p>
                  Practice navigating software systems before working with real students.
                </p>
                <div className="welcome-section-title">How to use the Simulator</div>
                <div className="welcome-steps">
                  <div className="welcome-step">
                    <span className="welcome-step-num">1</span>
                    <span>Use the <strong>sidebar on the left</strong> to choose a simulation from the dropdown.</span>
                  </div>
                  <div className="welcome-step">
                    <span className="welcome-step-num">2</span>
                    <span>Click <strong>▶ Start Simulation</strong> in the sidebar to begin.</span>
                  </div>
                  <div className="welcome-step">
                    <span className="welcome-step-num">3</span>
                    <span>Read the instruction above the screenshot, then <strong>click the correct area</strong> in the image.</span>
                  </div>
                </div>

                <div className="welcome-divider" />

                <div className="welcome-section-title">Need Help?</div>
                <div className="welcome-steps">
                  <div className="welcome-step">
                    <span className="welcome-step-num">4</span>
                    <span>Have a question about how to use the simulator? Click the <strong>💬 Ask Question</strong> button at the bottom-right of the screen.</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {started && phase === "simulation" && (
            <SimulationStep
              simId={selectedSim}
              simStep={simStep}
              onCorrect={handleStepCorrect}
              onTotalSteps={setTotalSteps}
              onNavigate={handleNavigate}
            />
          )}

          {started && phase === "end" && (
            <EndScreen
              prevSuccess={prevSuccess}
              onStartOver={startSim}
              onChooseSim={handleChooseSim}
            />
          )}
        </main>

        {showChat && (
          <ChatPanel open={chatOpen} onToggle={() => setChatOpen((o) => !o)} />
        )}
      </div>
    </div>
  );
}

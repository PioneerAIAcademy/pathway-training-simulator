# BYU Pathway – My Gatherings Training Simulator

An interactive training simulator that teaches BYU Pathway missionaries how to navigate the **My Gatherings** app through step-by-step click simulations.

Missionaries practice on real app screenshots and get immediate feedback before using the live system.

---

## Features

- Click-based simulation on actual My Gatherings screenshots
- Immediate correct / incorrect feedback
- Chat intro phase before the simulation begins
- Progress tracking in the sidebar
- Driven by an Excel spreadsheet — add new simulations without touching code

---

## Project Structure

```
simulation_chatbot/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── My_Gatherings_Simulation.xlsx   # Simulation data (steps, slides, responses)
├── byu-pw-yellow.svg               # BYU Pathway logo (gold, used in sidebar)
├── byu-pw-stackedgray.svg          # BYU Pathway logo (gray, original)
└── Screenshot/                     # App screenshots used in the simulation
    ├── slide3_mygatherings_home.png
    ├── slide4_students_dropdown.png
    └── slide5_student_list.png
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/pathway-training-simulator.git
cd pathway-training-simulator
```

### 2. Create and activate a virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate        # Mac / Linux
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`.

---

## Excel Data Format

The simulation steps are read from `My_Gatherings_Simulation.xlsx`, sheet **"Simulation - View Student List"**.

| Column | Description |
|--------|-------------|
| A – Introductory Text | Prompt shown to the missionary |
| B – Slide Filename | Screenshot filename from the `Screenshot/` folder |
| C – Words to Click On | The correct hotspot label |
| D – Response if Correct | Feedback shown on the next screen |
| E – Response if Incorrect | Feedback shown when wrong area is clicked |

- **Rows 2–3**: Chat intro phase (handled as a chatbot conversation)
- **Rows 4–5**: Clickable screenshot simulation steps
- **Row 6**: End screen

---

## Requirements

- Python 3.11+
- See `requirements.txt` for package versions

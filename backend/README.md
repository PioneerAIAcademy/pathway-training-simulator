# Backend — FastAPI Server

The backend serves simulation steps from an Excel file and exposes screenshot images as static files.

---

## Requirements

- Python 3.11+
- pip

---

## Setup

**1. Create the virtual environment (Python 3.11 required)**
```bash
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -m venv .venv
```

**2. Activate it**
```bash
source .venv/bin/activate        # Mac / Linux
.venv\Scripts\activate           # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Start the server**
```bash
uvicorn main:app --reload --port 8000
```

The server runs at `http://localhost:8000`.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/simulations` | List available simulations |
| GET | `/api/simulations/{id}/steps` | Get all steps for a simulation |
| GET | `/images/{filename}` | Serve a screenshot image |

---

## File Structure

```
backend/
├── main.py                         # FastAPI app
├── requirements.txt                # Python dependencies
├── My_Gatherings_Simulation.xlsx   # Simulation content (Excel)
└── Screenshot/                     # Screenshot images
```

---

## Excel Format

Sheet name: `Simulation - View Student List`

| Column | Description |
|---|---|
| `intro_text` | Instruction shown to the missionary |
| `slide_filename` | Screenshot filename in `Screenshot/` |
| `click_target` | Description of the correct click target |
| `correct_response` | Message shown on a correct click |
| `incorrect_response` | Message shown on an incorrect click |

Hotspot coordinates (fractional x1, y1, x2, y2) are defined directly in `main.py` in the `HOTSPOT_FRACTIONS` dictionary.

---

## Dependencies

| Package | Purpose |
|---|---|
| `fastapi` | Web framework |
| `uvicorn` | ASGI server |
| `pandas` | Read Excel data |
| `openpyxl` | Excel file engine for pandas |
| `Pillow` | Image processing |

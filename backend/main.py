from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
import pandas as pd
import os
import re
from openai import OpenAI
from dotenv import load_dotenv
from slide_renderer import render_slides, build_slide_map
from rag import RAGManager

load_dotenv()

app = FastAPI()

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_origin_regex=r"http://localhost:\d+|https://.*\.onrender\.com",
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).parent
EXCEL_FILE = BASE_DIR / "My_Gatherings_Simulation (orignal).xlsx"
AI_EXCEL_FILE = BASE_DIR / "My_Gatherings_Simulation (with ai link).xlsx"
PPTX_FILE = BASE_DIR / "Screenshot" / "Screen shoits for My Gatherings Simulations 1 and 2.pptx"
GENERATED_DIR = BASE_DIR / "generated_slides"

# ── Slide extraction at startup ───────────────────────────────────────────────
slide_files = render_slides(str(PPTX_FILE), str(GENERATED_DIR))
slide_map = build_slide_map(str(PPTX_FILE))

# ── RAG: load article PDFs from Excel hyperlinks ─────────────────────────────
rag = RAGManager(str(AI_EXCEL_FILE))
_openai_key = os.getenv("OPENAI_API_KEY", "")
openai_client = OpenAI(api_key=_openai_key) if _openai_key else None

app.mount("/images", StaticFiles(directory=str(GENERATED_DIR)), name="images")

# ── Hotspot coordinates ───────────────────────────────────────────────────────
# Fractional (x1, y1, x2, y2) relative to the extracted image dimensions.
# Update ("sim-2", 3) and ("sim-2", 4) after visually confirming rendered slides.
HOTSPOTS: dict = {
    ("sim-1", 1): (0.610, 0.044, 0.708, 0.117),
    ("sim-1", 2): (0.607, 0.109, 0.726, 0.185),
    ("sim-2", 1): (0.610, 0.044, 0.708, 0.117),
    ("sim-2", 2): (0.607, 0.109, 0.726, 0.185),
    ("sim-2", 3): (0.01,  0.26,  0.16,  0.30),   # Export Student List link
    ("sim-2", 4): (0.02,  0.50,  0.17,  0.62),   # Export List to Excel button
}

SIM_NAMES: dict = {
    "sim-1": "View Current Student List",
    "sim-2": "Export Student List",
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def _parse_ppt_ref(text: str) -> tuple | None:
    """Extract (sim_key, slide_num) from 'Sim 1 View ... - Slide 2' strings."""
    if not text or text.strip().upper() in ("NAN", "N/A"):
        return None
    m = re.search(r"Slide\s+(\d+)", text, re.IGNORECASE)
    if not m:
        return None
    n = int(m.group(1))
    lower = text.lower()
    if "sim 1" in lower:
        return ("sim-1", n)
    if "sim 2" in lower:
        return ("sim-2", n)
    return None


def load_all_simulations() -> dict:
    df = pd.read_excel(EXCEL_FILE, sheet_name="Simulation - View Student List", header=0)
    df.columns = [
        "sim_id", "sim_name", "ppt_file", "ppt_slide_ref",
        "intro_text", "slide_filename", "click_target", "correct", "incorrect",
    ]
    simulations: dict = {}

    for _, row in df.iterrows():
        raw = str(row["sim_id"]).strip()
        if not raw or raw.upper() in ("NAN", "N/A") or "End" in raw:
            continue

        m = re.match(r"Sim\s+(\d+)", raw, re.IGNORECASE)
        if not m:
            continue
        sim_key = f"sim-{m.group(1)}"

        ppt_ref = _parse_ppt_ref(str(row.get("ppt_slide_ref", "")))

        img_filename = None
        if ppt_ref:
            pptx_num = slide_map.get(ppt_ref)
            if pptx_num and pptx_num in slide_files:
                img_filename = slide_files[pptx_num]

        click_target = str(row["click_target"]).strip()
        is_completion = click_target.upper() in ("N/A", "NAN")
        hotspot_val = HOTSPOTS.get(ppt_ref) if (ppt_ref and not is_completion) else None

        def _clean(val):
            s = str(val).strip()
            return "" if s.upper() in ("NAN", "N/A") else s

        step = {
            "intro_text": _clean(row["intro_text"]),
            "slide_filename": img_filename,
            "correct": _clean(row["correct"]),
            "incorrect": _clean(row["incorrect"]),
            "hotspot": (
                {"x1": hotspot_val[0], "y1": hotspot_val[1],
                 "x2": hotspot_val[2], "y2": hotspot_val[3]}
                if hotspot_val else None
            ),
            "is_completion": is_completion,
        }

        simulations.setdefault(sim_key, []).append(step)

    # sim-1 ends naturally after the last click step; drop the completion slide
    if "sim-1" in simulations:
        simulations["sim-1"] = [s for s in simulations["sim-1"] if not s["is_completion"]]

    return simulations


ALL_SIMS = load_all_simulations()

# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/api/simulations")
def get_simulations():
    return [{"id": k, "name": SIM_NAMES.get(k, k)} for k in ALL_SIMS]


@app.get("/api/simulations/{sim_id}/steps")
def get_steps(sim_id: str):
    steps = ALL_SIMS.get(sim_id)
    if steps is None:
        raise HTTPException(status_code=404, detail="Simulation not found")
    return steps


class ChatRequest(BaseModel):
    message: str


@app.post("/api/chat")
def chat(body: ChatRequest):
    if not openai_client:
        raise HTTPException(status_code=503, detail="OPENAI_API_KEY is not configured on the server.")
    context = rag.get_context()
    completion = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a support assistant for BYU Pathway Worldwide missionaries. "
                    "You help with two things:\n"
                    "1. How to use this Training Simulator app.\n"
                    "2. How to use the My Gatherings system.\n\n"

                    "== About this Training Simulator ==\n"
                    "This is the My Gatherings Training Simulator, a web app that helps "
                    "missionaries practice navigating My Gatherings before working with real students.\n"
                    "- The LEFT SIDEBAR lets you choose a simulation from a dropdown and click "
                    "'▶ Start Simulation' to begin.\n"
                    "- There are two simulations available: 'View Current Student List' and "
                    "'Export Student List'.\n"
                    "- Each simulation shows a screenshot of My Gatherings. Read the instruction "
                    "at the top, then click the correct area in the screenshot.\n"
                    "- If you click the correct area, you move to the next step.\n"
                    "- If you click the wrong area, you get an error message and can try again.\n"
                    "- When the simulation is complete, you can click 'Start Over' to repeat it "
                    "or 'Choose Simulation' to pick a different one.\n"
                    "- The '💬 Ask Question' button (bottom right) opens this chat panel where "
                    "you can ask for help at any time.\n\n"

                    "== Rules ==\n"
                    "1. Answer questions about how to use this simulator app.\n"
                    "2. Answer questions about My Gatherings using the reference material below.\n"
                    "3. If a question is completely unrelated to the simulator or My Gatherings "
                    "(e.g. general knowledge, math, other topics), politely decline and remind "
                    "the user what you can help with.\n"
                    "4. For My Gatherings questions, base your answer on the reference material. "
                    "If the answer is not there, say: 'I don't have information on that. "
                    "Please contact your supervisor or check the official BYU Pathway resources.'\n"
                    "5. Be concise, clear, and friendly.\n\n"
                    "== Formatting Rules ==\n"
                    "Always format your responses using markdown so they render well in the chat:\n"
                    "- Use **bold** for important terms or UI elements (e.g. **Students**, **Export**).\n"
                    "- Use bullet lists (-) for steps or multiple items.\n"
                    "- Use numbered lists (1. 2. 3.) for ordered steps.\n"
                    "- Use ## for section headings when the answer has multiple sections.\n"
                    "- Keep responses concise — avoid long paragraphs.\n\n"
                    "== My Gatherings Reference Material ==\n\n"
                    f"{context}"
                ),
            },
            {"role": "user", "content": body.message},
        ],
    )
    return {"reply": completion.choices[0].message.content}

import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BYU Pathway Training Simulator",
    page_icon="🎓",
    layout="wide",
)

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
EXCEL_FILE = BASE_DIR / "My_Gatherings_Simulation.xlsx"
SCREENSHOT_DIR = BASE_DIR / "Screenshot"

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #002E5D;
    padding-top: 1.5rem;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {
    color: #FFFFFF !important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    background-color: #003d7a;
    border: 1px solid #FFCC00;
    color: white;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(255,204,0,0.3);
}
[data-testid="stSidebar"] [data-testid="stButton"] > button[kind="primary"] {
    background-color: #FFCC00;
    color: #002E5D;
    font-weight: 700;
    border: none;
    border-radius: 6px;
}
[data-testid="stSidebar"] [data-testid="stButton"] > button[kind="primary"]:hover {
    background-color: #e6b800;
    color: #002E5D;
}
[data-testid="stSidebar"] [data-testid="stProgressBar"] > div > div {
    background-color: #FFCC00;
}
h1 { color: #002E5D; }
</style>
""", unsafe_allow_html=True)

# ── Image resizing ────────────────────────────────────────────────────────────
MAX_WIDTH = 1200

@st.cache_data
def load_image(path: str) -> Image.Image:
    img = Image.open(path)
    w, h = img.size
    if w > MAX_WIDTH:
        img = img.resize((MAX_WIDTH, int(h * MAX_WIDTH / w)), Image.LANCZOS)
    return img

# ── Hotspots as fractions (left, top, right, bottom) ─────────────────────────
HOTSPOT_FRACTIONS = {
    0: (0.610, 0.044, 0.708, 0.117),   # "Students" nav item — slide3
    1: (0.607, 0.109, 0.726, 0.185),   # "Students - Current" dropdown — slide4
}

def in_hotspot(coords: dict, step: int, img: Image.Image) -> bool:
    x, y = coords["x"], coords["y"]
    w, h = img.size
    fx1, fy1, fx2, fy2 = HOTSPOT_FRACTIONS[step]
    return (fx1 * w <= x <= fx2 * w) and (fy1 * h <= y <= fy2 * h)

# ── Load simulation steps from Excel (rows 4-5) ───────────────────────────────
COLS = ["intro_text", "slide_filename", "click_target", "correct_response", "incorrect_response"]

@st.cache_data
def load_sim_steps() -> list[dict]:
    df = pd.read_excel(
        EXCEL_FILE,
        sheet_name="Simulation - View Student List",
        header=0,
        skiprows=[1, 2],
        nrows=2,
    )
    df.columns = COLS
    return [
        {
            "intro_text": str(row["intro_text"]).strip(),
            "slide":      SCREENSHOT_DIR / str(row["slide_filename"]).strip(),
            "correct":    str(row["correct_response"]).strip(),
            "incorrect":  str(row["incorrect_response"]).strip(),
        }
        for _, row in df.iterrows()
    ]

SIM_STEPS = load_sim_steps()

# ── Session state ─────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "started":      False,
        "phase":        "simulation",  # "simulation" | "end"
        "sim_step":     0,
        "prev_success": None,          # success message carried from previous step
        "feedback":     None,          # None | "incorrect"
        "completed":    False,
        "chat_reply":   None,          # placeholder chat response
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_state()

def reset():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_state()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    col = st.columns([1, 2, 1])[1]
    col.image(str(BASE_DIR / "byu-pw-yellow.svg"), width="stretch")
    st.markdown("### Training Simulator")
    st.markdown("---")

    st.selectbox("Choose a simulation:", options=["View Student List"])
    st.markdown("")

    if st.button("▶ Start Simulation", use_container_width=True, type="primary"):
        reset()
        st.session_state.started = True

    if st.session_state.started:
        st.markdown("---")
        if st.session_state.phase == "simulation":
            sim_step = st.session_state.sim_step
            st.progress((sim_step + 1) / 2, text=f"Step {sim_step + 1} of 2")
        elif st.session_state.phase == "end":
            st.progress(1.0, text="Complete!")

# ── Main area ─────────────────────────────────────────────────────────────────
st.markdown("# My Gatherings Training Simulator")
st.markdown("---")

if not st.session_state.started:
    st.markdown(
        """
        Welcome to the **BYU Pathway Missionary Training Simulator**.

        This tool helps you practice navigating the **My Gatherings** app before using it with real students.

        👈 Select a simulation from the sidebar and click **Start Simulation** to begin.
        """
    )
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# PHASE: END SCREEN
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.phase == "end":
    # Show success message carried from the last simulation step
    if st.session_state.prev_success:
        st.success(f"✅ {st.session_state.prev_success}")
        st.markdown("")

    if st.session_state.completed:
        st.success("🎉 Awesome work! You've completed this simulation. Feel free to try another one anytime!")
        if st.button("← Back to Start"):
            reset()
    else:
        st.markdown("### Would you like to do another simulation or practice this one again?")
        st.markdown("")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Start Over", use_container_width=True):
                reset()
                st.session_state.started = True
        with col2:
            if st.button("✅ Continue", use_container_width=True, type="primary"):
                st.session_state.completed = True
                st.rerun()
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# PHASE: SIMULATION STEPS
# ══════════════════════════════════════════════════════════════════════════════
step_data = SIM_STEPS[st.session_state.sim_step]

st.markdown(f"### Step {st.session_state.sim_step + 1} of 2")

# Show success message carried from previous step
if st.session_state.prev_success:
    st.success(f"✅ {st.session_state.prev_success}")

st.info(step_data["intro_text"])
st.markdown("")

img = load_image(str(step_data["slide"]))
st.caption("🖱️ Click directly on the app screenshot to navigate.")
coords = streamlit_image_coordinates(img, key=f"img_step_{st.session_state.sim_step}")

# Error shown AFTER the image — no second rerun needed, image stays stable
if coords is not None:
    if in_hotspot(coords, st.session_state.sim_step, img):
        # Correct — advance immediately with one rerun
        success_msg = step_data["correct"]
        next_step = st.session_state.sim_step + 1
        if next_step >= len(SIM_STEPS):
            st.session_state.phase = "end"
            st.session_state.prev_success = success_msg
        else:
            st.session_state.sim_step = next_step
            st.session_state.prev_success = success_msg
        st.session_state.feedback = None
        st.rerun()
    else:
        # Incorrect — set state and show error in this same rerun, no extra rerun
        st.session_state.feedback = "incorrect"

if st.session_state.feedback == "incorrect":
    st.error(f"❌ {step_data['incorrect']}")

# ── Chat bar (placeholder) ────────────────────────────────────────────────────
chat_msg = st.chat_input("Ask a question…")
if chat_msg:
    st.session_state.chat_reply = "Not implemented yet"
    st.rerun()

if st.session_state.chat_reply:
    with st.chat_message("assistant"):
        st.write(st.session_state.chat_reply)

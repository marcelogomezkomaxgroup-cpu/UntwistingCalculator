import streamlit as st

st.set_page_config(page_title="Zeta Torsion Controller", page_icon="🌀", layout="wide")

# --- CUSTOM CSS (Komax Green & Red + Large Text) ---
st.markdown("""
    <style>
    div.stButton > button:first-child {
        height: 3.5em;
        font-size: 20px;
        font-weight: bold;
        border-radius: 10px;
    }
    /* Negative Buttons */
    div[data-testid="column"]:nth-of-type(1) button, div[data-testid="column"]:nth-of-type(2) button,
    div[data-testid="column"]:nth-of-type(3) button, div[data-testid="column"]:nth-of-type(4) button,
    div[data-testid="column"]:nth-of-type(5) button {
        background-color: #d32f2f; color: white;
    }
    /* Positive Buttons */
    div[data-testid="column"]:nth-of-type(7) button, div[data-testid="column"]:nth-of-type(8) button,
    div[data-testid="column"]:nth-of-type(9) button, div[data-testid="column"]:nth-of-type(10) button,
    div[data-testid="column"]:nth-of-type(11) button {
        background-color: #2e7d32; color: white;
    }
    </style>
    """, unsafe_allow_html=True)

if 'lay_length' not in st.session_state:
    st.session_state.lay_length = 1000.0

def adjust_val(amount):
    st.session_state.lay_length = max(100.0, min(4950.0, st.session_state.lay_length + amount))

# --- TOP SECTION: THE TICKER BAR ---
st.title("🌀 Zeta Torsion Controller")

# The "Ticker" - It moves automatically when session_state.lay_length changes
# We use a progress bar to represent the 100mm to 4950mm range
progress_percentage = (st.session_state.lay_length - 100) / (4950 - 100)
st.write(f"**Lay Length Position Tracker:** {st.session_state.lay_length:.0f} mm")
st.progress(progress_percentage)

# Digital Readouts
p_mm = st.session_state.lay_length
col_m1, col_m2 = st.columns(2)
col_m1.metric("CURRENT MM", f"{p_mm:.0f}")
col_m2.metric("CURRENT INCH", f"{(p_mm * 0.0393701):.3f}")

st.write("---")

# --- THE CONTROL PANEL ---
neg_vals = [-1000, -500, -50, -5, -1]
pos_vals = [1, 5, 50, 500, 1000]

# Wide layout with a gap in the middle
cols = st.columns([1, 1, 1, 1, 1, 0.5, 1, 1, 1, 1, 1])

for i, val in enumerate(neg_vals):
    if cols[i].button(str(val), key=f"neg_{i}"):
        adjust_val(val)
        st.rerun()

cols[5].write("") # The Spacer

for i, val in enumerate(pos_vals):
    if cols[i+6].button(f"+{val}", key=f"pos_{i}"):
        adjust_val(val)
        st.rerun()

# --- BOTTOM SECTION: TOTALS ---
st.write("---")
total_mm = st.number_input("TOTAL WIRE LENGTH (MM)", value=10000.0)
untwist_enabled = st.toggle("Untwisting Active", value=True)

if untwist_enabled:
    rotations = total_mm / p_mm
    st.success(f"### TOTAL UNTWIST ROTATIONS: {rotations:.3f}")
else:
    st.error("SYSTEM BYPASS")

if st.button("RESET TO 1000mm"):
    st.session_state.lay_length = 1000.0
    st.rerun()

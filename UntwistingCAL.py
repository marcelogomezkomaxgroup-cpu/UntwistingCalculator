import streamlit as st

st.set_page_config(page_title="Zeta Torsion Controller", page_icon="🌀", layout="wide")

# --- CUSTOM CSS (Industrial Style) ---
st.markdown("""
    <style>
    div.stButton > button:first-child {
        height: 3.5em;
        font-size: 20px;
        font-weight: bold;
        border-radius: 10px;
    }
    /* Negative Side (Red) */
    div[data-testid="column"]:nth-of-type(1) button, div[data-testid="column"]:nth-of-type(2) button,
    div[data-testid="column"]:nth-of-type(3) button, div[data-testid="column"]:nth-of-type(4) button,
    div[data-testid="column"]:nth-of-type(5) button {
        background-color: #d32f2f; color: white;
    }
    /* Positive Side (Green) */
    div[data-testid="column"]:nth-of-type(7) button, div[data-testid="column"]:nth-of-type(8) button,
    div[data-testid="column"]:nth-of-type(9) button, div[data-testid="column"]:nth-of-type(10) button,
    div[data-testid="column"]:nth-of-type(11) button {
        background-color: #2e7d32; color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session State
if 'lay_length' not in st.session_state:
    st.session_state.lay_length = 1000.0

def adjust_val(amount):
    # Limits set to your original slider range (100 to 4950)
    st.session_state.lay_length = max(100.0, min(4950.0, st.session_state.lay_length + amount))

# --- HEADER & TICKER ---
st.title("🌀 Zeta Torsion Controller")

# The Ticker Bar
# Normalizing 100-4950 to 0.0-1.0 for the progress bar
progress = (st.session_state.lay_length - 100) / (4950 - 100)
st.progress(progress)

# Digital Readouts
p_mm = st.session_state.lay_length
p_inch = p_mm * 0.0393701

col_m1, col_m2 = st.columns(2)
col_m1.metric("LAY LENGTH (P)", f"{p_mm:.0f} mm")
col_m2.metric("INCHES", f"{p_inch:.3f} in")

st.write("---")

# --- CONTROL PANEL (NEGATIVES | GAP | POSITIVES) ---
neg_vals = [-1000, -500, -50, -5, -1]
pos_vals = [1, 5, 50, 500, 1000]

cols = st.columns([1, 1, 1, 1, 1, 0.5, 1, 1, 1, 1, 1])

for i, val in enumerate(neg_vals):
    if cols[i].button(str(val), key=f"neg_{i}"):
        adjust_val(val)
        st.rerun()

cols[5].write("") # Central Gap

for i, val in enumerate(pos_vals):
    if cols[i+6].button(f"+{val}", key=f"pos_{i}"):
        adjust_val(val)
        st.rerun()

st.write("---")

# --- ORIGINAL CALCULATION LOGIC ---
total_mm = st.number_input("TOTAL WIRE LENGTH (L) in mm", value=10000.0, step=1.0)
untwist_enabled = st.toggle("Untwisting Active", value=True)

st.markdown("### RESULT")

if not untwist_enabled:
    st.subheader("BYPASS")
else:
    # YOUR ORIGINAL FORMULA: rotations = l_mm / p_mm
    if p_mm > 0:
        rotations = total_mm / p_mm
        # Big bold output
        st.success(f"TOTAL UNTWIST ROTATIONS: {rotations:.3f}")
    else:
        st.error("Lay length must be greater than zero.")

if st.button("RESET TO 1000mm"):
    st.session_state.lay_length = 1000.0
    st.rerun()

import streamlit as st

# 1. Force "wide" mode so buttons have more horizontal room
st.set_page_config(page_title="Zeta Torsion Controller", page_icon="🌀", layout="wide")

# --- CSS FIXES ---
st.markdown("""
    <style>
    /* Fix button text wrapping and make them uniform */
    div.stButton > button:first-child {
        height: 3em;
        font-size: 14px; /* Slightly smaller to fit +1000 on one line */
        font-weight: bold;
        border-radius: 6px;
        white-space: nowrap; /* Prevents text from splitting into two lines */
        padding: 0px 2px;
    }
    /* Color coding */
    div[data-testid="column"]:nth-of-type(1) button, div[data-testid="column"]:nth-of-type(2) button,
    div[data-testid="column"]:nth-of-type(3) button, div[data-testid="column"]:nth-of-type(4) button,
    div[data-testid="column"]:nth-of-type(5) button {
        background-color: #d32f2f; color: white;
    }
    div[data-testid="column"]:nth-of-type(7) button, div[data-testid="column"]:nth-of-type(8) button,
    div[data-testid="column"]:nth-of-type(9) button, div[data-testid="column"]:nth-of-type(10) button,
    div[data-testid="column"]:nth-of-type(11) button {
        background-color: #2e7d32; color: white;
    }
    .button-title { text-align: center; font-weight: bold; color: #555; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

if 'lay_length' not in st.session_state:
    st.session_state.lay_length = 1000.0

def adjust_val(amount):
    st.session_state.lay_length = max(100.0, min(4950.0, st.session_state.lay_length + amount))

# --- UI START ---
st.title("🌀 Zeta Torsion Controller")

# Ticker Visual
p_mm = st.session_state.lay_length
progress = (p_mm - 100) / (4950 - 100)
st.progress(progress)

# Digital Readouts for Lay Length
col_m1, col_m2 = st.columns(2)
col_m1.metric("LAY LENGTH (P)", f"{p_mm:.0f} mm")
col_m2.metric("LAY LENGTH (IN)", f"{(p_mm * 0.0393701):.3f} in")

# --- COMPACT ADJUSTMENT PANEL ---
st.markdown('<p class="button-title">Precision Lay Adjustment Controls</p>', unsafe_allow_html=True)

with st.container(border=True):
    neg_vals = [-1000, -500, -50, -5, -1]
    pos_vals = [1, 5, 50, 500, 1000]
    
    # Using 11 columns with a very tiny middle gap
    cols = st.columns([1, 1, 1, 1, 1, 0.1, 1, 1, 1, 1, 1])

    for i, val in enumerate(neg_vals):
        if cols[i].button(str(val), key=f"neg_{i}"):
            adjust_val(val)
            st.rerun()

    cols[5].write("") 

    for i, val in enumerate(pos_vals):
        if cols[i+6].button(f"+{val}", key=f"pos_{i}"):
            adjust_val(val)
            st.rerun()

st.write("---")

# --- TOTAL WIRE LENGTH + MISSING INCH CONVERSION ---
col_in1, col_in2 = st.columns([2, 1])
with col_in1:
    total_mm = st.number_input("TOTAL WIRE LENGTH (L) in mm", value=10000.0)
with col_in2:
    # UPDATED: This now shows the conversion live for the Total Length
    total_inch = total_mm * 0.0393701
    st.metric("TOTAL INCHES", f"{total_inch:.3f} in")

untwist_enabled = st.toggle("Untwisting Active", value=True)

# --- CALCULATION ---
if untwist_enabled:
    rotations = total_mm / p_mm
    st.success(f"### TOTAL UNTWIST ROTATIONS: {rotations:.3f}")
else:
    st.warning("SYSTEM BYPASS")

if st.button("RESET TO 1000mm"):
    st.session_state.lay_length = 1000.0
    st.rerun()

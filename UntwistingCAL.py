import streamlit as st

# 1. Page Config
st.set_page_config(page_title="Zeta Torsion Controller", page_icon="🌀", layout="wide")

# --- CSS FOR BUTTONS (Stay same) ---
st.markdown("""
    <style>
    div.stButton > button:first-child { height: 3em; font-size: 14px; font-weight: bold; border-radius: 6px; white-space: nowrap; }
    div[data-testid="column"]:nth-of-type(1) button, div[data-testid="column"]:nth-of-type(2) button,
    div[data-testid="column"]:nth-of-type(3) button, div[data-testid="column"]:nth-of-type(4) button,
    div[data-testid="column"]:nth-of-type(5) button { background-color: #d32f2f; color: white; }
    div[data-testid="column"]:nth-of-type(7) button, div[data-testid="column"]:nth-of-type(8) button,
    div[data-testid="column"]:nth-of-type(9) button, div[data-testid="column"]:nth-of-type(10) button,
    div[data-testid="column"]:nth-of-type(11) button { background-color: #2e7d32; color: white; }
    .button-title { text-align: center; font-weight: bold; color: #555; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. STATE MANAGEMENT (The Fix is here)
if 'lay_length' not in st.session_state:
    st.session_state.lay_length = 1000.0

# --- UI START ---
st.title("🌀 Zeta Torsion Controller")

# 3. THE SLIDER (Ticker)
st.write("### LAY LENGTH ADJUSTMENT TRACKER")

# We use a standard variable here, NOT the key-lock method
p_mm = st.slider(
    "Drag to adjust", 
    min_value=100.0, 
    max_value=4950.0, 
    value=float(st.session_state.lay_length), # We feed it the value from memory
    step=1.0
)

# Sync the slider movement back to our memory
st.session_state.lay_length = p_mm

# Digital Readouts
p_inch = p_mm * 0.0393701
col_m1, col_m2 = st.columns(2)
col_m1.metric("LAY LENGTH (P)", f"{p_mm:.0f} mm")
col_m2.metric("LAY LENGTH (IN)", f"{p_inch:.3f} in")

st.write("---")

# --- PRECISION BUTTONS ---
st.markdown('<p class="button-title">Precision Incremental Controls</p>', unsafe_allow_html=True)

with st.container(border=True):
    neg_vals = [-1000, -500, -50, -5, -1]
    pos_vals = [1, 5, 50, 500, 1000]
    
    cols = st.columns([1, 1, 1, 1, 1, 0.1, 1, 1, 1, 1, 1])

    for i, val in enumerate(neg_vals):
        if cols[i].button(str(val), key=f"neg_{i}"):
            # Update the memory directly
            new_val = st.session_state.lay_length + val
            st.session_state.lay_length = max(100.0, min(4950.0, new_val))
            st.rerun() # Refresh to move the slider

    cols[5].write("") 

    for i, val in enumerate(pos_vals):
        if cols[i+6].button(f"+{val}", key=f"pos_{i}"):
            new_val = st.session_state.lay_length + val
            st.session_state.lay_length = max(100.0, min(4950.0, new_val))
            st.rerun()

st.write("---")

# --- TOTAL WIRE LENGTH & CONVERSION ---
col_in1, col_in2 = st.columns([2, 1])
with col_in1:
    total_mm = st.number_input("TOTAL WIRE LENGTH (L) in mm", value=10000.0, step=1.0)
with col_in2:
    total_inch = total_mm * 0.0393701
    st.metric("TOTAL INCHES", f"{total_inch:.3f} in")

untwist_enabled = st.toggle("Untwisting Active", value=True)

# --- THE CALCULATION ---
st.write("---")
if untwist_enabled:
    if p_mm > 0:
        rotations = total_mm / p_mm
        st.markdown(f"""
            <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; border-left: 10px solid #2e7d32;">
                <h2 style="margin:0; color:#333;">TOTAL UNTWIST ROTATIONS</h2>
                <h1 style="margin:0; color:#2e7d32; font-size:60px;">{rotations:.3f}</h1>
            </div>
        """, unsafe_allow_html=True)
else:
    st.warning("SYSTEM BYPASS: Torsion Control Inactive")

if st.button("RESET TO DEFAULT (1000mm)"):
    st.session_state.lay_length = 1000.0
    st.rerun()

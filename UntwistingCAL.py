import streamlit as st

# 1. Page Config
st.set_page_config(page_title="Zeta Torsion Pro", page_icon="🌀", layout="wide")

# --- PREMIUM DASHBOARD CSS ---
st.markdown("""
    <style>
    /* Main Background & Font */
    .stApp { background-color: #f8f9fa; }
    
    /* Card Container */
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
        margin-bottom: 20px;
    }

    /* Button Styling */
    div.stButton > button:first-child {
        height: 3.5em;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        border-radius: 8px;
        border: none;
        transition: all 0.2s ease;
    }
    
    /* Negative (Industrial Red) */
    div[data-testid="column"]:nth-of-type(1) button, div[data-testid="column"]:nth-of-type(2) button,
    div[data-testid="column"]:nth-of-type(3) button, div[data-testid="column"]:nth-of-type(4) button,
    div[data-testid="column"]:nth-of-type(5) button {
        background-color: #C62828; color: white;
    }
    
    /* Positive (Komax Green) */
    div[data-testid="column"]:nth-of-type(7) button, div[data-testid="column"]:nth-of-type(8) button,
    div[data-testid="column"]:nth-of-type(9) button, div[data-testid="column"]:nth-of-type(10) button,
    div[data-testid="column"]:nth-of-type(11) button {
        background-color: #2E7D32; color: white;
    }

    /* Result Highlight */
    .result-box {
        background-color: #1B2631;
        color: #2ECC71;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        border-bottom: 5px solid #2ECC71;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. State Management
if 'lay_length' not in st.session_state:
    st.session_state.lay_length = 1000.0

# --- HEADER ---
col_logo, col_title = st.columns([1, 4])
with col_title:
    st.title("Zeta Torsion Controller")
    st.caption("Industrial Torsion Precision Calculator | Komax Zeta Series")

# --- SECTION 1: VISUAL GAUGE ---
st.write("### 📏 Machine Configuration")
progress = (st.session_state.lay_length - 100) / (4950 - 100)
st.progress(progress)

# --- SECTION 2: THE CONTROL DECK ---
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("#### Lay Length Adjustment (P)")
    
    # The Slider
    new_p = st.slider("", 100.0, 4950.0, float(st.session_state.lay_length), step=1.0, label_visibility="collapsed")
    st.session_state.lay_length = new_p

    # The Buttons
    st.write("Precision Stepping")
    neg_vals = [-1000, -500, -50, -5, -1]
    pos_vals = [1, 5, 50, 500, 1000]
    btn_cols = st.columns([1, 1, 1, 1, 1, 0.2, 1, 1, 1, 1, 1])

    for i, val in enumerate(neg_vals):
        if btn_cols[i].button(str(val), key=f"neg_{i}"):
            st.session_state.lay_length = max(100.0, min(4950.0, st.session_state.lay_length + val))
            st.rerun()

    for i, val in enumerate(pos_vals):
        if btn_cols[i+6].button(f"+{val}", key=f"pos_{i}"):
            st.session_state.lay_length = max(100.0, min(4950.0, st.session_state.lay_length + val))
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("#### Current Settings")
    p_mm = st.session_state.lay_length
    st.metric("Metric Lay", f"{p_mm:.0f} mm")
    st.metric("Imperial Lay", f"{(p_mm * 0.0393701):.3f} in")
    st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 3: WIRE INPUT ---
st.write("### 🧵 Production Parameters")
col_wire1, col_wire2 = st.columns([3, 2])

with col_wire1:
    total_mm = st.number_input("TOTAL WIRE LENGTH (L) in mm", value=10000.0, step=10.0)

with col_wire2:
    st.metric("TOTAL WIRE (INCHES)", f"{(total_mm * 0.0393701):.3f} in")

# --- SECTION 4: THE CALCULATION ---
st.divider()
untwist_enabled = st.toggle("System Active", value=True)

if untwist_enabled:
    rotations = total_mm / p_mm
    st.markdown(f"""
        <div class="result-box">
            <p style="margin:0; font-size:1.2em; color:white; opacity:0.8;">REQUIRED UNTWIST ROTATIONS</p>
            <h1 style="margin:0; font-size:4.5em;">{rotations:.3f}</h1>
        </div>
    """, unsafe_allow_html=True)
else:
    st.error("⚠️ SYSTEM BYPASS: CALCULATOR INACTIVE")

if st.button("🔄 Reset Machine to Default"):
    st.session_state.lay_length = 1000.0
    st.rerun()

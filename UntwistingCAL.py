import streamlit as st

# 1. Page Config
st.set_page_config(page_title="Zeta Torsion Controller", page_icon="🌀", layout="wide")

# --- KOMAX BRANDED CSS ---
st.markdown("""
    <style>
    /* Dark Industrial Card */
    .komax-card {
        background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 50%, #1e1e1e 100%);
        padding: 40px;
        border-radius: 15px;
        border-bottom: 5px solid #28a745;
        text-align: center;
        color: white;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
        margin-top: 20px;
    }

    /* Centered Glowing Result */
    .wave-text {
        background: linear-gradient(90deg, #28a745, #97ebad, #28a745);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        font-weight: 800;
        font-size: 80px;
        margin: 0;
    }

    @keyframes shine {
        to { background-position: 200% center; }
    }

    /* Button Colors */
    div[data-testid="column"]:nth-of-type(1) button, div[data-testid="column"]:nth-of-type(2) button,
    div[data-testid="column"]:nth-of-type(3) button, div[data-testid="column"]:nth-of-type(4) button,
    div[data-testid="column"]:nth-of-type(5) button { background-color: #d32f2f !important; color: white !important; }

    div[data-testid="column"]:nth-of-type(7) button, div[data-testid="column"]:nth-of-type(8) button,
    div[data-testid="column"]:nth-of-type(9) button, div[data-testid="column"]:nth-of-type(10) button,
    div[data-testid="column"]:nth-of-type(11) button { background-color: #2e7d32 !important; color: white !important; }
    
    .button-title { text-align: center; font-weight: bold; color: #888; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. STATE MANAGEMENT
if 'lay_length' not in st.session_state:
    st.session_state.lay_length = 1000.0

# --- UI START ---
st.title("🌀 Zeta Torsion Controller")

# 3. THE SLIDER (Ticker)
st.write("### LAY LENGTH ADJUSTMENT TRACKER")

p_mm = st.slider(
    "Drag to adjust pitch", 
    min_value=100.0, 
    max_value=4950.0, 
    value=float(st.session_state.lay_length),
    step=1.0,
    help="Adjust the pitch (P) of the twist."
)

st.session_state.lay_length = p_mm

# Digital Readouts (Bringing back the Inch metrics you missed!)
p_inch = p_mm * 0.0393701
col_m1, col_m2 = st.columns(2)
col_m1.metric("LAY LENGTH (P) mm", f"{p_mm:.0f} mm")
col_m2.metric("LAY LENGTH (P) in", f"{p_inch:.3f} in")

st.write("---")

# --- PRECISION BUTTONS ---
st.markdown('<p class="button-title">Precision Incremental Controls</p>', unsafe_allow_html=True)
with st.container(border=True):
    neg_vals = [-1000, -500, -50, -5, -1]
    pos_vals = [1, 5, 50, 500, 1000]
    cols = st.columns([1, 1, 1, 1, 1, 0.1, 1, 1, 1, 1, 1])

    for i, val in enumerate(neg_vals):
        if cols[i].button(str(val), key=f"neg_{i}", help=f"Subtract {abs(val)}mm"):
            st.session_state.lay_length = max(100.0, min(4950.0, st.session_state.lay_length + val))
            st.rerun()

    for i, val in enumerate(pos_vals):
        if cols[i+6].button(f"+{val}", key=f"pos_{i}", help=f"Add {val}mm"):
            st.session_state.lay_length = max(100.0, min(4950.0, st.session_state.lay_length + val))
            st.rerun()

st.write("---")

# --- TOTAL WIRE LENGTH & CONVERSION (Ensuring these stay visible) ---
col_in1, col_in2 = st.columns([2, 1])
with col_in1:
    total_mm = st.number_input("TOTAL WIRE LENGTH (L) in mm", value=10000.0, step=1.0)
with col_in2:
    total_inch = total_mm * 0.0393701
    st.metric("TOTAL WIRE (L) in", f"{total_inch:.3f} in")

untwist_enabled = st.toggle("Untwisting Active", value=True)

# --- THE CENTERED RESULT BOX ---
if untwist_enabled:
    if p_mm > 0:
        rotations = total_mm / p_mm
        st.markdown(f"""
            <div class="komax-card">
                <p style="text-transform: uppercase; letter-spacing: 2px; color: #888;">Calculated Rotations</p>
                <h1 class="wave-text">{rotations:.3f}</h1>
                <p style="font-size: 20px; color: #28a745; font-weight: bold;">TOTAL TURNS</p>
            </div>
        """, unsafe_allow_html=True)
else:
    st.warning("SYSTEM BYPASS: Torsion Control Inactive")

# Sidebar for Reset so it doesn't clutter the main UI
if st.sidebar.button("RESET TO DEFAULT (1000mm)"):
    st.session_state.lay_length = 1000.0
    st.rerun()

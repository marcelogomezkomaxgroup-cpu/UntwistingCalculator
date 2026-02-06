import streamlit as st

# 1. Page Config
st.set_page_config(page_title="Zeta Torsion Controller", page_icon="🌀", layout="wide")

# --- UNIFORM INDUSTRIAL CSS ---
st.markdown("""
    <style>
    /* 1. Make all buttons uniform height and width */
    div.stButton > button:first-child { 
        width: 100%;           
        height: 60px;          /* Fixed height for uniformity */
        font-size: 18px; 
        font-weight: bold; 
        border-radius: 4px; 
        transition: all 0.2s ease;
        border: 1px solid #444;
    }

    /* 2. Match Number Input height to the buttons */
    .stNumberInput div[data-baseweb="input"] {
        height: 60px;
    }

    /* 3. Button Colors (Red for Negative, Green for Positive) */
    /* Negative Columns (1-5) */
    div[data-testid="column"]:nth-of-type(1) button, div[data-testid="column"]:nth-of-type(2) button,
    div[data-testid="column"]:nth-of-type(3) button, div[data-testid="column"]:nth-of-type(4) button,
    div[data-testid="column"]:nth-of-type(5) button { 
        background-color: #d32f2f !important; 
        color: white !important; 
    }

    /* Positive Columns (7-11) */
    div[data-testid="column"]:nth-of-type(7) button, div[data-testid="column"]:nth-of-type(8) button,
    div[data-testid="column"]:nth-of-type(9) button, div[data-testid="column"]:nth-of-type(10) button,
    div[data-testid="column"]:nth-of-type(11) button { 
        background-color: #2e7d32 !important; 
        color: white !important; 
    }

    /* 4. The Komax Result Card */
    .komax-card {
        background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 50%, #1e1e1e 100%);
        padding: 40px;
        border-radius: 12px;
        border-bottom: 6px solid #28a745;
        text-align: center;
        color: white;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.4);
        margin-top: 25px;
    }

    /* Centered Glowing Number */
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

    .button-title { text-align: center; font-weight: bold; color: #888; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. STATE MANAGEMENT
if 'lay_length' not in st.session_state:
    st.session_state.lay_length = 1000.0

# --- UI START ---
st.title("🌀 Zeta Torsion Controller")

# 3. THE SLIDER
st.write("### LAY LENGTH ADJUSTMENT TRACKER")
p_mm = st.slider(
    "Slide to adjust pitch", 
    min_value=100.0, 
    max_value=4950.0, 
    value=float(st.session_state.lay_length), 
    step=1.0,
    help="Adjust the lay length (P) in millimeters."
)
st.session_state.lay_length = p_mm

# Readouts for Slider
p_inch = p_mm * 0.0393701
col_m1, col_m2 = st.columns(2)
col_m1.metric("LAY LENGTH (P) mm", f"{p_mm:.1f} mm")
col_m2.metric("LAY LENGTH (P) in", f"{p_inch:.3f} in")

st.write("---")

# --- PRECISION BUTTONS (Uniform Rows) ---
st.markdown('<p class="button-title">Precision Incremental Controls (mm)</p>', unsafe_allow_html=True)
with st.container(border=True):
    neg_vals = [-1000, -500, -50, -5, -1]
    pos_vals = [1, 5, 50, 500, 1000]
    
    # Using specific ratios to keep a gap in the middle
    cols = st.columns([1, 1, 1, 1, 1, 0.2, 1, 1, 1, 1, 1])

    for i, val in enumerate(neg_vals):
        if cols[i].button(str(val), key=f"neg_{i}", help=f"Decrease by {abs(val)}mm"):
            st.session_state.lay_length = max(100.0, min(4950.0, st.session_state.lay_length + val))
            st.rerun()

    for i, val in enumerate(pos_vals):
        if cols[i+6].button(f"+{val}", key=f"pos_{i}", help=f"Increase by {val}mm"):
            st.session_state.lay_length = max(100.0, min(4950.0, st.session_state.lay_length + val))
            st.rerun()

st.write("---")

# --- TOTAL WIRE LENGTH & CONVERSION ---
col_in1, col_in2 = st.columns([2, 1])
with col_in1:
    total_mm = st.number_input(
        "TOTAL WIRE LENGTH (L) in mm", 
        value=10000.0, 
        step=1.0,
        help="Input the total length of the wire for processing."
    )
with col_in2:
    total_inch = total_mm * 0.0393701
    # Adding a spacer to align the metric with the input box
    st.write("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
    st.metric("TOTAL WIRE (L) in", f"{total_inch:.3f} in")

untwist_enabled = st.toggle("Untwisting Active", value=True, help="Switch off to bypass torsion calculations.")

# --- THE CENTERED KOMAX RESULT BOX ---
if untwist_enabled:
    if p_mm > 0:
        rotations = total_mm / p_mm
        st.markdown(f"""
            <div class="komax-card">
                <p style="text-transform: uppercase; letter-spacing: 3px; color: #888; font-weight:bold;">Torsion Calculation Output</p>
                <h1 class="wave-text">{rotations:.3f}</h1>
                <p style="font-size: 22px; color: #28a745; font-weight: bold; margin-top: -10px;">TOTAL TURNS (REVOLUTIONS)</p>
            </div>
        """, unsafe_allow_html=True)
else:
    st.warning("⚠️ SYSTEM BYPASS: Torsion Control Inactive")

# Sidebar Reset
st.sidebar.header("Machine Settings")
if st.sidebar.button("RESET TO DEFAULT (1000mm)"):
    st.session_state.lay_length = 1000.0
    st.rerun()

import streamlit as st

# 1. Page Config
st.set_page_config(page_title="Zeta Torsion Controller", page_icon="🌀", layout="wide")

# --- KOMAX BRANDED CSS ---
st.markdown("""
    <style>
    /* Gradient Wave Background for the Result Box */
    .komax-card {
        background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 50%, #1e1e1e 100%);
        background-image: url('https://www.transparenttextures.com/patterns/cubes.png'), 
                          linear-gradient(135deg, #1a1a1a 0%, #2c3e50 100%);
        padding: 40px;
        border-radius: 15px;
        border-bottom: 5px solid #28a745;
        text-align: center;
        color: white;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
        margin-top: 20px;
    }

    /* Wave effect accent */
    .wave-text {
        background: linear-gradient(90deg, #28a745, #97ebad, #28a745);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        font-weight: 800;
        font-size: 72px;
        margin: 0;
    }

    @keyframes shine {
        to { background-position: 200% center; }
    }

    /* Button Styling */
    div.stButton > button:first-child { 
        height: 3em; 
        font-size: 14px; 
        font-weight: bold; 
        border-radius: 4px; 
        transition: all 0.2s;
        border: 1px solid #444;
    }
    
    /* Precision Button Colors */
    div[data-testid="column"]:nth-of-type(1) button, div[data-testid="column"]:nth-of-type(2) button,
    div[data-testid="column"]:nth-of-type(3) button, div[data-testid="column"]:nth-of-type(4) button,
    div[data-testid="column"]:nth-of-type(5) button { background-color: #b71c1c; color: white; }

    div[data-testid="column"]:nth-of-type(7) button, div[data-testid="column"]:nth-of-type(8) button,
    div[data-testid="column"]:nth-of-type(9) button, div[data-testid="column"]:nth-of-type(10) button,
    div[data-testid="column"]:nth-of-type(11) button { background-color: #1b5e20; color: white; }

    .stSlider [data-baseweb="slider"] { color: #28a745; }
    </style>
    """, unsafe_allow_html=True)

# 2. STATE MANAGEMENT
if 'lay_length' not in st.session_state:
    st.session_state.lay_length = 1000.0

# --- UI START ---
st.title("🌀 Zeta Torsion Controller")

# 3. THE SLIDER
st.write("### LAY LENGTH ADJUSTMENT (P)")
p_mm = st.slider(
    "Fine-tune the wire torsion pitch", 
    100.0, 4950.0, float(st.session_state.lay_length), 1.0,
    help="Matches the pitch of the wire twist for the Zeta 650's twisting unit."
)
st.session_state.lay_length = p_mm

# Metrics
p_inch = p_mm * 0.0393701
col_m1, col_m2 = st.columns(2)
col_m1.metric("METRIC", f"{p_mm:.1f} mm")
col_m2.metric("IMPERIAL", f"{p_inch:.3f} in")

# --- PRECISION CONTROLS ---
with st.container(border=True):
    neg_vals = [-1000, -500, -50, -5, -1]
    pos_vals = [1, 5, 50, 500, 1000]
    cols = st.columns([1, 1, 1, 1, 1, 0.1, 1, 1, 1, 1, 1])

    for i, val in enumerate(neg_vals):
        if cols[i].button(str(val), key=f"n_{i}"):
            st.session_state.lay_length = max(100.0, min(4950.0, st.session_state.lay_length + val))
            st.rerun()

    for i, val in enumerate(pos_vals):
        if cols[i+6].button(f"+{val}", key=f"p_{i}"):
            st.session_state.lay_length = max(100.0, min(4950.0, st.session_state.lay_length + val))
            st.rerun()

# --- INPUTS ---
col_l1, col_l2 = st.columns([2, 1])
with col_l1:
    total_mm = st.number_input("TOTAL WIRE LENGTH (L) mm", value=10000.0, step=10.0)
with col_l2:
    untwist_enabled = st.toggle("Untwisting Active", value=True)

# --- THE KOMAX STYLE RESULT BOX ---
if untwist_enabled:
    rotations = total_mm / p_mm
    st.markdown(f"""
        <div class="komax-card">
            <p style="text-transform: uppercase; letter-spacing: 2px; color: #aaa; margin-bottom: 0;">Calculated Torsion Output</p>
            <h1 class="wave-text">{rotations:.3f}</h1>
            <p style="font-size: 20px; color: #28a745; margin-top: -10px;">TOTAL TURNS (REVOLUTIONS)</p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.warning("⚠️ Torsion Bypass Engaged - No Rotations Calculated")

# Sidebar Reset
if st.sidebar.button("System Reset"):
    st.session_state.lay_length = 1000.0
    st.rerun()

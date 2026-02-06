import streamlit as st

# 1. Page Config
st.set_page_config(page_title="Zeta Torsion Controller", page_icon="🌀", layout="wide")

# --- UNIFORM INDUSTRIAL CSS ---
st.markdown("""
    <style>
    div.stButton > button:first-child { 
        width: 100%;           
        height: 60px;          
        font-size: 18px; 
        font-weight: bold; 
        border-radius: 4px; 
        border: 1px solid #444;
    }
    /* Input Box Heights */
    .stNumberInput div[data-baseweb="input"], .stSlider {
        height: 60px;
    }
    
    /* Button Colors */
    div[data-testid="column"]:nth-of-type(1) button, div[data-testid="column"]:nth-of-type(2) button,
    div[data-testid="column"]:nth-of-type(3) button, div[data-testid="column"]:nth-of-type(4) button,
    div[data-testid="column"]:nth-of-type(5) button { background-color: #d32f2f !important; color: white !important; }

    div[data-testid="column"]:nth-of-type(7) button, div[data-testid="column"]:nth-of-type(8) button,
    div[data-testid="column"]:nth-of-type(9) button, div[data-testid="column"]:nth-of-type(10) button,
    div[data-testid="column"]:nth-of-type(11) button { background-color: #2e7d32 !important; color: white !important; }

    .komax-card {
        background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 50%, #1e1e1e 100%);
        padding: 40px;
        border-radius: 12px;
        border-bottom: 6px solid #28a745;
        text-align: center;
        color: white;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.4);
    }
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
    @keyframes shine { to { background-position: 200% center; } }
    </style>
    """, unsafe_allow_html=True)

# 2. CALLBACK FUNCTIONS (The Fix)
def update_lay(val):
    new_val = st.session_state.lay_length + val
    st.session_state.lay_length = max(100.0, min(4950.0, float(new_val)))

# 3. STATE MANAGEMENT
if 'lay_length' not in st.session_state:
    st.session_state.lay_length = 1000.0

# --- UI START ---
st.title("🌀 Zeta Torsion Controller")

# TOTAL WIRE LENGTH INPUT
col_in1, col_in2 = st.columns([2, 1])
with col_in1:
    total_mm = st.number_input("TOTAL WIRE LENGTH (L) mm", value=10000.0, step=1.0)
with col_in2:
    total_inch = total_mm * 0.0393701
    st.write("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
    st.metric("TOTAL WIRE in", f"{total_inch:.3f} in")

st.write("---")

# LAY LENGTH SLIDER
st.write("### LAY LENGTH ADJUSTMENT (P)")
# Use the key "lay_length" to link directly to session state
st.slider("Adjust Pitch", 100.0, 4950.0, step=1.0, key="lay_length", help="Slide to adjust P")

p_mm = st.session_state.lay_length
p_inch = p_mm * 0.0393701

col_m1, col_m2 = st.columns(2)
col_m1.metric("LAY LENGTH mm", f"{p_mm:.1f} mm")
col_m2.metric("LAY LENGTH in", f"{p_inch:.3f} in")

# PRECISION BUTTONS
st.write("---")
st.markdown('<p style="text-align:center; color:#888;">Precision Incremental Controls</p>', unsafe_allow_html=True)

with st.container(border=True):
    neg_vals = [-1000, -500, -50, -5, -1]
    pos_vals = [1, 5, 50, 500, 1000]
    cols = st.columns([1, 1, 1, 1, 1, 0.2, 1, 1, 1, 1, 1])

    for i, val in enumerate(neg_vals):
        cols[i].button(str(val), key=f"btn_{val}", on_click=update_lay, args=(val,))

    for i, val in enumerate(pos_vals):
        cols[i+6].button(f"+{val}", key=f"btn_{val}", on_click=update_lay, args=(val,))

# CALCULATED RESULT
st.write("---")
untwist_enabled = st.toggle("Untwisting Active", value=True)

if untwist_enabled and p_mm > 0:
    rotations = total_mm / p_mm
    st.markdown(f"""
        <div class="komax-card">
            <p style="text-transform: uppercase; letter-spacing: 3px; color: #888;">Calculated Torsion Output</p>
            <h1 class="wave-text">{rotations:.3f}</h1>
            <p style="font-size: 22px; color: #28a745; font-weight: bold;">TOTAL TURNS</p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.warning("⚠️ SYSTEM BYPASS: Torsion Control Inactive")

# Sidebar Reset
if st.sidebar.button("System Reset"):
    st.session_state.lay_length = 1000.0
    st.rerun()

import streamlit as st

# 1. Page Config
st.set_page_config(page_title="Zeta Torsion Controller", page_icon="🌀", layout="wide")

# --- KOMAX HMI DARK THEME CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #2b3033; }
    
    /* Uniform Button Sizing */
    div.stButton > button:first-child { 
        width: 100%; height: 60px; font-size: 18px; font-weight: bold; 
        border-radius: 4px; border: 1px solid #444; color: white;
    }
    
    /* Input Box Heights & Colors */
    .stNumberInput div[data-baseweb="input"] { 
        height: 60px; background-color: #1e1e1e !important; color: white !important;
    }

    /* Red Negative Buttons */
    div[data-testid="column"]:nth-of-type(1) button, div[data-testid="column"]:nth-of-type(2) button,
    div[data-testid="column"]:nth-of-type(3) button, div[data-testid="column"]:nth-of-type(4) button,
    div[data-testid="column"]:nth-of-type(5) button { background-color: #a82222 !important; }

    /* Green Positive Buttons */
    div[data-testid="column"]:nth-of-type(7) button, div[data-testid="column"]:nth-of-type(8) button,
    div[data-testid="column"]:nth-of-type(9) button, div[data-testid="column"]:nth-of-type(10) button,
    div[data-testid="column"]:nth-of-type(11) button { background-color: #1e7d32 !important; }

    /* The Result Card */
    .komax-card {
        background: #1e1e1e; padding: 40px; border-radius: 4px;
        border-left: 10px solid #28a745; text-align: center; color: white;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.5);
    }
    
    .wave-text { color: #28a745; font-weight: 800; font-size: 90px; margin: 0; }

    /* HMI Wire Representation using CSS (No external file needed) */
    .wire-graphic {
        width: 100%; height: 40px; background: #666; position: relative;
        border-radius: 5px; border: 2px solid #444; margin: 20px 0;
    }
    .wire-core {
        width: 90%; height: 10px; background: #c0392b; 
        position: absolute; top: 15px; left: 5%;
    }
    .strip-end {
        width: 15px; height: 15px; background: #d35400; position: absolute; top: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. STATE & CALLBACKS
if 'lay_length' not in st.session_state:
    st.session_state.lay_length = 1000.0

def update_lay(val):
    st.session_state.lay_length = max(100.0, min(4950.0, float(st.session_state.lay_length + val)))

# --- UI START ---
st.title("🌀 Zeta Torsion Controller | HMI Mode")

# 3. THE WIRE GRAPHIC (CSS Version to avoid file errors)
st.write("### Wire Processing Preview")
st.markdown("""
    <div style="background-color: #3e4447; padding: 20px; border-radius: 10px; text-align: center;">
        <div style="color: #ccc; margin-bottom: 5px;">Double-Sided Strip Selection</div>
        <div class="wire-graphic">
            <div class="wire-core"></div>
            <div class="strip-end" style="left: 2%;"></div>
            <div class="strip-end" style="right: 2%;"></div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 4. TOTAL WIRE LENGTH INPUT
col_in1, col_in2 = st.columns([3, 1])
with col_in1:
    total_mm = st.number_input("TOTAL WIRE LENGTH (L) mm", value=10000.0, step=1.0)
with col_in2:
    total_inch = total_mm * 0.0393701
    st.metric("TOTAL WIRE in", f"{total_inch:.3f} in")

st.write("---")

# 5. LAY LENGTH SLIDER
st.write("### LAY LENGTH ADJUSTMENT (P)")
st.slider("Adjust Pitch", 100.0, 4950.0, step=1.0, key="lay_length")

p_mm = st.session_state.lay_length
p_inch = p_mm * 0.0393701

col_m1, col_m2 = st.columns(2)
col_m1.metric("LAY LENGTH mm", f"{p_mm:.1f} mm")
col_m2.metric("LAY LENGTH in", f"{p_inch:.3f} in")

# 6. PRECISION BUTTONS
st.write("---")
with st.container():
    neg_vals = [-1000, -500, -50, -5, -1]
    pos_vals = [1, 5, 50, 500, 1000]
    cols = st.columns([1, 1, 1, 1, 1, 0.2, 1, 1, 1, 1, 1])

    for i, val in enumerate(neg_vals):
        cols[i].button(str(val), key=f"btn_{val}", on_click=update_lay, args=(val,))

    for i, val in enumerate(pos_vals):
        cols[i+6].button(f"+{val}", key=f"btn_{val}", on_click=update_lay, args=(val,))

# 7. CALCULATION DISPLAY
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

if st.sidebar.button("System Reset"):
    st.session_state.lay_length = 1000.0
    st.rerun()

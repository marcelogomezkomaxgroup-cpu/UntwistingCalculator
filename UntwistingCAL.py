import streamlit as st

# 1. Page Config
st.set_page_config(page_title="Zeta Torsion Controller", page_icon="🌀", layout="wide")

# --- ENHANCED CSS ---
st.markdown("""
    <style>
    /* Button Base Styling */
    div.stButton > button:first-child { 
        height: 3em; 
        font-size: 14px; 
        font-weight: bold; 
        border-radius: 8px; 
        transition: all 0.3s ease;
    }
    
    /* Negative Buttons (Red Gradient) */
    div[data-testid="column"]:nth-of-type(1) button, div[data-testid="column"]:nth-of-type(2) button,
    div[data-testid="column"]:nth-of-type(3) button, div[data-testid="column"]:nth-of-type(4) button,
    div[data-testid="column"]:nth-of-type(5) button { 
        background-color: #ff4b4b; 
        color: white; 
        border: none;
    }

    /* Positive Buttons (Green Gradient) */
    div[data-testid="column"]:nth-of-type(7) button, div[data-testid="column"]:nth-of-type(8) button,
    div[data-testid="column"]:nth-of-type(9) button, div[data-testid="column"]:nth-of-type(10) button,
    div[data-testid="column"]:nth-of-type(11) button { 
        background-color: #28a745; 
        color: white; 
        border: none;
    }
    
    /* Hover Effects */
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }

    .button-title { text-align: center; font-weight: bold; color: #555; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. STATE MANAGEMENT
if 'lay_length' not in st.session_state:
    st.session_state.lay_length = 1000.0

# --- UI START ---
st.title("🌀 Zeta Torsion Controller")
st.info("💡 **Pro Tip:** Use the precision buttons below for fine-tuning, or drag the slider for large adjustments.")

# 3. THE SLIDER
st.write("### LAY LENGTH ADJUSTMENT TRACKER")

p_mm = st.slider(
    "Adjust Lay Length (P)", 
    min_value=100.0, 
    max_value=4950.0, 
    value=float(st.session_state.lay_length),
    step=1.0,
    help="The 'Lay Length' is the longitudinal distance required for one complete helical wrap of a strand around the core."
)

st.session_state.lay_length = p_mm

# Digital Readouts
p_inch = p_mm * 0.0393701
col_m1, col_m2 = st.columns(2)
col_m1.metric("METRIC (P)", f"{p_mm:.0f} mm", help="Current value in Millimeters")
col_m2.metric("IMPERIAL (P)", f"{p_inch:.3f} in", help="Current value converted to Inches")

st.write("---")

# --- PRECISION BUTTONS ---
st.markdown('<p class="button-title">Precision Incremental Controls</p>', unsafe_allow_html=True)

with st.container(border=True):
    neg_vals = [-1000, -500, -50, -5, -1]
    pos_vals = [1, 5, 50, 500, 1000]
    
    cols = st.columns([1, 1, 1, 1, 1, 0.1, 1, 1, 1, 1, 1])

    for i, val in enumerate(neg_vals):
        if cols[i].button(str(val), key=f"neg_{i}", help=f"Subtract {abs(val)}mm from current length"):
            new_val = st.session_state.lay_length + val
            st.session_state.lay_length = max(100.0, min(4950.0, new_val))
            st.rerun()

    cols[5].write("") 

    for i, val in enumerate(pos_vals):
        if cols[i+6].button(f"+{val}", key=f"pos_{i}", help=f"Add {val}mm to current length"):
            new_val = st.session_state.lay_length + val
            st.session_state.lay_length = max(100.0, min(4950.0, new_val))
            st.rerun()

st.write("---")

# --- TOTAL WIRE LENGTH & CONVERSION ---
col_in1, col_in2 = st.columns([2, 1])
with col_in1:
    total_mm = st.number_input(
        "TOTAL WIRE LENGTH (L) in mm", 
        value=10000.0, 
        step=1.0,
        help="Input the total length of the wire being processed."
    )
with col_in2:
    total_inch = total_mm * 0.0393701
    st.metric("TOTAL INCHES", f"{total_inch:.3f} in")

untwist_enabled = st.toggle("Untwisting Active", value=True, help="Toggle this off to bypass torsion calculations.")

# --- THE CALCULATION ---
st.write("---")
if untwist_enabled:
    if p_mm > 0:
        # Rotations = L / P
        rotations = total_mm / p_mm
        st.markdown(f"""
            <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; border-left: 10px solid #28a745; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);">
                <h2 style="margin:0; color:#333; font-size: 18px;">TOTAL UNTWIST ROTATIONS</h2>
                <h1 style="margin:0; color:#28a745; font-size:60px;">{rotations:.3f} <span style="font-size:20px; color:#666;">Turns</span></h1>
            </div>
        """, unsafe_allow_html=True)
else:
    st.warning("⚠️ SYSTEM BYPASS: Torsion Control Inactive. No rotations calculated.")

st.sidebar.title("Settings")
if st.sidebar.button("RESET TO DEFAULT", help="Returns Lay Length to 1000mm"):
    st.session_state.lay_length = 1000.0
    st.rerun()

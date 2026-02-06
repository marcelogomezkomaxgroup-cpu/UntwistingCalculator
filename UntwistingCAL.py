import streamlit as st

# 1. Page Config
st.set_page_config(page_title="Zeta Torsion Pro", page_icon="🌀", layout="wide")

# --- HIGH CONTRAST INDUSTRIAL CSS ---
st.markdown("""
    <style>
    /* Force Large Black Text for Readability */
    html, body, [class*="st-"] {
        font-size: 20px;
        color: #000000 !important;
        font-weight: 600;
    }

    /* Button Styling - Bigger and Bolder */
    div.stButton > button:first-child {
        height: 3.5em;
        font-size: 22px !important;
        font-weight: 900 !important;
        border-radius: 4px;
        border: 2px solid #000;
    }
    
    /* Negative Buttons (Solid Red) */
    div[data-testid="column"]:nth-of-type(1) button, div[data-testid="column"]:nth-of-type(2) button,
    div[data-testid="column"]:nth-of-type(3) button, div[data-testid="column"]:nth-of-type(4) button,
    div[data-testid="column"]:nth-of-type(5) button {
        background-color: #FF0000 !important; color: white !important;
    }
    
    /* Positive Buttons (Solid Green) */
    div[data-testid="column"]:nth-of-type(7) button, div[data-testid="column"]:nth-of-type(8) button,
    div[data-testid="column"]:nth-of-type(9) button, div[data-testid="column"]:nth-of-type(10) button,
    div[data-testid="column"]:nth-of-type(11) button {
        background-color: #008000 !important; color: white !important;
    }

    /* Input Fields - Make them stand out */
    .stNumberInput input {
        font-size: 30px !important;
        font-weight: bold !important;
        color: #000 !important;
    }

    /* Result Area - Maximum Visibility */
    .big-result-box {
        background-color: #FFFF00; /* Safety Yellow */
        border: 5px solid #000;
        padding: 20px;
        text-align: center;
        margin-top: 20px;
    }
    
    .big-result-text {
        font-size: 80px !important;
        color: #000 !important;
        font-weight: 900 !important;
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. State Management
if 'lay_length' not in st.session_state:
    st.session_state.lay_length = 1000.0

# --- UI START ---
st.title("🌀 ZETA TORSION CONTROLLER")

# --- SECTION 1: THE GAUGE ---
p_mm = st.session_state.lay_length
st.write(f"### LAY LENGTH (P): {p_mm:.0f} mm")
st.progress((p_mm - 100) / (4950 - 100))

# --- SECTION 2: DUAL UNIT DISPLAY ---
col_m1, col_m2 = st.columns(2)
col_m1.metric("MM", f"{p_mm:.0f}")
col_m2.metric("INCHES", f"{(p_mm * 0.0393701):.3f}")

st.write("---")

# --- SECTION 3: ADJUSTMENT BUTTONS (User Fancy & Fast) ---
st.markdown("### QUICK ADJUST")
neg_vals = [-1000, -500, -50, -5, -1]
pos_vals = [1, 5, 50, 500, 1000]

# Using a layout that stays together on phones
cols = st.columns([1, 1, 1, 1, 1, 0.2, 1, 1, 1, 1, 1])

for i, val in enumerate(neg_vals):
    if cols[i].button(str(val), key=f"neg_{i}"):
        st.session_state.lay_length = max(100.0, min(4950.0, st.session_state.lay_length + val))
        st.rerun()

cols[5].write("") # Gap

for i, val in enumerate(pos_vals):
    if cols[i+6].button(f"+{val}", key=f"pos_{i}"):
        st.session_state.lay_length = max(100.0, min(4950.0, st.session_state.lay_length + val))
        st.rerun()

st.write("---")

# --- SECTION 4: PRODUCTION INPUT ---
total_mm = st.number_input("TOTAL WIRE LENGTH (L) mm", value=10000.0, step=1.0)
st.write(f"**CONVERSION:** {(total_mm * 0.0393701):.3f} inches")

# --- SECTION 5: THE FINAL CALCULATION (Big & Bold) ---
st.write("---")
untwist_enabled = st.toggle("UNTWISTING ACTIVE", value=True)

if untwist_enabled:
    rotations = total_mm / p_mm
    st.markdown(f"""
        <div class="big-result-box">
            <span style="font-size: 25px; font-weight: bold;">TOTAL UNTWIST ROTATIONS</span>
            <p class="big-result-text">{rotations:.3f}</p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.error("⚠️ BYPASS MODE")

if st.button("RESET TO 1000mm"):
    st.session_state.lay_length = 1000.0
    st.rerun()

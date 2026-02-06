import streamlit as st

st.set_page_config(page_title="Zeta Torsion Controller", page_icon="🌀", layout="centered")

# --- KOMAX BRANDING CSS ---
st.markdown("""
    <style>
    /* Main Button Styling */
    div.stButton > button:first-child {
        background-color: #2e7d32; /* Komax Green */
        color: white;
        border-radius: 5px;
        border: none;
        width: 100%;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    /* Hover Effect */
    div.stButton > button:first-child:hover {
        background-color: #1b5e20;
        border: 1px solid #ffffff;
    }
    /* Make metrics look more industrial */
    [data-testid="stMetricValue"] {
        font-family: 'Courier New', Courier, monospace;
        color: #333333;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. Memory Setup
if 'lay_length' not in st.session_state:
    st.session_state.lay_length = 1000.0

def mm_to_inch(mm_val):
    return mm_val * 0.0393701

def adjust_val(amount):
    st.session_state.lay_length = max(100.0, min(4950.0, st.session_state.lay_length + amount))

# --- UI ---
st.image("https://www.komaxgroup.com/etc.clientlibs/komax/clientlibs/clientlib-site/resources/images/logo.svg", width=200) 
st.title("Zeta Torsion Controller")

# Header Metrics
p_mm = st.session_state.lay_length
col_a, col_b = st.columns(2)
col_a.metric("LAY LENGTH (MM)", f"{p_mm:.0f}")
col_b.metric("LAY LENGTH (IN)", f"{mm_to_inch(p_mm):.3f}")

# --- UNIFORMED BUTTONS ---
st.write("### QUICK ADJUST")

# Row 1: Negatives
neg_inc = [-1000, -500, -50, -5, -1]
cols1 = st.columns(len(neg_inc))
for i, val in enumerate(neg_inc):
    if cols1[i].button(f"{val}", key=f"neg_{i}"):
        adjust_val(val)
        st.rerun()

# Row 2: Positives
pos_inc = [1, 5, 50, 500, 1000]
cols2 = st.columns(len(pos_inc))
for i, val in enumerate(pos_inc):
    if cols2[i].button(f"+{val}", key=f"pos_{i}"):
        adjust_val(val)
        st.rerun()

# --- INPUT & CALCULATION ---
st.divider()
total_mm = st.number_input("TOTAL WIRE LENGTH (MM)", value=10000.0, step=1.0)

# Final Result
st.markdown("---")
untwist_enabled = st.toggle("Untwisting Active", value=True)

if not untwist_enabled:
    st.info("SYSTEM BYPASS")
else:
    rotations = total_mm / p_mm
    st.subheader("TOTAL UNTWIST ROTATIONS")
    st.title(f"🔄 {rotations:.3f}")

if st.button("RESET TO 1000mm"):
    st.session_state.lay_length = 1000.0
    st.rerun()

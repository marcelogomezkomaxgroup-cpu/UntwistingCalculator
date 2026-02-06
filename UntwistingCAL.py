import streamlit as st

# 1. Initialize "Memory" (Session State)
if 'lay_length' not in st.session_state:
    st.session_state.lay_length = 1000.0

# Helper for conversion
def mm_to_inch(mm_val):
    return mm_val * 0.0393701

def adjust_val(amount):
    new_val = st.session_state.lay_length + amount
    # Keep it within your 100-4950 range
    st.session_state.lay_length = max(100.0, min(4950.0, new_val))

st.title("🌀 Zeta Torsion Controller")

# --- SECTION 1: HEADER & BYPASS ---
untwist_enabled = st.toggle("Untwisting Active", value=True)

# --- SECTION 2: THE BUTTONS (Your favorite part) ---
st.markdown(f"### Lay Length (P): **{st.session_state.lay_length:.0f} mm** :blue[({mm_to_inch(st.session_state.lay_length):.2f} in)]")

# Create rows of buttons just like your Tkinter app
increments = [-1000, -500, -50, -5, -1, 1, 5, 50, 500, 1000]
cols = st.columns(len(increments))

for i, inc in enumerate(increments):
    label = f"+{inc}" if inc > 0 else str(inc)
    if cols[i].button(label, key=f"btn_{inc}_{i}"):
        adjust_val(inc)

# A small slider for fine-tuning
st.session_state.lay_length = st.slider("Fine Tune (mm)", 100.0, 4950.0, st.session_state.lay_length)

# --- SECTION 3: INPUT ---
st.divider()
total_mm = st.number_input("Total Wire Length (mm)", value=10000.0)
st.caption(f"Imperial: {mm_to_inch(total_mm):.2f} inches")

# --- SECTION 4: THE BIG RESULT ---
if not untwist_enabled:
    st.warning("SYSTEM BYPASS")
else:
    rotations = total_mm / st.session_state.lay_length
    
    # Big visual container
    st.container(border=True)
    st.metric(label="TOTAL UNTWIST ROTATIONS", value=f"{rotations:.3f}")

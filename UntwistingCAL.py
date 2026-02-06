import streamlit as st

# 1. Page Config for a professional look
st.set_page_config(page_title="Zeta Controller", page_icon="🌀")

# 2. Memory Setup
if 'lay_length' not in st.session_state:
    st.session_state.lay_length = 1000.0

# 3. Helper Functions
def mm_to_inch(mm_val):
    return mm_val * 0.0393701

# Logic: This function forces the calculation to be "fresh"
def adjust_val(amount):
    new_val = st.session_state.lay_length + amount
    st.session_state.lay_length = max(100.0, min(4950.0, new_val))

# --- UI LAYOUT ---
st.title("🌀 Zeta Torsion Controller")

# Bypass Toggle
untwist_enabled = st.toggle("Untwisting Active", value=True)

# 4. The Display Area (Updates immediately)
p_mm = st.session_state.lay_length
p_inch = mm_to_inch(p_mm)

# Show the Current Lay Length in a "Nice" Box
st.subheader("Current Lay Length (P)")
col_a, col_b = st.columns(2)
col_a.metric("Metric", f"{p_mm:.0f} mm")
col_b.metric("Imperial", f"{p_inch:.2f} in")

# 5. The Buttons Row
st.write("Quick Adjust:")
increments = [-1000, -500, -50, -5, -1, 1, 5, 50, 500, 1000]
cols = st.columns(len(increments))

for i, inc in enumerate(increments):
    label = f"+{inc}" if inc > 0 else str(inc)
    # When button is clicked, it runs adjust_val AND triggers a page rerun
    if cols[i].button(label, key=f"btn_{i}"):
        adjust_val(inc)
        st.rerun() 

# 6. Total Wire Length Input
st.divider()
total_mm = st.number_input("Total Wire Length (mm)", value=10000.0, step=10.0)
total_inch = mm_to_inch(total_mm)
st.write(f"📏 **Total Inch:** {total_inch:.2f} in")

# 7. Final Calculation
st.divider()
if not untwist_enabled:
    st.error("SYSTEM BYPASS ACTIVE")
else:
    # We calculate using the absolute latest p_mm
    rotations = total_mm / p_mm
    
    st.write("### TOTAL UNTWIST ROTATIONS")
    st.title(f"{rotations:.3f}")
    
    # Progress bar just for "niceness"
    st.progress(min(rotations / 100, 1.0))

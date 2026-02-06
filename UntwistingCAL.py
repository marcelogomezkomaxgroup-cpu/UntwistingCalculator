import streamlit as st

# Helper for conversion
def mm_to_inch(mm_val):
    return mm_val * 0.0393701

# Title and Layout
st.title("🌀 Zeta Torsion Controller")
st.subheader("Dual Unit Precision Calculator")

# 1. Bypass Switch
untwist_enabled = st.checkbox("Untwisting Active", value=True)

# 2. Lay Length Controls
st.markdown(f"**Lay Length (P)**")
col1, col2 = st.columns([3, 1])

with col1:
    # The slider replaces your buttons and scale
    lay_length = st.slider("Select mm", 100, 4950, 1000)

with col2:
    # Show imperial equivalent immediately
    st.metric("Inches", f"{mm_to_inch(lay_length):.2f} in")

# 3. Wire Length Input
total_mm = st.number_input("Total Wire Length (mm)", value=10000.0, step=1.0)
st.caption(f"Equivalent to: {mm_to_inch(total_mm):.2f} inches")

# 4. Calculation Logic
st.divider()

if not untwist_enabled:
    st.info("BYPASS MODE: System is currently inactive.")
    rotations = 0.0
else:
    if lay_length > 0:
        rotations = total_mm / lay_length
        # Large Output Visual
        st.write("### TOTAL UNTWIST ROTATIONS")
        st.title(f" {rotations:.3f}")
    else:
        st.error("Lay Length must be greater than 0")

# Styling the result box (Optional)
if untwist_enabled:
    st.success(f"Calculation complete for {total_mm}mm wire.")

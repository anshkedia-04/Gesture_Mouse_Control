import streamlit as st
from gesture_control import start_control, stop_control

st.set_page_config(page_title="Gesture Mouse Control", layout="centered")
st.title("🖐️ Gesture-Based Mouse Control")
st.markdown("Control your mouse with your hand gestures.")

if "gesture_active" not in st.session_state:
    st.session_state.gesture_active = False

col1, col2 = st.columns(2)

if col1.button("🟢 Start Control"):
    if not st.session_state.gesture_active:
        start_control()
        st.session_state.gesture_active = True
        st.success("Gesture control started!")
    else:
        st.info("Already running.")

if col2.button("🔴 Stop Control"):
    if st.session_state.gesture_active:
        stop_control()
        st.session_state.gesture_active = False
        st.warning("Gesture control stopped.")
    else:
        st.info("Gesture control is not running.")

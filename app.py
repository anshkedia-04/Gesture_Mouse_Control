import streamlit as st
from gesture_control import start_control, stop_control

# Page configuration with dark theme
st.set_page_config(
    page_title="VisionMouse - Gesture Control",
    page_icon="🖱️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional dark theme
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #1e2936 0%, #2d3748 100%);
        padding: 2rem;
        border-radius: 12px;
        border-left: 4px solid #3b82f6;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .main-title {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Stats container */
    .stats-container {
        background: #1e2936;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #2d3748;
        margin-bottom: 1.5rem;
    }
    
    .stat-box {
        background: linear-gradient(135deg, #2d3748 0%, #1e2936 100%);
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #3b82f6;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .stat-value {
        color: #3b82f6;
        font-size: 2.5rem;
        font-weight: 700;
        display: block;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        color: #94a3b8;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Instructions box */
    .instructions {
        background: #1e2936;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 3px solid #10b981;
        margin: 1.5rem 0;
    }
    
    .instruction-title {
        color: #10b981;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .instruction-item {
        color: #cbd5e1;
        margin: 0.5rem 0;
        padding-left: 1.5rem;
        position: relative;
    }
    
    .instruction-item:before {
        content: "→";
        position: absolute;
        left: 0;
        color: #3b82f6;
    }
    
    /* Status indicator */
    .status-active {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
        border-radius: 25px;
        border: 2px solid #10b981;
        font-weight: 700;
        font-size: 1rem;
        animation: pulse 2s infinite;
        margin: 1rem 0;
    }
    
    .status-inactive {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        background: rgba(100, 116, 139, 0.2);
        color: #64748b;
        border-radius: 25px;
        border: 2px solid #64748b;
        font-weight: 700;
        font-size: 1rem;
        margin: 1rem 0;
    }
    
    @keyframes pulse {
        0%, 100% { 
            opacity: 1;
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
        }
        50% { 
            opacity: 0.7;
            box-shadow: 0 0 30px rgba(16, 185, 129, 0.5);
        }
    }
    
    /* Button styling */
    .stButton > button {
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 8px;
        width: 100%;
        transition: all 0.3s ease;
        height: 60px;
    }
    
    /* Start button - Green */
    div[data-testid="column"]:nth-child(1) .stButton > button {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    
    div[data-testid="column"]:nth-child(1) .stButton > button:hover {
        background: linear-gradient(90deg, #059669 0%, #047857 100%);
        box-shadow: 0 6px 16px rgba(16, 185, 129, 0.4);
        transform: translateY(-2px);
    }
    
    /* Stop button - Red */
    div[data-testid="column"]:nth-child(2) .stButton > button {
        background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%);
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
    }
    
    div[data-testid="column"]:nth-child(2) .stButton > button:hover {
        background: linear-gradient(90deg, #dc2626 0%, #b91c1c 100%);
        box-shadow: 0 6px 16px rgba(239, 68, 68, 0.4);
        transform: translateY(-2px);
    }
    
    /* Sidebar styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: #1e2936;
    }
    
    /* Remove default streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Alert box */
    .alert-box {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid #3b82f6;
        border-radius: 8px;
        padding: 1rem;
        color: #93c5fd;
        margin: 1rem 0;
    }
    
    /* Feature card */
    .feature-card {
        background: #1e2936;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #2d3748;
        margin: 1rem 0;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        border-color: #3b82f6;
        transform: translateY(-4px);
        box-shadow: 0 8px 16px rgba(59, 130, 246, 0.2);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .feature-title {
        color: #ffffff;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: #94a3b8;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    /* Gesture info cards */
    .gesture-card {
        background: linear-gradient(135deg, #1e2936 0%, #2d3748 100%);
        padding: 1.2rem;
        border-radius: 8px;
        border-left: 3px solid #3b82f6;
        margin: 0.8rem 0;
    }
    
    .gesture-name {
        color: #3b82f6;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 0.3rem;
    }
    
    .gesture-action {
        color: #cbd5e1;
        font-size: 0.9rem;
    }
    
    /* Success/Warning messages override */
    .stSuccess, .stWarning, .stInfo {
        background: transparent !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🖱️ VisionMouse - Gesture Control</h1>
    <p class="subtitle">Control your computer mouse with intuitive hand gestures powered by AI</p>
</div>
""", unsafe_allow_html=True)

# Session state initialization
if "gesture_active" not in st.session_state:
    st.session_state.gesture_active = False

# Sidebar - Gesture Guide
with st.sidebar:
    st.markdown("### 🎯 Gesture Guide")
    
    st.markdown("""
    <div class="gesture-card">
        <div class="gesture-name">👆 Index Finger Up</div>
        <div class="gesture-action">Move cursor around screen</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="gesture-card">
        <div class="gesture-name">✌️ Index + Middle Up</div>
        <div class="gesture-action">Left click action</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="gesture-card">
        <div class="gesture-name">🤟 Three Fingers Up</div>
        <div class="gesture-action">Right click action</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="gesture-card">
        <div class="gesture-name">✋ Full Hand</div>
        <div class="gesture-action">Drag and drop</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style='background: rgba(59, 130, 246, 0.1); padding: 1rem; border-radius: 8px; border-left: 3px solid #3b82f6;'>
        <p style='color: #93c5fd; margin: 0; font-size: 0.9rem;'>
            <strong>💡 Pro Tip:</strong> Ensure good lighting and position your hand 1-2 feet from the camera for best results.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Status display
col_status1, col_status2, col_status3 = st.columns([1, 2, 1])
with col_status2:
    if st.session_state.gesture_active:
        st.markdown('<div class="status-active">🟢 ACTIVE - CONTROLLING MOUSE</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-inactive">⚫ INACTIVE - READY TO START</div>', unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("""
    <div class="instructions">
        <div class="instruction-title">📋 Quick Start Guide</div>
        <div class="instruction-item">Click the green "Start Control" button below</div>
        <div class="instruction-item">Position your hand in front of the camera</div>
        <div class="instruction-item">Use different finger gestures to control the mouse</div>
        <div class="instruction-item">Click "Stop Control" to end the session</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Current status info
    if st.session_state.gesture_active:
        st.markdown("""
        <div class="alert-box">
            <strong>✅ System Active:</strong> Your mouse is now being controlled by hand gestures. Make sure your hand is visible to the camera.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alert-box">
            <strong>ℹ️ Ready to begin:</strong> Click the "Start Control" button to activate gesture-based mouse control.
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stats-container">
        <div class="stat-box">
            <span class="stat-value">🖐️</span>
            <div class="stat-label">Gesture Recognition</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Features section (only show when inactive)
if not st.session_state.gesture_active:
    st.markdown("### ✨ Key Features")
    feat_col1, feat_col2, feat_col3, feat_col4 = st.columns(4)
    
    with feat_col1:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🎯</span>
            <div class="feature-title">Precise Control</div>
            <div class="feature-desc">Accurate cursor movement with minimal lag</div>
        </div>
        """, unsafe_allow_html=True)
    
    with feat_col2:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">⚡</span>
            <div class="feature-title">Fast Response</div>
            <div class="feature-desc">Real-time gesture recognition</div>
        </div>
        """, unsafe_allow_html=True)
    
    with feat_col3:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🤖</span>
            <div class="feature-title">AI Powered</div>
            <div class="feature-desc">Advanced hand tracking technology</div>
        </div>
        """, unsafe_allow_html=True)
    
    with feat_col4:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🎨</span>
            <div class="feature-title">Intuitive</div>
            <div class="feature-desc">Natural gesture-based interface</div>
        </div>
        """, unsafe_allow_html=True)

# Control buttons section
st.markdown("---")
st.markdown("### 🎮 Control Panel")

btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])

with btn_col1:
    if st.button("🟢 Start Control", key="start_btn"):
        if not st.session_state.gesture_active:
            try:
                start_control()
                st.session_state.gesture_active = True
                st.success("✅ Gesture control started successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to start control: {str(e)}")
        else:
            st.info("ℹ️ Gesture control is already running.")

with btn_col2:
    if st.button("🔴 Stop Control", key="stop_btn"):
        if st.session_state.gesture_active:
            try:
                stop_control()
                st.session_state.gesture_active = False
                st.warning("⚠️ Gesture control stopped.")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to stop control: {str(e)}")
        else:
            st.info("ℹ️ Gesture control is not running.")

# Information section at bottom
st.markdown("---")
info_col1, info_col2 = st.columns(2)

with info_col1:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">⚙️</span>
        <div class="feature-title">System Requirements</div>
        <div class="feature-desc">
            • Webcam with at least 720p resolution<br>
            • Good lighting conditions<br>
            • Clear background for better detection<br>
            • Python 3.7+ with required packages
        </div>
    </div>
    """, unsafe_allow_html=True)

with info_col2:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">🛡️</span>
        <div class="feature-title">Privacy & Security</div>
        <div class="feature-desc">
            • All processing done locally on your device<br>
            • No video data is stored or transmitted<br>
            • Camera access only when control is active<br>
            • Complete control over when to start/stop
        </div>
    </div>
    """, unsafe_allow_html=True)
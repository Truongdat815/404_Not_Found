"""
Main Streamlit Application
Requirements Engineering App
"""

import streamlit as st
from core.agent import app

# Configure page
st.set_page_config(
    page_title="AI Requirements Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# Inject global CSS to override Streamlit defaults - DARK THEME
st.markdown("""
<style>
    /* Hide Streamlit branding and menu */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    
    /* Global font and DARK background */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Dark background */
    html, body, .stApp, .stApp > div {
        background: #0f0f0f !important;
        background-color: #0f0f0f !important;
        color: #ffffff !important;
    }
    
    /* Main container - Dark */
    .main {
        background: #0f0f0f !important;
        background-color: #0f0f0f !important;
    }
    
    .main .block-container {
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
        max-width: 1400px !important;
        background: transparent !important;
    }
    
    /* Override Streamlit sidebar - Dark */
    section[data-testid="stSidebar"],
    div[data-testid="stSidebar"] {
        background: #1a1a1a !important;
    }
    
    /* All text should be white */
    p, span, div, label {
        color: #ffffff !important;
    }
    
    /* Better title styling - Dark theme with gradient */
    h1 {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #818cf8 0%, #a78bfa 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2, h3 {
        color: #e5e5e5 !important;
        font-weight: 700 !important;
    }
    
    /* Hide default sidebar styling if needed */
    .css-1d391kg {
        padding-top: 3rem !important;
    }
    
    /* Force dark theme on all Streamlit elements */
    [data-baseweb="base-input"],
    [data-baseweb="input"],
    .stTextInput > div > div > input {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
        border-color: #4a4a4a !important;
    }
    
    /* File uploader - Dark */
    .stFileUploader > div {
        background-color: #1a1a1a !important;
        border-color: #4a4a4a !important;
    }
    
    /* Buttons - Dark with gradient */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: #ffffff !important;
    }
    
    /* Success/Error messages - Dark */
    .stSuccess {
        background-color: #1e3a1e !important;
        color: #86efac !important;
    }
    
    .stError {
        background-color: #3a1e1e !important;
        color: #fca5a5 !important;
    }
    
    .stInfo {
        background-color: #1e1e3a !important;
        color: #a5b4fc !important;
    }
    
    /* Sidebar text - Dark */
    .sidebar .sidebar-content {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
    }
    
    .sidebar .sidebar-content * {
        color: #ffffff !important;
    }
    
    /* Radio button - Dark */
    .stRadio > div > label {
        color: #ffffff !important;
    }
    
    /* Spinner - Dark */
    .stSpinner > div {
        border-top-color: #818cf8 !important;
    }
</style>
""", unsafe_allow_html=True)

# Main title with better styling
st.markdown("<h1 style='text-align: center; margin-bottom: 0.5rem;'>🤖 AI Requirements Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a78bfa; font-size: 1.1rem; font-weight: 600; margin-bottom: 2rem;'>✨ Powered by LangGraph and Google Gemini ✨</p>", unsafe_allow_html=True)

# IMPORTANT: Show file upload at the very top level
st.markdown("---")
st.markdown("""
<h2 style='
    font-size: 1.75rem;
    font-weight: 700;
    color: #a78bfa;
    margin-bottom: 0.5rem;
'>📁 UPLOAD FILE ĐỂ PHÂN TÍCH</h2>
""", unsafe_allow_html=True)
st.markdown("<p style='color: #818cf8; font-weight: 600; margin-bottom: 1rem;'>**Chọn file .txt hoặc .docx chứa SRS/User Stories**</p>", unsafe_allow_html=True)

uploaded_file_top = st.file_uploader(
    "📎 CHỌN FILE",
    type=['txt', 'docx'],
    help="Chọn file để phân tích",
    label_visibility="visible",
    key="main_file_uploader"
)

if uploaded_file_top:
    file_size = f"{uploaded_file_top.size / 1024:.2f} KB"
    st.success(f"✅ **File đã chọn:** {uploaded_file_top.name} ({file_size})")
    
    if st.button("🔍 PHÂN TÍCH FILE NÀY", type="primary", use_container_width=True, key="main_analyze_btn"):
        try:
            with st.spinner("🤖 Đang phân tích file... Vui lòng đợi 10-30 giây"):
                response = app.analyze_file(uploaded_file_top)
                
                if response and "error" not in response:
                    conflicts = len(response.get('conflicts', []))
                    ambiguities = len(response.get('ambiguities', []))
                    suggestions = len(response.get('suggestions', []))
                    st.success(
                        f"✅ **Phân tích hoàn tất!** "
                        f"Tìm thấy {conflicts} xung đột, "
                        f"{ambiguities} mơ hồ, "
                        f"{suggestions} đề xuất"
                    )
                    # Store result for display
                    if 'analysis_results' not in st.session_state:
                        st.session_state.analysis_results = []
                    st.session_state.analysis_results.append(response)
                    st.rerun()
                else:
                    error_msg = response.get("error", "Unknown error") if response else "Failed to analyze"
                    st.error(f"❌ Lỗi: {error_msg}")
        except Exception as e:
            st.error(f"❌ Lỗi: {str(e)}")

st.markdown("---")

# Navigation sidebar
st.sidebar.title("Navigation")
st.sidebar.markdown("### Pages")
page = st.sidebar.radio(
    "Select a page",
    ["Analyze Document", "About"],
    label_visibility="collapsed"
)

# Route to pages
if page == "Analyze Document":
    # Import and show Analyze Document page
    # Note: Streamlit will automatically detect pages/1_Analyze_Document.py
    # but we can also import it directly here for custom navigation
    import sys
    from pathlib import Path
    
    # Add pages directory to path if needed
    pages_path = Path(__file__).parent / "pages"
    if str(pages_path) not in sys.path:
        sys.path.insert(0, str(pages_path))
    
    # Import using the actual module name (1_Analyze_Document)
    import importlib
    analyze_module = importlib.import_module("1_Analyze_Document")
    analyze_module.show()
elif page == "About":
    st.header("About")
    st.markdown("""
    <div style='color: #ffffff;'>
    This is a Requirements Engineering App that analyzes SRS/User Stories to detect 
    conflicts, ambiguities, and provide suggestions for improvement.
    
    **Features:**
    - 🔍 Detect conflicts in requirements
    - ❓ Identify ambiguities
    - 💡 Provide improvement suggestions
    - 📊 Show analysis metrics
    
    **Built with Streamlit**
    </div>
    """, unsafe_allow_html=True)


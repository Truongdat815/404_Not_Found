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

# Inject global CSS to override Streamlit defaults and improve styling
st.markdown("""
<style>
    /* Hide Streamlit branding and menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Global font and background */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }
    
    /* Improve main container */
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1400px !important;
    }
    
    /* Better title styling */
    h1 {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem !important;
    }
    
    /* Hide default sidebar styling if needed */
    .css-1d391kg {
        padding-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# Main title with better styling
st.markdown("<h1 style='text-align: center; margin-bottom: 0.5rem;'>🤖 AI Requirements Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6b7280; font-size: 1.1rem; margin-bottom: 2rem;'>Powered by LangGraph and Google Gemini</p>", unsafe_allow_html=True)

# IMPORTANT: Show file upload at the very top level
st.markdown("---")
st.markdown("## 📁 UPLOAD FILE ĐỂ PHÂN TÍCH")
st.markdown("**Chọn file .txt hoặc .docx chứa SRS/User Stories**")

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
    This is a Requirements Engineering App that analyzes SRS/User Stories to detect 
    conflicts, ambiguities, and provide suggestions for improvement.
    
    **Features:**
    - 🔍 Detect conflicts in requirements
    - ❓ Identify ambiguities
    - 💡 Provide improvement suggestions
    - 📊 Show analysis metrics
    
    **Built with Streamlit**
    """)


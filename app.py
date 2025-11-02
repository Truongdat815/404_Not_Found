"""
Main Streamlit Application
Requirements Engineering App
"""

import streamlit as st

# Configure page
st.set_page_config(
    page_title="Requirements Engineering App",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main title
st.title("📋 Requirements Engineering App")
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


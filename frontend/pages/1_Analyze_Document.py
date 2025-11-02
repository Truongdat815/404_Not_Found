"""
Chat-Based Requirements Engineering AI Assistant
Claude-like interface for interacting with AI agent
"""

import streamlit as st
from core.agent import app
from datetime import datetime
import json
import time


def show():
    """Display the chat-based AI Assistant interface"""
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello! I'm your Requirements Engineering AI Assistant. I can help you:\n\n• Analyze full SRS/User Stories documents\n• Answer questions about requirements\n• Generate test cases\n• Explain detected conflicts\n\nJust paste a document or ask me a question!",
                "timestamp": datetime.now().isoformat(),
                "function_used": "welcome"
            }
        ]
    
    if "processing" not in st.session_state:
        st.session_state.processing = False
    
    # Apply modern, beautiful CSS styling - DARK THEME
    st.markdown("""
    <style>
    /* Dark background */
    html, body {
        background: #0f0f0f !important;
        background-color: #0f0f0f !important;
        min-height: 100vh !important;
    }
    
    .stApp, .stApp > div, [data-testid="stAppViewContainer"] {
        background: #0f0f0f !important;
        background-color: #0f0f0f !important;
        min-height: 100vh !important;
        color: #ffffff !important;
    }
    
    .main {
        background: #0f0f0f !important;
        background-color: #0f0f0f !important;
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem !important;
        max-width: 1400px !important;
        margin: 0 auto !important;
    }
    
    /* Smooth page transitions */
    * {
        transition: background-color 0.3s ease, color 0.3s ease !important;
    }
    
    /* Smooth scroll */
    html {
        scroll-behavior: smooth !important;
    }
    
    /* Chat message styling with smooth animations */
    .chat-message {
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 0.5rem;
        animation: fadeIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    @keyframes fadeIn {
        from { 
            opacity: 0; 
            transform: translateY(20px) scale(0.96);
        }
        to { 
            opacity: 1; 
            transform: translateY(0) scale(1);
        }
    }
    
    /* User messages (right-aligned) - Fit content width - Dark theme */
    .user-message {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        margin-left: auto !important;
        margin-right: 0 !important;
        margin-bottom: 1.5rem !important;
        border-radius: 1.5rem 1.5rem 0.25rem 1.5rem !important;
        padding: 1rem 1.5rem !important;
        text-align: left !important;
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.5) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: none !important;
        display: inline-block !important;
        max-width: 70% !important;
        min-width: fit-content !important;
        width: auto !important;
        animation: slideInRight 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px) scale(0.95);
        }
        to {
            opacity: 1;
            transform: translateX(0) scale(1);
        }
    }
    
    .user-message:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 12px 32px rgba(99, 102, 241, 0.6) !important;
        background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%) !important;
    }
    
    /* Assistant messages (left-aligned) - Fit content width - Gray theme */
    .assistant-message,
    div.assistant-message,
    [class*="assistant-message"],
    div[class*="assistant-message"] {
        background: #555555 !important;
        background-color: #555555 !important;
        background-image: none !important;
        color: #ffffff !important;
        margin-left: 0 !important;
        margin-right: auto !important;
        margin-bottom: 1.5rem !important;
        border-radius: 1.5rem 1.5rem 1.5rem 0.25rem !important;
        padding: 1rem 1.5rem !important;
        border-left: 5px solid #818cf8 !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border-top: 1px solid rgba(129, 140, 248, 0.3) !important;
        border-right: 1px solid rgba(129, 140, 248, 0.3) !important;
        border-bottom: 1px solid rgba(129, 140, 248, 0.3) !important;
        display: inline-block !important;
        max-width: 70% !important;
        min-width: fit-content !important;
        width: auto !important;
        animation: slideInLeft 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    /* Force all child elements to use gray background and white text */
    .assistant-message *,
    div.assistant-message *,
    [class*="assistant-message"] *,
    .assistant-message p,
    .assistant-message span,
    .assistant-message div,
    .assistant-message strong,
    .assistant-message em,
    .assistant-message br {
        background: transparent !important;
        background-color: transparent !important;
        background-image: none !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        text-fill-color: #ffffff !important;
    }
    
    /* Override any Streamlit markdown containers inside assistant messages */
    .assistant-message .stMarkdown,
    .assistant-message [data-testid="stMarkdownContainer"],
    div.assistant-message .stMarkdown,
    div.assistant-message [data-testid="stMarkdownContainer"] {
        background: transparent !important;
        background-color: transparent !important;
        color: #ffffff !important;
    }
    
    .assistant-message .stMarkdown *,
    .assistant-message [data-testid="stMarkdownContainer"] * {
        background: transparent !important;
        background-color: transparent !important;
        color: #ffffff !important;
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px) scale(0.95);
        }
        to {
            opacity: 1;
            transform: translateX(0) scale(1);
        }
    }
    
    .assistant-message:hover,
    div.assistant-message:hover,
    [class*="assistant-message"]:hover {
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5) !important;
        transform: translateX(4px) scale(1.01) !important;
        background: #606060 !important;
        background-color: #606060 !important;
        background-image: none !important;
    }
    
    /* Override any white backgrounds that might be applied by Streamlit */
    div[style*="background"]:has(.assistant-message),
    div[style*="background-color: white"],
    div[style*="background-color: #fff"],
    div[style*="background-color: #ffffff"] {
        background: #555555 !important;
        background-color: #555555 !important;
    }
    
    /* Force override for any div containing assistant messages */
    div:has(> .assistant-message),
    div:has(.assistant-message) {
        background: transparent !important;
    }
    
    /* Override Streamlit's default element backgrounds */
    [data-testid="stMarkdownContainer"]:has(.assistant-message),
    .element-container:has(.assistant-message),
    div[data-testid="element-container"]:has(.assistant-message) {
        background: transparent !important;
        background-color: transparent !important;
    }
    
    /* Target ALL possible Streamlit containers that might have white backgrounds */
    div[data-testid="stMarkdownContainer"],
    .stMarkdown,
    [class*="stMarkdown"],
    div[data-testid="element-container"],
    .element-container {
        background: transparent !important;
        background-color: transparent !important;
    }
    
    /* Specifically override any white backgrounds in markdown containers */
    div[data-testid="stMarkdownContainer"]:has(> div:has(.assistant-message)),
    .stMarkdown:has(.assistant-message),
    [class*="stMarkdown"]:has(.assistant-message) {
        background: transparent !important;
        background-color: transparent !important;
    }
    
    /* Override any inline styles that Streamlit might add */
    div[style*="background-color: rgb(255, 255, 255)"],
    div[style*="background-color:white"],
    div[style*="background-color:#fff"],
    div[style*="background-color:#ffffff"],
    div[style*="background:white"],
    div[style*="background:#fff"],
    div[style*="background:#ffffff"] {
        background: #555555 !important;
        background-color: #555555 !important;
    }
    
    /* CRITICAL: Override Streamlit's markdown container that wraps our HTML */
    div[data-testid="stMarkdownContainer"] div:has(> div[style*="background: #555555"]),
    div[data-testid="stMarkdownContainer"] > div > div[style*="background: #555555"],
    [data-testid="stMarkdownContainer"] > div,
    [data-testid="stMarkdownContainer"] {
        background: transparent !important;
        background-color: transparent !important;
    }
    
    /* Force all divs inside markdown containers to not have white backgrounds */
    [data-testid="stMarkdownContainer"] > div[style*="background"],
    [data-testid="stMarkdownContainer"] > div > div {
        background: transparent !important;
        background-color: transparent !important;
    }
    
    /* Override ANY white background anywhere in the app - especially in markdown containers */
    [data-testid="stMarkdownContainer"] div[style*="background"]:not([style*="background: transparent"]):not([style*="background-color: transparent"]):not([style*="background: #555555"]):not([style*="background-color: #555555"]) {
        background: transparent !important;
        background-color: transparent !important;
    }
    
    /* Chat input styling - Dark */
    .stTextInput > div > div > input {
        border-radius: 2rem;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        background-color: #2d2d2d !important;
        color: #ffffff !important;
        border-color: #4a4a4a !important;
    }
    
    /* File upload button styling - Dark */
    .stFileUploader > div {
        border: 3px dashed #818cf8 !important;
        border-radius: 1.5rem !important;
        padding: 3rem 2.5rem !important;
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 16px rgba(129, 140, 248, 0.3) !important;
    }
    
    .stFileUploader > div:hover {
        border-color: #a78bfa !important;
        background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%) !important;
        transform: translateY(-4px) scale(1.01) !important;
        box-shadow: 0 12px 32px rgba(129, 140, 248, 0.5) !important;
    }
    
    /* Button styling - Dark gradients */
    .stButton > button {
        border-radius: 1rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        border: none !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5) !important;
        color: white !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.05) !important;
        box-shadow: 0 12px 32px rgba(99, 102, 241, 0.7) !important;
        background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-2px) scale(1.02) !important;
    }
    
    /* Primary button special styling - Dark */
    .stButton > button[data-baseweb="button"][kind="primary"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    }
    
    /* Results formatting - Dark */
    .analysis-results {
        background-color: #1a1a1a;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-top: 1rem;
        color: #ffffff !important;
    }
    
    /* Column styling for 3-column layout - Dark Cards */
    .analysis-column {
        background: #1a1a1a !important;
        border-radius: 1.25rem !important;
        padding: 2rem !important;
        margin: 1rem !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.5) !important;
        min-height: 500px !important;
        height: 100% !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: 2px solid #4a4a4a !important;
        overflow-y: auto !important;
        max-height: 600px !important;
        color: #ffffff !important;
    }
    
    .analysis-column * {
        color: #ffffff !important;
    }
    
    .analysis-column:hover {
        transform: translateY(-6px) scale(1.02) !important;
        box-shadow: 0 16px 48px rgba(129, 140, 248, 0.4) !important;
        background: #2d2d2d !important;
        border-color: #818cf8 !important;
    }
    
    /* Smooth animations for all interactive elements */
    button, .stButton > button {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    button:hover, .stButton > button:hover {
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    /* Smooth page load animation */
    .main .block-container {
        animation: fadeInPage 0.6s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    @keyframes fadeInPage {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Smooth scrollbar - Dark */
    ::-webkit-scrollbar {
        width: 10px;
        transition: width 0.3s ease !important;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
        border-radius: 10px;
        transition: background 0.3s ease !important;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #4a4a4a;
        border-radius: 10px;
        transition: background 0.3s ease !important;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #6a6a6a;
    }
    
    .conflict-column {
        border-top: 5px solid #ef4444 !important;
        background: linear-gradient(135deg, #2d1a1a 0%, #1a1a1a 100%) !important;
    }
    
    .ambiguity-column {
        border-top: 5px solid #f59e0b !important;
        background: linear-gradient(135deg, #2d2a1a 0%, #1a1a1a 100%) !important;
    }
    
    .suggestion-column {
        border-top: 5px solid #10b981 !important;
        background: linear-gradient(135deg, #1a2d1a 0%, #1a1a1a 100%) !important;
    }
    
    .column-header {
        font-size: 1.35rem !important;
        font-weight: 700 !important;
        margin-bottom: 1.25rem !important;
        padding-bottom: 0.875rem !important;
        border-bottom: 2px solid #4a4a4a !important;
        color: #ffffff !important;
        letter-spacing: -0.02em !important;
    }
    
    .conflict-item, .ambiguity-item, .suggestion-item {
        background: #2d2d2d !important;
        border-left: 5px solid #818cf8 !important;
        padding: 1.25rem !important;
        margin: 1rem 0 !important;
        border-radius: 0.75rem !important;
        color: #ffffff !important;
        font-size: 0.95rem !important;
        line-height: 1.7 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
        transition: all 0.3s ease !important;
        border: 1px solid #4a4a4a !important;
    }
    
    .conflict-item:hover, .ambiguity-item:hover, .suggestion-item:hover {
        transform: translateX(4px) !important;
        box-shadow: 0 4px 12px rgba(129, 140, 248, 0.3) !important;
        background: #3d3d3d !important;
    }
    
    .conflict-item *, .ambiguity-item *, .suggestion-item * {
        color: #ffffff !important;
    }
    
    .conflict-item strong, .ambiguity-item strong, .suggestion-item strong {
        color: #ffffff !important;
        font-weight: 700 !important;
        display: inline-block !important;
        margin-top: 0.5rem !important;
    }
    
    .conflict-item p, .ambiguity-item p, .suggestion-item p {
        color: #ffffff !important;
        margin: 0.5rem 0 !important;
    }
    
    .ambiguity-item {
        border-left-color: #fbbf24;
    }
    
    .suggestion-item {
        border-left-color: #34d399;
    }
    
    .empty-state {
        color: #a0a0a0 !important;
        text-align: center !important;
        padding: 3rem 2rem !important;
        font-style: italic !important;
        font-size: 1rem !important;
        background: #1a1a1a !important;
        border-radius: 0.75rem !important;
        border: 2px dashed #4a4a4a !important;
    }
    
    /* Force all text in analysis columns to be readable */
    .analysis-column h1, .analysis-column h2, .analysis-column h3,
    .analysis-column p, .analysis-column div, .analysis-column span {
        color: #ffffff !important;
    }
    
    /* Override Streamlit default text colors */
    .stMarkdown h3 {
        color: #ffffff !important;
    }
    
    /* Force ALL text in analysis results to be readable */
    .conflict-column, .ambiguity-column, .suggestion-column {
        color: #ffffff !important;
    }
    
    .conflict-column *, .ambiguity-column *, .suggestion-column * {
        color: #ffffff !important;
    }
    
    /* Override any Streamlit text colors */
    [data-testid="stMarkdownContainer"] h3 {
        color: #ffffff !important;
    }
    
    /* Ensure text in expandable sections is readable */
    .streamlit-expanderHeader {
        color: #ffffff !important;
    }
    
    /* Force text in all markdown containers */
    .stMarkdown {
        color: #ffffff !important;
    }
    
    .stMarkdown * {
        color: #ffffff !important;
    }
    
    /* Metrics styling - Dark */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #818cf8 !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        color: #a0a0a0 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Input fields - Dark styling */
    .stTextArea > div > div > textarea {
        border-radius: 1rem !important;
        border: 2px solid #4a4a4a !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        background: #2d2d2d !important;
        color: #ffffff !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.2) !important;
        background: #2d2d2d !important;
        color: #ffffff !important;
    }
    
    /* Success/Error messages - Dark */
    .stSuccess {
        background: #1e3a1e !important;
        border-left: 5px solid #10b981 !important;
        border-radius: 0.75rem !important;
        padding: 1rem !important;
        color: #86efac !important;
    }
    
    .stError {
        background: #3a1e1e !important;
        border-left: 5px solid #ef4444 !important;
        border-radius: 0.75rem !important;
        padding: 1rem !important;
        color: #fca5a5 !important;
    }
    
    .stInfo {
        background: #1e1e3a !important;
        border-left: 5px solid #818cf8 !important;
        border-radius: 0.75rem !important;
        padding: 1rem !important;
        color: #a5b4fc !important;
    }
    
    /* Section headers - Dark */
    h2, h3 {
        color: #e5e5e5 !important;
        font-weight: 700 !important;
    }
    
    /* Dividers - Dark */
    hr {
        border-top: 2px solid #4a4a4a !important;
        margin: 2rem 0 !important;
    }
    
    /* Improve scrollbar - Dark */
    .analysis-column::-webkit-scrollbar {
        width: 8px;
    }
    
    .analysis-column::-webkit-scrollbar-track {
        background: #1a1a1a;
        border-radius: 10px;
    }
    
    .analysis-column::-webkit-scrollbar-thumb {
        background: #4a4a4a;
        border-radius: 10px;
    }
    
    .analysis-column::-webkit-scrollbar-thumb:hover {
        background: #6a6a6a;
    }
    </style>
    
    <script>
    // Optimized version - only fix when needed, debounced
    let fixedMessages = new Set();
    let isProcessing = false;
    
    function fixAssistantMessages() {
        if (isProcessing) return;
        isProcessing = true;
        
        try {
            // Find all elements with assistant-message class
            const assistantMessages = document.querySelectorAll('.assistant-message');
            assistantMessages.forEach(msg => {
                const msgId = msg.getAttribute('data-msg-id') || Math.random().toString();
                if (!msg.getAttribute('data-msg-id')) {
                    msg.setAttribute('data-msg-id', msgId);
                }
                
                // Only fix if not already fixed
                if (!fixedMessages.has(msgId) || msg.style.backgroundColor !== 'rgb(85, 85, 85)') {
                    msg.style.setProperty('background', '#555555', 'important');
                    msg.style.setProperty('background-color', '#555555', 'important');
                    msg.style.setProperty('color', '#ffffff', 'important');
                    msg.style.setProperty('background-image', 'none', 'important');
                    
                    // Fix child elements - only if needed
                    const children = msg.querySelectorAll('*');
                    children.forEach(child => {
                        const childColor = getComputedStyle(child).color;
                        // Only set if not already white
                        if (childColor !== 'rgb(255, 255, 255)' && childColor !== '#ffffff') {
                            child.style.setProperty('color', '#ffffff', 'important');
                            child.style.setProperty('-webkit-text-fill-color', '#ffffff', 'important');
                        }
                        
                        // Remove white backgrounds
                        const bgColor = getComputedStyle(child).backgroundColor;
                        if (bgColor === 'rgb(255, 255, 255)' || bgColor === 'white') {
                            child.style.setProperty('background', 'transparent', 'important');
                            child.style.setProperty('background-color', 'transparent', 'important');
                        }
                    });
                    
                    fixedMessages.add(msgId);
                }
            });
            
            // Fix parent containers only once
            const parentDivs = document.querySelectorAll('div');
            parentDivs.forEach(div => {
                if (div.querySelector('.assistant-message')) {
                    const bgColor = getComputedStyle(div).backgroundColor;
                    if (bgColor === 'rgb(255, 255, 255)' || bgColor === 'white') {
                        div.style.setProperty('background', 'transparent', 'important');
                        div.style.setProperty('background-color', 'transparent', 'important');
                    }
                }
            });
        } catch (e) {
            console.warn('Error fixing messages:', e);
        } finally {
            isProcessing = false;
        }
    }
    
    // Debounced version
    let debounceTimer;
    function debouncedFix() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(fixAssistantMessages, 100);
    }
    
    // Run once on load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(fixAssistantMessages, 100);
        });
    } else {
        setTimeout(fixAssistantMessages, 100);
    }
    
    // Use MutationObserver with debouncing - only watch for new elements
    const observer = new MutationObserver((mutations) => {
        let hasNewMessage = false;
        mutations.forEach(mutation => {
            if (mutation.addedNodes.length > 0) {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === 1 && 
                        (node.classList.contains('assistant-message') || 
                         node.querySelector('.assistant-message'))) {
                        hasNewMessage = true;
                    }
                });
            }
        });
        if (hasNewMessage) {
            debouncedFix();
        }
    });
    
    // Start observing - only watch for new nodes, not all changes
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // Fallback: check less frequently (every 2 seconds instead of 500ms)
    setInterval(fixAssistantMessages, 2000);
    </script>
    """, unsafe_allow_html=True)
    
    # ============================================
    # FILE UPLOAD SECTION - MOVED TO TOP (VERY VISIBLE)
    # ============================================
    st.markdown("---")
    
    # Big, visible section header - Dark theme
    st.markdown("""
    <h2 style='
        text-align: center;
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #818cf8 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    '>📁 UPLOAD FILE ĐỂ PHÂN TÍCH</h2>
    """, unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.1rem; color: #a78bfa; font-weight: 600; margin-bottom: 1.5rem;'>Chọn file .txt hoặc .docx chứa SRS/User Stories để AI phân tích</p>", unsafe_allow_html=True)
    
    # Very visible upload box - Dark theme
    st.markdown("""
    <div style='
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        padding: 2.5rem;
        border-radius: 1.25rem;
        margin-bottom: 2rem;
        border: 3px dashed #818cf8;
        box-shadow: 0 8px 24px rgba(129, 140, 248, 0.3);
        transition: all 0.3s ease;
    '>
    """, unsafe_allow_html=True)
    
    # File uploader - MUST BE VISIBLE
    uploaded_file = st.file_uploader(
        "📎 CHỌN FILE .TXT HOẶC .DOCX",
        type=['txt', 'docx'],
        help="Kéo thả file vào đây hoặc click để chọn file",
        label_visibility="visible",
        key="file_uploader_main"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Show file info and analyze button
    if uploaded_file is not None:
        file_details = {
            "Filename": uploaded_file.name,
            "FileType": uploaded_file.type,
            "FileSize": f"{uploaded_file.size / 1024:.2f} KB"
        }
        
        # File info display
        st.success(f"✅ **File đã chọn:** {uploaded_file.name} ({file_details['FileSize']})")
        
        # Big analyze button - VERY VISIBLE
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_button = st.button(
            "🔍 PHÂN TÍCH FILE NÀY",
            type="primary",
            use_container_width=True,
            help="Click để AI phân tích file của bạn",
            key="analyze_file_button_main"
        )
        
        # Analyze file when button is clicked
        if analyze_button:
            st.session_state.messages.append({
                "role": "user",
                "content": f"📁 Uploaded file: **{uploaded_file.name}** ({file_details['FileSize']})",
                "timestamp": datetime.now().isoformat()
            })
            
            st.session_state.processing = True
            try:
                # Show progress
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.info("🔍 Đang kiểm tra kết nối backend...")
                progress_bar.progress(10)
                
                status_text.info("📤 Đang upload file lên backend...")
                progress_bar.progress(30)
                
                # Estimate time based on file size
                file_size_kb = uploaded_file.size / 1024
                if file_size_kb < 50:
                    estimated_time = "30-45 giây"
                elif file_size_kb < 200:
                    estimated_time = "45-60 giây"
                else:
                    estimated_time = "60-90 giây"
                
                status_text.info(f"🤖 Backend đang phân tích file... (Ước tính: {estimated_time})")
                progress_bar.progress(50)
                
                response = app.analyze_file(uploaded_file)
                
                progress_bar.progress(90)
                status_text.info("✅ Đang xử lý kết quả...")
                
                if response and "error" not in response:
                    progress_bar.progress(100)
                    status_text.empty()
                    progress_bar.empty()
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "timestamp": datetime.now().isoformat(),
                        "function_used": "analyze_requirements"
                    })
                    app.current_document = response
                    
                    conflicts_count = len(response.get('conflicts', []))
                    ambiguities_count = len(response.get('ambiguities', []))
                    suggestions_count = len(response.get('suggestions', []))
                    st.success(
                        f"✅ **Phân tích hoàn tất!** "
                        f"Tìm thấy {conflicts_count} xung đột, "
                        f"{ambiguities_count} mơ hồ, "
                        f"{suggestions_count} đề xuất"
                    )
                    
                    # Also add error message to chat if there's an error field
                    if "error" in response:
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": {"message": response["error"]},
                            "timestamp": datetime.now().isoformat(),
                            "function_used": "error"
                        })
                    
                    st.rerun()
                else:
                    progress_bar.empty()
                    status_text.empty()
                    error_msg = response.get("error", "Unknown error") if response else "Failed to analyze file"
                    st.error(f"❌ **Lỗi:** {error_msg}")
                    
                    # Add error to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": {"message": error_msg, "error": error_msg},
                        "timestamp": datetime.now().isoformat(),
                        "function_used": "error"
                    })
            except Exception as e:
                st.error(f"❌ **Lỗi khi phân tích file:** {str(e)}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": {"message": f"❌ Lỗi: {str(e)}", "error": str(e)},
                    "timestamp": datetime.now().isoformat(),
                    "function_used": "error"
                })
            finally:
                st.session_state.processing = False
    else:
        st.info("👆 **Chọn file ở trên** để upload và phân tích document SRS/User Stories của bạn (.txt hoặc .docx)")
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    # ============================================
    # CHAT HISTORY DISPLAY
    # ============================================
    st.markdown("""
    <h3 style='
        font-size: 1.75rem;
        font-weight: 700;
        color: #a78bfa;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #818cf8;
    '>💬 Lịch sử chat</h3>
    """, unsafe_allow_html=True)
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            role = message.get("role", "assistant")
            content = message.get("content", "")
            function_used = message.get("function_used", "unknown")
            
            # Format message display
            if role == "user":
                # Escape HTML and format content
                import html
                escaped_content = html.escape(str(content))
                escaped_content = escaped_content.replace("\n", "<br>")
                st.markdown(f"""
                <div style="text-align: right; margin-bottom: 1rem;">
                    <div class="user-message">
                        <strong>You:</strong><br>
                        {escaped_content}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Check if this is an analysis result
                if function_used == "analyze_requirements" and isinstance(content, dict) and "conflicts" in content:
                    # Display formatted analysis results
                    display_analysis_results(content)
                else:
                    # Display regular message - Convert \n to <br> for proper line breaks
                    # Handle both string and dict content
                    display_text = ""
                    
                    # Handle different content types
                    if isinstance(content, dict):
                        # If it's a dict, extract message field
                        if "message" in content:
                            display_text = str(content["message"])
                        elif "error" in content:
                            display_text = f"❌ Error: {content['error']}"
                        else:
                            # Dict without message field - don't show raw dict
                            display_text = "Response received"
                    else:
                        # If it's a string, check if it's a dict string representation
                        content_str = str(content)
                        if (content_str.startswith("{'") or content_str.startswith('{"') or 
                            content_str.startswith("{") and "'message'" in content_str):
                            # It's a dict string, try to extract message
                            import re
                            # Try to extract message value using regex
                            message_match = re.search(r"'message'[\s]*:[\s]*[\"'](.*?)[\"']", content_str)
                            if message_match:
                                display_text = message_match.group(1)
                                # Replace \n in the extracted message
                                display_text = display_text.replace("\\n", "\n")
                            else:
                                # Fallback: try simple string find
                                if "'message':" in content_str:
                                    start = content_str.find("'message':") + len("'message':")
                                    # Find the end - look for next key or closing
                                    end_positions = [
                                        content_str.find(", 'function_used'", start),
                                        content_str.find("'function_used'", start),
                                        content_str.find(", ", start),
                                        content_str.find("}", start)
                                    ]
                                    end = min([pos for pos in end_positions if pos > start], default=len(content_str))
                                    if end > start:
                                        display_text = content_str[start:end].strip()
                                        # Clean up quotes
                                        display_text = display_text.strip('"').strip("'").strip()
                                        display_text = display_text.replace("\\n", "\n")
                                else:
                                    display_text = "Response received"
                        else:
                            # Regular string content
                            display_text = content_str
                    
                    # Make sure display_text is a valid string
                    if not display_text or not isinstance(display_text, str):
                        display_text = "Response received"
                    
                    # Convert \n to HTML line breaks and escape HTML to prevent XSS
                    import html
                    display_text = html.escape(display_text)
                    # Replace both escaped and actual newlines
                    display_text = display_text.replace("\\n", "<br>").replace("\n", "<br>")
                    
                    # Use HTML with inline styles and avoid Streamlit's markdown processing
                    import streamlit.components.v1 as components
                    
                    assistant_html = f"""
                    <div style="text-align: left; margin-bottom: 1rem; width: 100%;">
                        <div style="
                            background: #555555 !important; 
                            background-color: #555555 !important; 
                            background-image: none !important;
                            color: #ffffff !important; 
                            padding: 1rem 1.5rem !important; 
                            border-radius: 1.5rem 1.5rem 1.5rem 0.25rem !important; 
                            border-left: 5px solid #818cf8 !important; 
                            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important; 
                            display: inline-block !important; 
                            max-width: 70% !important;
                            min-width: fit-content !important;
                            margin: 0 !important;
                        ">
                            <div style="color: #ffffff !important; background: transparent !important; background-color: transparent !important; background-image: none !important;">
                                <strong style="color: #ffffff !important; background: transparent !important; background-color: transparent !important;">AI Assistant:</strong><br>
                                <div style="color: #ffffff !important; background: transparent !important; background-color: transparent !important; font-weight: normal !important; margin-top: 0.5rem;">{display_text}</div>
                            </div>
                        </div>
                    </div>
                    """
                    st.markdown(assistant_html, unsafe_allow_html=True)
    
    # ============================================
    # TEXT INPUT SECTION AT BOTTOM
    # ============================================
    st.markdown("---")
    st.markdown("### 💬 Or paste text below")
    st.markdown("<p style='color: #a0a0a0; margin-bottom: 1rem;'>Alternatively, paste your requirements text directly into the input field</p>", unsafe_allow_html=True)
    
    # Input section with centered styling
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        # Use a counter to force refresh input field
        if "input_counter" not in st.session_state:
            st.session_state.input_counter = 0
        
        user_input = st.text_area(
            "Type your message here...",
            height=100,
            key=f"chat_input_{st.session_state.input_counter}",
            help="Paste a document or ask a question",
            label_visibility="collapsed"
        )
    
    # Buttons row
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        send_button = st.button("Send", type="primary", use_container_width=True)
    with col2:
        clear_button = st.button("Clear Chat", use_container_width=True)
    with col3:
        export_button = st.button("Export Chat", use_container_width=True)
    with col4:
        # Model selection (placeholder for future use)
        pass
    
    # Handle send button
    if send_button and user_input and user_input.strip():
        # Store the input before clearing
        message_to_send = user_input.strip()
        
        # Increment counter to force input field refresh (clear)
        st.session_state.input_counter += 1
        
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": message_to_send,
            "timestamp": datetime.now().isoformat()
        })
        
        # Process message and get AI response
        st.session_state.processing = True
        
        try:
            # Detect if this is likely an analysis request (long text or keywords)
            is_analysis = len(message_to_send) > 500 or any(keyword in message_to_send.lower() for keyword in 
                ["requirement", "srs", "user story", "specification", "analyze", "phân tích"])
            
            if is_analysis:
                # Show detailed progress for analysis requests
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Estimate time based on text length
                text_length = len(message_to_send)
                if text_length < 1000:
                    estimated_time = "30-45 giây"
                elif text_length < 3000:
                    estimated_time = "45-60 giây"
                else:
                    estimated_time = "60-90 giây"
                
                status_text.info(f"🔍 Đang phân tích... (Ước tính: {estimated_time})")
                progress_bar.progress(10)
                
                # Get response from agent
                response = app.process_message(message_to_send, app.current_document)
                
                progress_bar.progress(80)
                status_text.info("✅ Đang xử lý kết quả...")
                
                # Add AI response - ensure it's properly formatted
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,  # response is already a dict with message/function_used
                    "timestamp": datetime.now().isoformat(),
                    "function_used": response.get("function_used", "unknown")
                })
                
                # Update document context if this was an analysis
                if response.get("function_used") == "analyze_requirements":
                    app.current_document = response
                    conflicts_count = len(response.get('conflicts', []))
                    ambiguities_count = len(response.get('ambiguities', []))
                    suggestions_count = len(response.get('suggestions', []))
                    
                    progress_bar.progress(100)
                    status_text.success(
                        f"✅ **Hoàn tất!** "
                        f"Tìm thấy {conflicts_count} xung đột, "
                        f"{ambiguities_count} mơ hồ, "
                        f"{suggestions_count} đề xuất"
                    )
                else:
                    progress_bar.progress(100)
                    status_text.empty()
                
                progress_bar.empty()
                time.sleep(0.5)  # Brief pause to show completion
                status_text.empty()
            else:
                # Simple spinner for short messages
                with st.spinner("🤖 Đang suy nghĩ..."):
                    response = app.process_message(message_to_send, app.current_document)
                    
                    # Add AI response
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "timestamp": datetime.now().isoformat(),
                        "function_used": response.get("function_used", "unknown")
                    })
                    
                    # Update document context if this was an analysis
                    if response.get("function_used") == "analyze_requirements":
                        app.current_document = response
                
        except Exception as e:
            st.session_state.messages.append({
                "role": "assistant",
                "content": {"message": f"❌ Error: {str(e)}", "error": str(e)},
                "timestamp": datetime.now().isoformat(),
                "function_used": "error"
            })
        finally:
            st.session_state.processing = False
            # Clear input by rerunning with counter incremented
            st.rerun()
    
    # Handle clear button
    if clear_button:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Chat cleared! How can I help you today?",
                "timestamp": datetime.now().isoformat(),
                "function_used": "welcome"
            }
        ]
        app.current_document = None
        st.rerun()
    
    # Handle export button
    if export_button:
        chat_history = json.dumps(st.session_state.messages, indent=2)
        st.download_button(
            "📥 Download Chat History",
            data=chat_history,
            file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )


def display_analysis_results(results: dict) -> None:
    """
    Display formatted analysis results in the chat with 3-column layout
    
    Args:
        results: Analysis results dictionary with conflicts, ambiguities, suggestions
    """
    analysis_msg_html = """
    <div style="
        background: #555555 !important; 
        background-color: #555555 !important; 
        background-image: none !important;
        color: #ffffff !important; 
        padding: 1rem 1.5rem !important; 
        border-radius: 1.5rem 1.5rem 1.5rem 0.25rem !important; 
        border-left: 5px solid #818cf8 !important; 
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important; 
        display: inline-block !important; 
        max-width: 70% !important;
        margin-bottom: 1.5rem !important;
    ">
        <div style="color: #ffffff !important; background: transparent !important; background-color: transparent !important;">
            <strong style="color: #ffffff !important; background: transparent !important; background-color: transparent !important;">AI Assistant:</strong><br>
            <div style="color: #ffffff !important; background: transparent !important; background-color: transparent !important; font-weight: normal !important; margin-top: 0.5rem;">I've completed the analysis of your requirements document.</div>
        </div>
    </div>
    """
    st.markdown(analysis_msg_html, unsafe_allow_html=True)
    
    # Get data
    conflicts = results.get("conflicts", [])
    ambiguities = results.get("ambiguities", [])
    suggestions = results.get("suggestions", [])
    
    # Display summary stats with icons
    st.markdown("<div style='background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); padding: 2rem; border-radius: 1rem; margin: 1.5rem 0;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: white; margin-bottom: 1.5rem; text-align: center; font-weight: 700;'>📊 Analysis Summary</h3>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🧩 Conflicts", len(conflicts), delta_color="inverse")
    with col2:
        st.metric("❓ Ambiguities", len(ambiguities), delta_color="inverse")
    with col3:
        st.metric("💡 Suggestions", len(suggestions), delta_color="normal")
    with col4:
        st.metric("📋 Total Issues", len(conflicts) + len(ambiguities) + len(suggestions))
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 3-column layout for results
    col_conflicts, col_ambiguities, col_suggestions = st.columns(3)
    
    # Column 1: Conflicts
    with col_conflicts:
        st.markdown("### 🧩 Conflicts Detected", help="Conflicts between requirements")
        st.markdown('<div class="analysis-column conflict-column">', unsafe_allow_html=True)
        
        if conflicts:
            for i, conflict in enumerate(conflicts, 1):
                req1 = conflict.get("req1", "N/A")
                req2 = conflict.get("req2", "N/A")
                desc = conflict.get("description", "No description")
                st.markdown(f"""
                <div class="conflict-item" style="background: #2d2d2d !important; color: #ffffff !important;">
                    <p style="color: #ffffff !important; font-weight: 700; margin-bottom: 0.5rem;"><strong>Conflict {i}:</strong></p>
                    <p style="color: #ffffff !important; margin: 0.5rem 0;"><strong>Req 1:</strong> {req1}</p>
                    <p style="color: #ffffff !important; margin: 0.5rem 0;"><strong>Req 2:</strong> {req2}</p>
                    <p style="color: #ffffff !important; margin: 0.5rem 0;"><strong>Issue:</strong> {desc}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="empty-state">
                ✅ No conflicts detected!
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Column 2: Ambiguities
    with col_ambiguities:
        st.markdown("### ❓ Ambiguities Detected", help="Unclear or ambiguous requirements")
        st.markdown('<div class="analysis-column ambiguity-column">', unsafe_allow_html=True)
        
        if ambiguities:
            for i, ambiguity in enumerate(ambiguities, 1):
                req = ambiguity.get("req", "N/A")
                issue = ambiguity.get("issue", "No issue described")
                st.markdown(f"""
                <div class="ambiguity-item" style="background: #2d2d2d !important; color: #ffffff !important;">
                    <p style="color: #ffffff !important; font-weight: 700; margin-bottom: 0.5rem;"><strong>Ambiguity {i}:</strong></p>
                    <p style="color: #ffffff !important; margin: 0.5rem 0;"><strong>Requirement:</strong> {req}</p>
                    <p style="color: #ffffff !important; margin: 0.5rem 0;"><strong>Issue:</strong> {issue}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="empty-state">
                ✅ No ambiguities detected!
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Column 3: Suggestions
    with col_suggestions:
        st.markdown("### 💡 Improvement Suggestions", help="Suggested improvements for requirements")
        st.markdown('<div class="analysis-column suggestion-column">', unsafe_allow_html=True)
        
        if suggestions:
            for i, suggestion in enumerate(suggestions, 1):
                req = suggestion.get("req", "N/A")
                new_version = suggestion.get("new_version", "No suggestion")
                st.markdown(f"""
                <div class="suggestion-item" style="background: #2d2d2d !important; color: #ffffff !important;">
                    <p style="color: #ffffff !important; font-weight: 700; margin-bottom: 0.5rem;"><strong>Suggestion {i}:</strong></p>
                    <p style="color: #ffffff !important; margin: 0.5rem 0;"><strong>Original:</strong> {req}</p>
                    <p style="color: #ffffff !important; margin: 0.5rem 0;"><strong>Improved:</strong> {new_version}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="empty-state">
                ✅ No suggestions at this time.
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)


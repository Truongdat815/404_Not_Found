"""
Chat-Based Requirements Engineering AI Assistant
Claude-like interface for interacting with AI agent
"""

import streamlit as st
from core.agent import app
from datetime import datetime
import json


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
    
    # Apply modern, beautiful CSS styling with strong overrides
    st.markdown("""
    <style>
    /* Force override Streamlit defaults */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 50%, #f8f9fa 100%) !important;
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem !important;
        max-width: 1400px !important;
        margin: 0 auto !important;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 0.5rem;
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* User messages (right-aligned) - Enhanced */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        margin-left: 20% !important;
        margin-bottom: 1.5rem !important;
        border-radius: 1.5rem 1.5rem 0.25rem 1.5rem !important;
        padding: 1.5rem 2rem !important;
        text-align: left !important;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.35) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: none !important;
    }
    
    .user-message:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 12px 32px rgba(102, 126, 234, 0.45) !important;
    }
    
    /* Assistant messages (left-aligned) - Enhanced */
    .assistant-message {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
        color: #1f2937 !important;
        margin-right: 20% !important;
        margin-bottom: 1.5rem !important;
        border-radius: 1.5rem 1.5rem 1.5rem 0.25rem !important;
        padding: 1.5rem 2rem !important;
        border-left: 5px solid #667eea !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border-top: 1px solid rgba(102, 126, 234, 0.1) !important;
        border-right: 1px solid rgba(102, 126, 234, 0.1) !important;
        border-bottom: 1px solid rgba(102, 126, 234, 0.1) !important;
    }
    
    .assistant-message:hover {
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15) !important;
        transform: translateX(4px) !important;
    }
    
    /* Chat input styling */
    .stTextInput > div > div > input {
        border-radius: 2rem;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
    }
    
    /* File upload button styling - Enhanced */
    .stFileUploader > div {
        border: 3px dashed #667eea !important;
        border-radius: 1.5rem !important;
        padding: 3rem 2.5rem !important;
        background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.15) !important;
    }
    
    .stFileUploader > div:hover {
        border-color: #764ba2 !important;
        background: linear-gradient(135deg, #f0f2ff 0%, #f8f9ff 100%) !important;
        transform: translateY(-4px) scale(1.01) !important;
        box-shadow: 0 12px 32px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Button styling - Modern gradient buttons - Enhanced */
    .stButton > button {
        border-radius: 1rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.35) !important;
        color: white !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.05) !important;
        box-shadow: 0 12px 32px rgba(102, 126, 234, 0.5) !important;
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-2px) scale(1.02) !important;
    }
    
    /* Primary button special styling */
    .stButton > button[data-baseweb="button"][kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    /* Results formatting */
    .analysis-results {
        background-color: #f0f0f0;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-top: 1rem;
    }
    
    /* Column styling for 3-column layout - Modern cards - Enhanced */
    .analysis-column {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
        border-radius: 1.25rem !important;
        padding: 2rem !important;
        margin: 1rem !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.12) !important;
        min-height: 500px !important;
        height: 100% !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: 1px solid rgba(0,0,0,0.08) !important;
        overflow-y: auto !important;
        max-height: 600px !important;
    }
    
    .analysis-column:hover {
        transform: translateY(-6px) scale(1.02) !important;
        box-shadow: 0 16px 48px rgba(0,0,0,0.18) !important;
    }
    
    .conflict-column {
        border-top: 5px solid #ef4444;
        background: linear-gradient(135deg, #fff5f5 0%, #ffffff 100%);
    }
    
    .ambiguity-column {
        border-top: 5px solid #f59e0b;
        background: linear-gradient(135deg, #fffbf0 0%, #ffffff 100%);
    }
    
    .suggestion-column {
        border-top: 5px solid #10b981;
        background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 100%);
    }
    
    .column-header {
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 1.25rem;
        padding-bottom: 0.875rem;
        border-bottom: 2px solid rgba(0,0,0,0.08);
        color: #1f2937;
        letter-spacing: -0.02em;
    }
    
    .conflict-item, .ambiguity-item, .suggestion-item {
        background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
        border-left: 5px solid #ef4444;
        padding: 1.25rem;
        margin: 1rem 0;
        border-radius: 0.75rem;
        color: #1f2937;
        font-size: 0.95rem;
        line-height: 1.7;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: all 0.3s ease;
        border-top: 1px solid rgba(0,0,0,0.05);
        border-right: 1px solid rgba(0,0,0,0.05);
        border-bottom: 1px solid rgba(0,0,0,0.05);
    }
    
    .conflict-item:hover, .ambiguity-item:hover, .suggestion-item:hover {
        transform: translateX(4px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .conflict-item strong, .ambiguity-item strong, .suggestion-item strong {
        color: #111827;
        font-weight: 600;
        display: inline-block;
        margin-top: 0.5rem;
    }
    
    .ambiguity-item {
        border-left-color: #f59e0b;
    }
    
    .suggestion-item {
        border-left-color: #10b981;
    }
    
    .empty-state {
        color: #6b7280;
        text-align: center;
        padding: 3rem 2rem;
        font-style: italic;
        font-size: 1rem;
        background: linear-gradient(135deg, #f9fafb 0%, #ffffff 100%);
        border-radius: 0.75rem;
        border: 2px dashed #d1d5db;
    }
    
    /* Metrics styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #667eea !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        color: #6b7280 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Improve scrollbar */
    .analysis-column::-webkit-scrollbar {
        width: 8px;
    }
    
    .analysis-column::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    .analysis-column::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 10px;
    }
    
    .analysis-column::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # ============================================
    # FILE UPLOAD SECTION - MOVED TO TOP (VERY VISIBLE)
    # ============================================
    st.markdown("---")
    
    # Big, visible section header
    st.markdown("## 📁 UPLOAD FILE ĐỂ PHÂN TÍCH")
    st.markdown("<p style='font-size: 1.1rem; color: #667eea; font-weight: 600; margin-bottom: 1.5rem;'>Chọn file .txt hoặc .docx chứa SRS/User Stories để AI phân tích</p>", unsafe_allow_html=True)
    
    # Very visible upload box
    st.markdown("""
    <div style='
        background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%);
        padding: 2.5rem;
        border-radius: 1.25rem;
        margin-bottom: 2rem;
        border: 3px dashed #667eea;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.2);
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
                with st.spinner("🤖 Đang phân tích file... Vui lòng đợi 10-30 giây"):
                    response = app.analyze_file(uploaded_file)
                    
                    if response and "error" not in response:
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
                        st.rerun()
                    else:
                        error_msg = response.get("error", "Unknown error") if response else "Failed to analyze file"
                        st.error(f"❌ Lỗi: {error_msg}")
            except Exception as e:
                st.error(f"❌ Lỗi khi phân tích file: {str(e)}")
            finally:
                st.session_state.processing = False
    else:
        st.info("👆 **Chọn file ở trên** để upload và phân tích document SRS/User Stories của bạn (.txt hoặc .docx)")
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    # ============================================
    # CHAT HISTORY DISPLAY
    # ============================================
    st.markdown("### 💬 Lịch sử chat")
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            role = message.get("role", "assistant")
            content = message.get("content", "")
            function_used = message.get("function_used", "unknown")
            
            # Format message display
            if role == "user":
                st.markdown(f"""
                <div class="user-message">
                    <strong>You:</strong><br>
                    {content}
                </div>
                """, unsafe_allow_html=True)
            else:
                # Check if this is an analysis result
                if function_used == "analyze_requirements" and isinstance(content, dict):
                    # Display formatted analysis results
                    display_analysis_results(content)
                else:
                    # Display regular message
                    st.markdown(f"""
                    <div class="assistant-message">
                        <strong>AI Assistant:</strong><br>
                        {content}
                    </div>
                    """, unsafe_allow_html=True)
    
    # ============================================
    # TEXT INPUT SECTION AT BOTTOM
    # ============================================
    st.markdown("---")
    st.markdown("### 💬 Or paste text below")
    st.markdown("<p style='color: #6b7280; margin-bottom: 1rem;'>Alternatively, paste your requirements text directly into the input field</p>", unsafe_allow_html=True)
    
    # Input section with centered styling
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        user_input = st.text_area(
            "Type your message here...",
            height=100,
            key="chat_input",
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
    if send_button and user_input.strip():
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().isoformat()
        })
        
        # Process message and get AI response
        st.session_state.processing = True
        
        try:
            with st.spinner("🤖 Thinking..."):
                # Get response from agent
                response = app.process_message(user_input, app.current_document)
                
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
                "content": f"❌ Error: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "function_used": "error"
            })
        finally:
            st.session_state.processing = False
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
    st.markdown(f"""
    <div class="assistant-message">
        <strong>AI Assistant:</strong><br>
        I've completed the analysis of your requirements document.
    </div>
    """, unsafe_allow_html=True)
    
    # Get data
    conflicts = results.get("conflicts", [])
    ambiguities = results.get("ambiguities", [])
    suggestions = results.get("suggestions", [])
    
    # Display summary stats with icons
    st.markdown("<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 1rem; margin: 1.5rem 0;'>", unsafe_allow_html=True)
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
                <div class="conflict-item">
                    <strong>Conflict {i}:</strong><br><br>
                    <strong>Req 1:</strong> {req1}<br><br>
                    <strong>Req 2:</strong> {req2}<br><br>
                    <strong>Issue:</strong> {desc}
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
                <div class="ambiguity-item">
                    <strong>Ambiguity {i}:</strong><br><br>
                    <strong>Requirement:</strong> {req}<br><br>
                    <strong>Issue:</strong> {issue}
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
                <div class="suggestion-item">
                    <strong>Suggestion {i}:</strong><br><br>
                    <strong>Original:</strong> {req}<br><br>
                    <strong>Improved:</strong> {new_version}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="empty-state">
                ✅ No suggestions at this time.
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)


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
    
    # Apply custom CSS for Claude-like styling
    st.markdown("""
    <style>
    /* Main container styling */
    .main > div {
        padding-top: 2rem;
        max-width: 900px;
        margin: 0 auto;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 0.5rem;
    }
    
    /* User messages (right-aligned) */
    .user-message {
        background-color: #1e3a8a;
        color: white;
        margin-left: 20%;
        border-radius: 1rem 1rem 0.25rem 1rem;
        padding: 1rem;
        text-align: left;
    }
    
    /* Assistant messages (left-aligned) */
    .assistant-message {
        background-color: #f8f9fa;
        color: #333;
        margin-right: 20%;
        border-radius: 1rem 1rem 1rem 0.25rem;
        padding: 1rem;
        border-left: 3px solid #4f46e5;
    }
    
    /* Chat input styling */
    .stTextInput > div > div > input {
        border-radius: 2rem;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
    }
    
    /* File upload button styling */
    .stFileUploader > div {
        border: 2px dashed #4f46e5;
        border-radius: 1rem;
        padding: 2rem;
        background-color: #f8f9fa;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div:hover {
        border-color: #6366f1;
        background-color: #f0f0ff;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 0.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Results formatting */
    .analysis-results {
        background-color: #f0f0f0;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-top: 1rem;
    }
    
    /* Column styling for 3-column layout */
    .analysis-column {
        background-color: #ffffff;
        border-radius: 0.75rem;
        padding: 1.25rem;
        margin: 0.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        min-height: 400px;
        height: 100%;
    }
    
    .conflict-column {
        border-top: 4px solid #ef4444;
    }
    
    .ambiguity-column {
        border-top: 4px solid #f59e0b;
    }
    
    .suggestion-column {
        border-top: 4px solid #10b981;
    }
    
    .column-header {
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #e5e7eb;
        color: #1f2937;
    }
    
    .conflict-item, .ambiguity-item, .suggestion-item {
        background-color: #f9fafb;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        margin: 0.75rem 0;
        border-radius: 0.5rem;
        color: #1f2937;
        font-size: 0.9rem;
        line-height: 1.6;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .conflict-item strong, .ambiguity-item strong, .suggestion-item strong {
        color: #111827;
        font-weight: 600;
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
        padding: 2rem;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Chat history display
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
    
    # Chat input at the bottom
    st.markdown("---")
    
    # File upload section with prominent button
    st.markdown("### 📁 Upload & Analyze File")
    
    # Create two columns for better layout
    col_upload, col_info = st.columns([2, 1])
    
    with col_upload:
        uploaded_file = st.file_uploader(
            "Choose a .txt or .docx file",
            type=['txt', 'docx'],
            help="Upload a .txt or .docx file containing SRS/User Stories",
            label_visibility="visible"
        )
    
    # Show upload button if file is selected
    if uploaded_file is not None:
        # Show file info
        file_details = {
            "Filename": uploaded_file.name,
            "FileType": uploaded_file.type,
            "FileSize": f"{uploaded_file.size / 1024:.2f} KB"
        }
        
        with col_info:
            st.markdown("<br>", unsafe_allow_html=True)  # Spacing
            st.info(f"📄 **{uploaded_file.name}**\n\nSize: {file_details['FileSize']}")
        
        # Large prominent analyze button
        st.markdown("<br>", unsafe_allow_html=True)
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            analyze_button = st.button(
                "🔍 Analyze File",
                type="primary",
                use_container_width=True,
                help="Click to analyze the uploaded file"
            )
        
        # Analyze file when button is clicked
        if analyze_button:
            # Add user message about file upload
            st.session_state.messages.append({
                "role": "user",
                "content": f"📁 Uploaded file: **{uploaded_file.name}** ({file_details['FileSize']})",
                "timestamp": datetime.now().isoformat()
            })
            
            st.session_state.processing = True
            try:
                with st.spinner("🤖 Analyzing file... This may take 10-30 seconds"):
                    # Analyze file via backend API
                    response = app.analyze_file(uploaded_file)
                    
                    if response and "error" not in response:
                        # Add successful response
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response,
                            "timestamp": datetime.now().isoformat(),
                            "function_used": "analyze_requirements"
                        })
                        app.current_document = response
                        
                        # Success message with stats
                        conflicts_count = len(response.get('conflicts', []))
                        ambiguities_count = len(response.get('ambiguities', []))
                        suggestions_count = len(response.get('suggestions', []))
                        st.success(
                            f"✅ **Analysis Complete!** "
                            f"Found {conflicts_count} conflict(s), "
                            f"{ambiguities_count} ambiguity(ies), "
                            f"{suggestions_count} suggestion(s)"
                        )
                    else:
                        # Add error response
                        error_msg = response.get("error", "Unknown error") if response else "Failed to analyze file"
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"❌ Error: {error_msg}",
                            "timestamp": datetime.now().isoformat(),
                            "function_used": "error"
                        })
                        st.error(f"❌ Error: {error_msg}")
            except Exception as e:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"❌ Error: {str(e)}",
                    "timestamp": datetime.now().isoformat(),
                    "function_used": "error"
                })
                st.error(f"❌ Error analyzing file: {str(e)}")
            finally:
                st.session_state.processing = False
                st.rerun()
    else:
        # Show placeholder when no file is uploaded
        st.info("👆 **Select a file above** to upload and analyze your SRS/User Stories document (.txt or .docx)")
    
    st.markdown("---")
    st.markdown("### 💬 Or paste text below")
    
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
    
    # Display summary stats
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Conflicts", len(conflicts), delta_color="inverse")
    with col2:
        st.metric("Ambiguities", len(ambiguities), delta_color="inverse")
    with col3:
        st.metric("Suggestions", len(suggestions), delta_color="normal")
    with col4:
        st.metric("Total Issues", len(conflicts) + len(ambiguities) + len(suggestions))
    
    st.markdown("---")
    
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


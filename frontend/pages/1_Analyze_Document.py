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
    
    /* Results formatting */
    .analysis-results {
        background-color: #f0f0f0;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-top: 1rem;
    }
    
    .conflict-item, .ambiguity-item, .suggestion-item {
        background-color: white;
        border-left: 3px solid #ef4444;
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-radius: 0.25rem;
    }
    
    .ambiguity-item {
        border-left-color: #f59e0b;
    }
    
    .suggestion-item {
        border-left-color: #10b981;
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
    Display formatted analysis results in the chat
    
    Args:
        results: Analysis results dictionary with conflicts, ambiguities, suggestions
    """
    st.markdown(f"""
    <div class="assistant-message">
        <strong>AI Assistant:</strong><br>
        I've completed the analysis of your requirements document.
    </div>
    """, unsafe_allow_html=True)
    
    # Display in an expandable results section
    with st.expander("📊 View Analysis Results", expanded=True):
        # Conflicts
        conflicts = results.get("conflicts", [])
        if conflicts:
            st.markdown("### 🧩 Conflicts Detected")
            for i, conflict in enumerate(conflicts, 1):
                req1 = conflict.get("req1", "")
                req2 = conflict.get("req2", "")
                desc = conflict.get("description", "")
                st.markdown(f"""
                <div class="conflict-item">
                    <strong>Conflict {i}:</strong><br>
                    <strong>Req 1:</strong> {req1}<br>
                    <strong>Req 2:</strong> {req2}<br>
                    <strong>Issue:</strong> {desc}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("✅ No conflicts detected!")
        
        # Ambiguities
        ambiguities = results.get("ambiguities", [])
        if ambiguities:
            st.markdown("### ❓ Ambiguities Detected")
            for i, ambiguity in enumerate(ambiguities, 1):
                req = ambiguity.get("req", "")
                issue = ambiguity.get("issue", "")
                st.markdown(f"""
                <div class="ambiguity-item">
                    <strong>Ambiguity {i}:</strong><br>
                    <strong>Requirement:</strong> {req}<br>
                    <strong>Issue:</strong> {issue}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("✅ No ambiguities detected!")
        
        # Suggestions
        suggestions = results.get("suggestions", [])
        if suggestions:
            st.markdown("### 💡 Improvement Suggestions")
            for i, suggestion in enumerate(suggestions, 1):
                req = suggestion.get("req", "")
                new_version = suggestion.get("new_version", "")
                st.markdown(f"""
                <div class="suggestion-item">
                    <strong>Suggestion {i}:</strong><br>
                    <strong>Original:</strong> {req}<br>
                    <strong>Improved:</strong> {new_version}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("✅ No suggestions at this time.")


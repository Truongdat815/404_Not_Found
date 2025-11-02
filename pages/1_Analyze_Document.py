"""
Analyze Document Page
Analyze SRS/User Stories for conflicts, ambiguities, and suggestions
"""

import streamlit as st
from core.agent import app


def show():
    """Display the Analyze Document page"""
    
    st.header("🧩 Analyze SRS/User Stories")
    st.markdown("Upload a document or paste text to analyze for conflicts, ambiguities, and suggestions.")
    
    # File uploader section
    with st.container():
        st.subheader("📤 Upload Document")
        uploaded_file = st.file_uploader(
            "Choose a .txt file",
            type=['txt'],
            help="Upload a text file containing your SRS or User Stories"
        )
    
    # Text input section
    with st.container():
        st.subheader("✍️ Or Paste Text Below")
        input_text = st.text_area(
            "SRS/User Stories Text",
            height=200,
            placeholder="Paste your SRS text or user stories here...",
            help="Enter or paste the requirements document text"
        )
    
    # Get text from file or textarea
    text_to_analyze = ""
    if uploaded_file is not None:
        text_to_analyze = uploaded_file.read().decode("utf-8")
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        # Pre-fill textarea with file content
        input_text = text_to_analyze
    elif input_text:
        text_to_analyze = input_text
    
    # Analyze button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        analyze_button = st.button(
            "🔍 Analyze Document",
            type="primary",
            use_container_width=True,
            disabled=not text_to_analyze.strip()
        )
    
    # Processing state
    if analyze_button and text_to_analyze.strip():
        with st.spinner("🤖 Analyzing your document... This may take a moment."):
            try:
                # Call the agent
                results = app.invoke(text_to_analyze)
                
                # Display metrics
                st.markdown("---")
                st.subheader("📊 Analysis Metrics")
                
                metrics = results.get("metrics", {})
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        label="Conflicts",
                        value=metrics.get("total_conflicts", 0),
                        delta=None
                    )
                
                with col2:
                    st.metric(
                        label="Ambiguities",
                        value=metrics.get("total_ambiguities", 0),
                        delta=None
                    )
                
                with col3:
                    st.metric(
                        label="Suggestions",
                        value=metrics.get("total_suggestions", 0),
                        delta=None
                    )
                
                with col4:
                    st.metric(
                        label="Text Length",
                        value=f"{metrics.get('text_length', 0):,}",
                        delta="characters"
                    )
                
                # Display results in tabs
                st.markdown("---")
                st.subheader("📋 Analysis Results")
                
                tab1, tab2, tab3 = st.tabs([
                    "🧩 Conflicts",
                    "❓ Ambiguities",
                    "💡 Suggestions"
                ])
                
                # Conflicts tab
                with tab1:
                    conflicts = results.get("conflicts", [])
                    if conflicts:
                        st.write("**Detected Conflicts:**")
                        for i, conflict in enumerate(conflicts, 1):
                            with st.container():
                                st.markdown(f"**{i}. {conflict}**")
                                st.markdown("---")
                    else:
                        st.info("✅ No conflicts detected!")
                
                # Ambiguities tab
                with tab2:
                    ambiguities = results.get("ambiguities", [])
                    if ambiguities:
                        st.write("**Detected Ambiguities:**")
                        for i, ambiguity in enumerate(ambiguities, 1):
                            with st.container():
                                st.markdown(f"**{i}. {ambiguity}**")
                                st.markdown("---")
                    else:
                        st.info("✅ No ambiguities detected!")
                
                # Suggestions tab
                with tab3:
                    suggestions = results.get("suggestions", [])
                    if suggestions:
                        st.write("**Improvement Suggestions:**")
                        for i, suggestion in enumerate(suggestions, 1):
                            with st.container():
                                st.markdown(f"**{i}. {suggestion}**")
                                st.markdown("---")
                    else:
                        st.info("✅ No suggestions at this time.")
                
                # Export results section
                st.markdown("---")
                st.subheader("💾 Export Results")
                
                export_col1, export_col2 = st.columns([1, 1])
                
                with export_col1:
                    # Export as JSON
                    import json
                    json_result = json.dumps(results, indent=2)
                    st.download_button(
                        label="📥 Download as JSON",
                        data=json_result,
                        file_name="analysis_results.json",
                        mime="application/json"
                    )
                
                with export_col2:
                    # Export as text
                    text_result = format_results_as_text(results)
                    st.download_button(
                        label="📄 Download as Text",
                        data=text_result,
                        file_name="analysis_results.txt",
                        mime="text/plain"
                    )
                
            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
                st.exception(e)


def format_results_as_text(results: dict) -> str:
    """Format results as readable text"""
    output = "=" * 60 + "\n"
    output += "REQUIREMENTS ANALYSIS RESULTS\n"
    output += "=" * 60 + "\n\n"
    
    # Metrics
    metrics = results.get("metrics", {})
    output += "METRICS:\n"
    output += f"  Total Conflicts: {metrics.get('total_conflicts', 0)}\n"
    output += f"  Total Ambiguities: {metrics.get('total_ambiguities', 0)}\n"
    output += f"  Total Suggestions: {metrics.get('total_suggestions', 0)}\n"
    output += f"  Text Length: {metrics.get('text_length', 0)} characters\n\n"
    
    # Conflicts
    conflicts = results.get("conflicts", [])
    output += "CONFLICTS:\n"
    output += "-" * 60 + "\n"
    if conflicts:
        for i, conflict in enumerate(conflicts, 1):
            output += f"{i}. {conflict}\n"
    else:
        output += "No conflicts detected.\n"
    output += "\n"
    
    # Ambiguities
    ambiguities = results.get("ambiguities", [])
    output += "AMBIGUITIES:\n"
    output += "-" * 60 + "\n"
    if ambiguities:
        for i, ambiguity in enumerate(ambiguities, 1):
            output += f"{i}. {ambiguity}\n"
    else:
        output += "No ambiguities detected.\n"
    output += "\n"
    
    # Suggestions
    suggestions = results.get("suggestions", [])
    output += "SUGGESTIONS:\n"
    output += "-" * 60 + "\n"
    if suggestions:
        for i, suggestion in enumerate(suggestions, 1):
            output += f"{i}. {suggestion}\n"
    else:
        output += "No suggestions at this time.\n"
    
    return output


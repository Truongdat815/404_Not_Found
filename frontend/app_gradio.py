"""
AI Requirements Assistant - Gradio Version
Chat interface với dark theme và tin nhắn AI màu xám
"""

import gradio as gr
from core.agent import app
from datetime import datetime
import json
import tempfile
import os


# Custom CSS cho dark theme và tin nhắn AI màu xám
custom_css = """
.dark-theme {
    background: #0f0f0f !important;
    color: #ffffff !important;
}

/* Tin nhắn AI (assistant) - màu XÁM */
.message.assistant {
    background: #555555 !important;
    background-color: #555555 !important;
    color: #ffffff !important;
    border-radius: 1.5rem 1.5rem 1.5rem 0.25rem !important;
    padding: 1rem 1.5rem !important;
    margin: 0.5rem 0 !important;
    border-left: 5px solid #818cf8 !important;
}

/* Tin nhắn user - màu tím */
.message.user {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: white !important;
    border-radius: 1.5rem 1.5rem 1.5rem 0.25rem !important;
    padding: 1rem 1.5rem !important;
    margin: 0.5rem 0 !important;
}

/* Force override cho chatbot messages */
.message {
    color: #ffffff !important;
}

.message * {
    color: #ffffff !important;
}

/* File upload area */
.upload-area {
    background: #1a1a1a !important;
    border: 3px dashed #818cf8 !important;
    border-radius: 1.25rem !important;
    padding: 2rem !important;
}

/* Buttons */
button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 1rem !important;
    padding: 0.75rem 2rem !important;
    font-weight: 700 !important;
}

/* Input fields */
input, textarea {
    background: #2d2d2d !important;
    color: #ffffff !important;
    border-color: #4a4a4a !important;
    border-radius: 1rem !important;
}
"""


def analyze_file(file, history):
    """Phân tích file được upload"""
    history = history or []
    
    if file is None:
        return history, "Vui lòng chọn file để phân tích!"
    
    try:
        # Gradio trả về file path, cần tạo file object giống Streamlit
        # Tạo một object giả lập Streamlit's UploadedFile
        class FileWrapper:
            def __init__(self, filepath):
                self.name = os.path.basename(filepath) if filepath else "unknown"
                self.filepath = filepath
                self.size = os.path.getsize(filepath) if os.path.exists(filepath) else 0
                self.type = "text/plain" if filepath.endswith('.txt') else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                # Cache file content
                self._content = None
            
            def getvalue(self):
                """Read file content as bytes"""
                if self._content is None:
                    with open(self.filepath, 'rb') as f:
                        self._content = f.read()
                return self._content
        
        file_obj = FileWrapper(file)
        
        # Phân tích bằng agent
        response = app.analyze_file(file_obj)
        
        if response and "error" not in response:
            conflicts = len(response.get('conflicts', []))
            ambiguities = len(response.get('ambiguities', []))
            suggestions = len(response.get('suggestions', []))
            
            app.current_document = response
            
            result_text = f"✅ **Phân tích hoàn tất!**\n\n"
            result_text += f"• Xung đột: {conflicts}\n"
            result_text += f"• Mơ hồ: {ambiguities}\n"
            result_text += f"• Đề xuất: {suggestions}\n\n"
            
            if conflicts or ambiguities or suggestions:
                result_text += "**Chi tiết:**\n"
                if conflicts:
                    result_text += f"\n**Xung đột ({conflicts}):**\n"
                    for i, c in enumerate(response.get('conflicts', [])[:3], 1):
                        result_text += f"{i}. {c.get('req1', '')} vs {c.get('req2', '')}\n"
                if ambiguities:
                    result_text += f"\n**Mơ hồ ({ambiguities}):**\n"
                    for i, a in enumerate(response.get('ambiguities', [])[:3], 1):
                        result_text += f"{i}. {a.get('req', '')}\n"
                if suggestions:
                    result_text += f"\n**Đề xuất ({suggestions}):**\n"
                    for i, s in enumerate(response.get('suggestions', [])[:3], 1):
                        result_text += f"{i}. {s.get('req', '')}\n"
            
            # Add to chat history
            new_history = history + [
                ["user", f"📁 Đã upload và phân tích file: {os.path.basename(file.name)}"],
                ["assistant", result_text]
            ]
            
            return new_history, result_text
        else:
            error_msg = response.get("error", "Unknown error") if response else "Failed to analyze"
            error_text = f"❌ Lỗi: {error_msg}"
            new_history = history + [["user", f"📁 Upload file: {os.path.basename(file.name) if file else 'N/A'}"], ["assistant", error_text]]
            return new_history, error_text
    except Exception as e:
        error_text = f"❌ Lỗi khi đọc file: {str(e)}"
        new_history = history + [["assistant", error_text]] if history else [[None, error_text]]
        return new_history, error_text


def chat_function(message, history):
    """Xử lý chat messages"""
    if not message or not message.strip():
        return history
    
    history = history or []
    
    # Add user message
    new_history = history + [["user", message]]
    
    # Xử lý tin nhắn
    try:
        response = app.process_message(message, app.current_document)
        
        if response and "error" not in response:
            if response.get("function_used") == "analyze_requirements":
                # Format analysis results
                conflicts = response.get('conflicts', [])
                ambiguities = response.get('ambiguities', [])
                suggestions = response.get('suggestions', [])
                
                app.current_document = response
                
                result_text = "✅ **Phân tích hoàn tất!**\n\n"
                result_text += f"Tìm thấy {len(conflicts)} xung đột, {len(ambiguities)} mơ hồ, {len(suggestions)} đề xuất.\n\n"
                
                if conflicts:
                    result_text += "**Xung đột:**\n"
                    for i, c in enumerate(conflicts[:5], 1):
                        result_text += f"{i}. {c.get('req1', '')} vs {c.get('req2', '')}\n"
                
                if ambiguities:
                    result_text += "\n**Mơ hồ:**\n"
                    for i, a in enumerate(ambiguities[:5], 1):
                        result_text += f"{i}. {a.get('req', '')}\n"
                
                if suggestions:
                    result_text += "\n**Đề xuất:**\n"
                    for i, s in enumerate(suggestions[:5], 1):
                        result_text += f"{i}. {s.get('req', '')}\n"
                
                new_history.append(["assistant", result_text])
            else:
                # Regular message
                ai_response = response.get("message", "Response received")
                new_history.append(["assistant", ai_response])
        else:
            error_msg = response.get("error", "Unknown error") if response else "Failed to process"
            new_history.append(["assistant", f"❌ Lỗi: {error_msg}"])
    except Exception as e:
        new_history.append(["assistant", f"❌ Lỗi: {str(e)}"])
    
    return new_history


def clear_chat(file, file_result):
    """Clear chat history"""
    app.current_document = None
    return [], None, "Chat đã được xóa!"


def export_chat(history):
    """Export chat history to JSON"""
    if not history or len(history) == 0:
        return None
    
    try:
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "messages": [
                {"role": role, "content": content} 
                for role, content in history
            ]
        }
        
        # Tạo file tạm
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8')
        json.dump(export_data, temp_file, indent=2, ensure_ascii=False)
        temp_file.close()
        
        return temp_file.name
    except Exception as e:
        return None


# Tạo Gradio interface
with gr.Blocks(theme=gr.themes.Soft(
    primary_hue="purple",
    neutral_hue="slate"
), css=custom_css) as demo:
    
    # Title
    gr.Markdown(
        """
        # 🤖 AI Requirements Assistant
        ## ✨ Powered by LangGraph and Google Gemini ✨
        """,
        elem_classes=["dark-theme"]
    )
    
    # File Upload Section
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown(
                """
                ## 📁 UPLOAD FILE ĐỂ PHÂN TÍCH
                **Chọn file .txt hoặc .docx chứa SRS/User Stories**
                """,
                elem_classes=["dark-theme"]
            )
            
            file_upload = gr.File(
                label="📎 CHỌN FILE",
                file_types=[".txt", ".docx"],
                type="filepath"
            )
            
            analyze_btn = gr.Button("🔍 PHÂN TÍCH FILE NÀY", variant="primary")
            
            file_result = gr.Textbox(
                label="Kết quả",
                interactive=False,
                lines=5
            )
    
    gr.Markdown("---")
    
    # Chat Interface
    gr.Markdown("### 💬 Chat với AI Assistant", elem_classes=["dark-theme"])
    
    chatbot = gr.Chatbot(
        label="Lịch sử chat",
        height=500,
        show_label=True,
        avatar_images=(None, None)  # Có thể thêm avatar sau
    )
    
    with gr.Row():
        msg_input = gr.Textbox(
            label="Nhập tin nhắn của bạn",
            placeholder="Paste document hoặc đặt câu hỏi...",
            lines=3,
            scale=4
        )
    
    with gr.Row():
        send_btn = gr.Button("Send", variant="primary", scale=1)
        clear_btn = gr.Button("Clear Chat", scale=1)
        export_btn = gr.Button("Export Chat", scale=1)
    
    export_file = gr.File(label="📥 Download Chat History", visible=True)
    
    # Event handlers
    analyze_btn.click(
        fn=analyze_file,
        inputs=[file_upload, chatbot],
        outputs=[chatbot, file_result]
    )
    
    def send_message(message, history):
        """Send message and clear input"""
        new_history = chat_function(message, history)
        return new_history, ""
    
    send_btn.click(
        fn=send_message,
        inputs=[msg_input, chatbot],
        outputs=[chatbot, msg_input]
    )
    
    msg_input.submit(
        fn=send_message,
        inputs=[msg_input, chatbot],
        outputs=[chatbot, msg_input]
    )
    
    clear_btn.click(
        fn=clear_chat,
        inputs=[file_upload, file_result],
        outputs=[chatbot, file_upload, file_result]
    )
    
    export_btn.click(
        fn=export_chat,
        inputs=[chatbot],
        outputs=[export_file]
    )
    
    # Welcome message khi load
    welcome_msg = [["assistant", "Hello! I'm your Requirements Engineering AI Assistant. I can help you:\n\n• Analyze full SRS/User Stories documents\n• Answer questions about requirements\n• Generate test cases\n• Explain detected conflicts\n\nJust paste a document or ask me a question!"]]
    
    demo.load(
        fn=lambda: welcome_msg,
        outputs=[chatbot]
    )


if __name__ == "__main__":
    import io
    import sys
    # Set UTF-8 encoding
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    print("=" * 60)
    print("Starting AI Requirements Assistant - Gradio Version")
    print("=" * 60)
    print(f"Backend URL: {app.api_base_url}")
    print(f"Backend API Docs: {app.api_base_url}/docs")
    print(f"App se chay tai: http://localhost:7860")
    print("=" * 60)
    
    # Test backend connection
    try:
        import requests
        health_response = requests.get(f"{app.api_base_url}/health", timeout=3)
        if health_response.status_code == 200:
            print("[OK] Backend connection: OK")
        else:
            print(f"[WARNING] Backend health check returned: {health_response.status_code}")
    except Exception as e:
        print(f"[WARNING] Cannot connect to backend: {e}")
        print(f"         Make sure backend is running at {app.api_base_url}")
    
    print("\nLuu y: Dam bao backend dang chay tai http://127.0.0.1:8000")
    print("       Backend API docs: http://127.0.0.1:8000/docs")
    print("\nNeu gap loi, kiem tra:")
    print("   1. Backend co dang chay khong? (http://127.0.0.1:8000/docs)")
    print("   2. Port 7860 co bi chiem khong?")
    print("   3. Da cai dat Gradio chua? (pip install gradio)")
    print("\n" + "=" * 60 + "\n")
    
    try:
        demo.launch(
            server_name="127.0.0.1",  # Chỉ localhost để tránh firewall issues
            server_port=7860,
            share=False,
            show_error=True,
            inbrowser=False,  # Không tự động mở để tránh lỗi
            show_api=False
        )
    except OSError as e:
        if "Address already in use" in str(e) or "port" in str(e).lower():
            print(f"\n[ERROR] Port 7860 da bi su dung!")
            print("Giai phap:")
            print("   1. Dong app khac dang dung port 7860")
            print("   2. Hoac doi port trong code:")
            print("      demo.launch(server_port=7861)  # Doi sang port khac")
        else:
            print(f"\n[ERROR] Loi khi khoi dong: {e}")
            import traceback
            traceback.print_exc()
    except Exception as e:
        print(f"\n[ERROR] Loi khong xac dinh: {e}")
        import traceback
        traceback.print_exc()
        print("\nHay chay test script: python test_gradio.py")


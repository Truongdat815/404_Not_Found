"""
Test script để kiểm tra Gradio có cài đặt đúng không
"""

import sys
import io

# Set UTF-8 encoding cho console output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

print("Kiem tra dependencies...")

try:
    import gradio as gr
    print(f"[OK] Gradio version: {gr.__version__}")
except ImportError:
    print("[ERROR] Gradio chua duoc cai dat!")
    print("Chay: pip install gradio>=4.0.0")
    sys.exit(1)

try:
    from core.agent import app
    print(f"[OK] Agent loaded. Backend URL: {app.api_base_url}")
except Exception as e:
    print(f"[ERROR] Loi khi load agent: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    import requests
    print(f"[OK] Requests OK")
except ImportError:
    print("[ERROR] Requests chua duoc cai dat!")
    sys.exit(1)

print("\n[OK] Tat ca dependencies OK!")
print("\nBay gio chay: python app_gradio.py")


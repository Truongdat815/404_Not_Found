"""
Script để chạy Gradio app
"""

import subprocess
import sys
import os

if __name__ == "__main__":
    # Đảm bảo đang ở đúng thư mục
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Chạy Gradio app
    subprocess.run([sys.executable, "app_gradio.py"])


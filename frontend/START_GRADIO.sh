#!/bin/bash

echo "===================================="
echo "Starting Gradio App"
echo "===================================="
echo ""

# Check if Gradio is installed
python3 -c "import gradio" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[ERROR] Gradio chua duoc cai dat!"
    echo "Dang cai dat Gradio..."
    pip install gradio>=4.0.0
    if [ $? -ne 0 ]; then
        echo "[ERROR] Khong the cai dat Gradio!"
        exit 1
    fi
fi

echo "[OK] Gradio da san sang"
echo ""
echo "Dang khoi dong app..."
echo "App se mo tai: http://localhost:7860"
echo ""
echo "Nhan Ctrl+C de dung app"
echo ""

python3 app_gradio.py


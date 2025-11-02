@echo off
chcp 65001 >nul
echo ====================================
echo Starting Gradio App
echo ====================================
echo.

REM Check if Gradio is installed
python -c "import gradio" 2>nul
if errorlevel 1 (
    echo [ERROR] Gradio chua duoc cai dat!
    echo Dang cai dat Gradio...
    pip install gradio>=4.0.0
    if errorlevel 1 (
        echo [ERROR] Khong the cai dat Gradio!
        pause
        exit /b 1
    )
)

echo [OK] Gradio da san sang
echo.
echo Dang khoi dong app...
echo App se mo tai: http://localhost:7860
echo.
echo Nhan Ctrl+C de dung app
echo.

python app_gradio.py

pause


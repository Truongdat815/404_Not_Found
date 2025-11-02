# 🚀 Quick Start Guide - AI Requirements Assistant

## ✅ Setup Complete!

Tất cả dependencies và configuration đã được setup xong. Bạn có thể chạy ứng dụng ngay!

## 🎯 Chạy Frontend (Streamlit Chat Interface)

### Cách 1: Từ root directory

```bash
streamlit run frontend/app.py
```

### Cách 2: Từ thư mục frontend

```bash
cd frontend
streamlit run app.py
```

Sau đó mở browser tại: **http://localhost:8501**

## 🔧 Chạy Backend API (Optional)

Nếu muốn chạy backend API riêng (frontend vẫn hoạt động được mà không cần backend vì đã import trực tiếp):

```bash
cd backend
.\venv\Scripts\Activate.ps1  # Kích hoạt virtual environment (nếu có)
uvicorn main:app --reload
```

API sẽ chạy tại: **http://localhost:8000**

## 📋 Cấu trúc đã hoàn thiện

### Frontend
- ✅ `frontend/app.py` - Main Streamlit app
- ✅ `frontend/pages/1_Analyze_Document.py` - Chat interface
- ✅ `frontend/core/agent.py` - Multi-function AI agent
- ✅ `requirements.txt` - Đã có streamlit và tất cả dependencies

### Backend
- ✅ `backend/main.py` - FastAPI server
- ✅ `backend/app/agents/langgraph_agent.py` - LangGraph agent
- ✅ `backend/app/agents/prompts/` - 4 prompt files (parse, conflict, ambiguity, improve)
- ✅ `backend/app/api/router.py` - API endpoints
- ✅ `backend/requirements.txt` - Dependencies

### Configuration
- ✅ `.env` - GEMINI_API_KEY (ở cả root và backend)
- ✅ Tất cả dependencies đã được cài đặt

## 🎨 Tính năng

### Chat Interface
- Claude-like UI với message bubbles
- Text-only input
- Multiple agent functions:
  - Analyze requirements documents
  - Answer questions
  - Generate test cases
  - Explain conflicts

### Agent Functions
1. **analyze_requirements**: Phân tích full SRS document
2. **answer_question**: Trả lời câu hỏi về requirements
3. **generate_test_cases**: Tạo test cases
4. **explain_conflicts**: Giải thích conflicts chi tiết

## 📝 Sử dụng

1. Paste một requirements document vào chat
2. AI sẽ tự động detect và analyze
3. Có thể hỏi thêm câu hỏi sau khi analyze
4. Export chat history hoặc clear chat

## 🐛 Troubleshooting

### Agent chạy mock mode?
- Kiểm tra file `.env` có GEMINI_API_KEY
- Chạy: `python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('GEMINI_API_KEY'))"`

### ModuleNotFoundError?
- Chạy: `pip install -r requirements.txt`

### Backend không khởi động?
- Kiểm tra file `.env` trong `backend/`
- Activate virtual environment: `backend\venv\Scripts\Activate.ps1`

## 🎉 Done!

Chúc bạn hackathon vui vẻ! 🚀


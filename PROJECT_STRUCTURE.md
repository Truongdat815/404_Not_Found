git# Project Structure

## Cấu trúc thư mục

```
D:\404_Not_Found\
├── frontend/                    # Streamlit Frontend Application
│   ├── app.py                   # Main Streamlit app
│   ├── pages/
│   │   └── 1_Analyze_Document.py
│   ├── core/
│   │   └── agent.py             # Agent module (app.invoke())
│   └── README.md
│
├── backend/                     # FastAPI Backend Application
│   ├── app/
│   │   ├── agents/
│   │   │   └── langgraph_agent.py
│   │   ├── api/
│   │   │   ├── router.py
│   │   │   └── schema.py
│   │   ├── services/
│   │   │   └── analyzer.py
│   │   └── utils/
│   │       └── file_handler.py
│   ├── main.py                  # FastAPI entry point
│   └── requirements.txt
│
├── docs/                        # Documentation
├── requirements.txt              # Root Python dependencies
├── README.md
└── STREAMLIT_SETUP.md
```

## Vị trí thư mục

- ✅ `frontend/` và `backend/` ở **cùng cấp** trong root project
- ✅ Không có `frontend/` trong `backend/`
- ✅ Mỗi module độc lập và có thể chạy riêng biệt

## Chạy ứng dụng

### Frontend (Streamlit)
```bash
python -m streamlit run frontend/app.py
```

### Backend (FastAPI)
```bash
cd backend
uvicorn main:app --reload
```


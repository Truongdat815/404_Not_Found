# 🚀 How to Start Frontend

## Quick Start

```bash
# 1. Install dependencies (if not already done)
pip install streamlit requests python-dotenv

# 2. Run frontend
streamlit run frontend/app.py
```

## Alternative (from frontend directory)

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

## Troubleshooting

### Error: ModuleNotFoundError: No module named 'dotenv'

**Solution:**
```bash
pip install python-dotenv requests
```

### Error: Port 8501 already in use

**Solution:**
```bash
streamlit run frontend/app.py --server.port 8502
```

### Frontend can't connect to backend

**Check:**
1. Backend is running: http://127.0.0.1:8000/health
2. Backend is healthy

**Solution:**
```bash
# In separate terminal, start backend first:
cd backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload
```

---

**Default URLs:**
- Frontend: http://localhost:8501
- Backend: http://127.0.0.1:8000


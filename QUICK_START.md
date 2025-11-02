# 🚀 Quick Start Guide - Run Full Stack

## Prerequisites

- Python 3.10+
- SQL Server running (local)
- Gemini API Key configured

## 📋 Step 1: Start Backend

```bash
cd backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Verify:** Open http://127.0.0.1:8000/health

## 📋 Step 2: Start Frontend

**In a NEW terminal:**

```bash
# From project root
pip install -r frontend/requirements.txt
streamlit run frontend/app.py
```

**Or:**

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

**Frontend will run on:** http://localhost:8501

## ✅ Verify Connection

1. **Backend Health:** http://127.0.0.1:8000/health
2. **Frontend:** http://localhost:8501
3. **API Docs:** http://127.0.0.1:8000/docs

## 🎯 Test Full Flow

1. Open http://localhost:8501 in browser
2. Paste requirements text:
   ```
   REQ1: The system shall display user information.
   REQ2: The system shall not display user information.
   ```
3. Click "Send"
4. Wait for analysis (10-30 seconds)
5. See results: Conflicts, Ambiguities, Suggestions
6. Results are automatically saved to database!

## 🔧 Troubleshooting

### Frontend can't connect to backend

**Check:**
- Backend is running on port 8000
- No firewall blocking
- CORS is configured (already done)

**Solution:**
```bash
# Test backend manually
curl http://127.0.0.1:8000/health
# Or in PowerShell:
Invoke-RestMethod -Uri http://127.0.0.1:8000/health
```

### Frontend shows mock data

**Cause:** Backend not reachable

**Solution:**
1. Check backend is running
2. Check API_BASE_URL in frontend/.env (optional)
3. Default: http://127.0.0.1:8000

### Port 8501 already in use

**Solution:**
```bash
# Use different port
streamlit run frontend/app.py --server.port 8502
```

## 📊 Architecture

```
Frontend (Streamlit)      Backend (FastAPI)
localhost:8501    →      127.0.0.1:8000
   │                        │
   │  HTTP API Calls        │
   ├──> POST /api/analyze   │
   ├──> GET /api/history    │
   └──> GET /api/export/... │
                              │
                              ├──> LangGraph Agent (Gemini 2.5 Flash)
                              ├──> SQL Server Database
                              └──> Export Services
```

---

**Happy Coding! 🎉**

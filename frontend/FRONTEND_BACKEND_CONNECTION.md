# 🔗 Frontend-Backend Connection Guide

## ✅ Đã cập nhật

Frontend bây giờ kết nối với backend qua **HTTP API** thay vì import trực tiếp Python module.

## 📋 Thay đổi

### `frontend/core/agent.py`

**Trước:**
- Import trực tiếp `RequirementsAnalysisAgent` từ backend
- Gọi `agent.analyze()` trong cùng process

**Sau:**
- Sử dụng `requests` library để gọi HTTP API
- Kết nối đến `http://127.0.0.1:8000/api/analyze`
- Store `analysis_id` để có thể export/history sau

## 🚀 Cách sử dụng

### 1. Đảm bảo Backend đang chạy

```bash
cd backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 2. Chạy Frontend

```bash
cd frontend
streamlit run app.py
```

Hoặc từ root:
```bash
streamlit run frontend/app.py
```

### 3. Cấu hình API URL (Optional)

Tạo file `frontend/.env`:
```
API_BASE_URL=http://127.0.0.1:8000
```

## 🔧 API Endpoints được sử dụng

1. **POST /api/analyze** - Phân tích text input
2. **GET /api/history** - Lấy lịch sử phân tích (method mới)
3. **GET /api/export/json/{id}** - Export JSON (method mới)
4. **GET /api/export/docx/{id}** - Export DOCX (method mới)

## ✨ Tính năng mới

### 1. Analysis ID Tracking
- Frontend lưu `analysis_id` sau mỗi lần analyze
- Có thể dùng để export hoặc xem history

### 2. History Access
- Method `get_history()` để lấy lịch sử từ backend
- Có thể hiển thị trong UI sau

### 3. Export Functionality
- Method `export_analysis()` để export JSON/DOCX
- Tải file trực tiếp từ backend

### 4. Error Handling
- Connection errors được handle gracefully
- Timeout errors được thông báo rõ ràng
- Fallback to mock data nếu backend không available

## 🐛 Troubleshooting

### Lỗi: "Cannot connect to backend API"

**Giải pháp:**
1. Kiểm tra backend đang chạy: `http://127.0.0.1:8000/health`
2. Kiểm tra CORS config trong `backend/main.py`
3. Đảm bảo port 8000 không bị block

### Lỗi: "Request timeout"

**Giải pháp:**
- Text quá dài, analysis mất thời gian
- Có thể tăng timeout hoặc chia nhỏ text

### Frontend dùng mock data

**Nguyên nhân:**
- Backend không available
- API URL không đúng
- Network issues

## 📝 Next Steps

Có thể thêm vào frontend UI:
1. **History Page** - Hiển thị lịch sử phân tích
2. **Export Buttons** - Export JSON/DOCX cho mỗi analysis
3. **Analysis ID Display** - Hiển thị ID để reference
4. **File Upload** - Upload file qua `/api/analyze/file`

---

**Status:** ✅ Frontend-Backend connection hoàn tất!


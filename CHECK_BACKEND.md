# 🔍 Kiểm tra và sửa lỗi Backend

## ⚠️ Vấn đề: File upload không trả kết quả, load lâu

### Bước 1: Kiểm tra Backend có đang chạy không

Mở browser và vào:
```
http://127.0.0.1:8000/health
```

**Nếu thấy JSON response** → Backend đang chạy ✅
**Nếu không kết nối được** → Backend không chạy ❌

### Bước 2: Khởi động Backend (nếu chưa chạy)

```powershell
# Terminal 1 - Backend
cd backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Đợi thấy message:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Bước 3: Kiểm tra CORS và API endpoints

Backend phải có:
- `POST /api/analyze/file` - để upload và phân tích file
- `GET /health` - để check health

### Bước 4: Test API trực tiếp

```powershell
# Test health
Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -UseBasicParsing

# Test analyze endpoint (cần file)
# Dùng Postman hoặc curl để test
```

## 🔧 Các lỗi thường gặp

### Lỗi: "Cannot connect to backend API"
**Nguyên nhân:** Backend không chạy hoặc sai port
**Giải pháp:** 
1. Kiểm tra backend có chạy không
2. Kiểm tra port 8000 có bị block không
3. Kiểm tra URL trong `.env`: `API_BASE_URL=http://127.0.0.1:8000`

### Lỗi: "Request timeout"
**Nguyên nhân:** File quá lớn hoặc AI analysis mất quá nhiều thời gian
**Giải pháp:**
- Đợi lâu hơn (có thể mất 2-3 phút)
- Thử file nhỏ hơn
- Kiểm tra backend logs xem có lỗi không

### Lỗi: "429 Too Many Requests"
**Nguyên nhân:** Gửi quá nhiều request đến Gemini API
**Giải pháp:**
- Đợi một chút rồi thử lại
- Kiểm tra quota Gemini API

### Lỗi: F12 Console có nhiều lỗi
**Các lỗi không liên quan đến code:**
- `429` từ Sentry → Có thể ignore
- `Content script errors` → Browser extension issues → Có thể ignore

**Các lỗi cần chú ý:**
- `Failed to fetch` → Backend không chạy
- `CORS error` → Cần check CORS config trong backend
- `Network error` → Backend không accessible

## 📋 Checklist Debug

- [ ] Backend đang chạy (`http://127.0.0.1:8000/health`)
- [ ] Frontend có thể kết nối backend
- [ ] File upload endpoint hoạt động (`/api/analyze/file`)
- [ ] Gemini API key đúng trong `.env`
- [ ] SQL Server đang chạy (nếu cần lưu history)
- [ ] Không có lỗi trong backend logs

## 🚀 Quick Fix

1. **Restart Backend:**
   ```powershell
   # Stop: Ctrl+C
   # Start lại:
   cd backend
   .\venv\Scripts\Activate.ps1
   uvicorn main:app --reload
   ```

2. **Restart Frontend:**
   ```powershell
   # Stop: Ctrl+C
   # Start lại:
   streamlit run frontend/app.py
   ```

3. **Clear Browser Cache:**
   - Ctrl+Shift+Delete
   - Chọn "Cached images and files"

---

**Sau khi fix, thử upload file lại và xem error message cụ thể!**


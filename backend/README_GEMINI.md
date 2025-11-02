# 🚀 Gemini API Integration - Quick Start

## ✅ Đã hoàn thành setup:

1. ✅ Cài đặt `google-generativeai` package
2. ✅ Tạo file `.env` với GEMINI_API_KEY
3. ✅ Implement analyzer service với Gemini API
4. ✅ Tạo API endpoint `/api/analyze`
5. ✅ Cấu hình CORS cho frontend

## 📋 Các file đã tạo/cập nhật:

```
backend/
├── .env                           ✅ API Key (không commit)
├── requirements.txt               ✅ Đã thêm google-generativeai
├── main.py                       ✅ Đã include router
├── app/
│   ├── api/
│   │   ├── router.py             ✅ Endpoint /api/analyze
│   │   └── schema.py             ✅ Request/Response models
│   └── services/
│       └── analyzer.py            ✅ Gemini API integration
└── test_api.py                   ✅ Script test API
```

## 🎯 Cách sử dụng:

### 1. Khởi động server:

```bash
cd backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload
```

### 2. Test API:

**Option A: Dùng Swagger UI (Khuyến nghị)**
- Mở trình duyệt: http://127.0.0.1:8000/docs
- Tìm endpoint `POST /api/analyze`
- Click "Try it out"
- Nhập text vào field `text`
- Click "Execute"

**Option B: Dùng script test**
```bash
# Trong terminal mới (server đang chạy)
cd backend
.\venv\Scripts\Activate.ps1
pip install requests  # Nếu chưa có
python test_api.py
```

**Option C: Dùng curl/PowerShell**
```powershell
$body = @{
    text = "User must login. User should not login."
    model = "gemini-1.5-pro"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/analyze" `
  -Method POST -Body $body -ContentType "application/json"
```

### 3. Request format:

```json
{
  "text": "Your SRS or User Stories text here...",
  "model": "gemini-1.5-pro"  // optional
}
```

### 4. Response format:

```json
{
  "conflicts": [
    {
      "req1": "requirement 1 text",
      "req2": "requirement 2 text",
      "description": "explanation of conflict"
    }
  ],
  "ambiguities": [
    {
      "req": "ambiguous requirement",
      "issue": "why it's ambiguous"
    }
  ],
  "suggestions": [
    {
      "req": "original requirement",
      "new_version": "improved version"
    }
  ]
}
```

## 🔧 Models có sẵn:

- `gemini-1.5-pro` (default) - Khuyến nghị cho phân tích phức tạp
- `gemini-1.5-flash` - Nhanh hơn, phù hợp cho test nhanh
- `gemini-pro` - Legacy model

## ⚠️ Troubleshooting:

### Lỗi: "API key not configured"
- Kiểm tra file `.env` có tồn tại không
- Kiểm tra GEMINI_API_KEY có đúng format không
- Restart server sau khi thay đổi .env

### Lỗi: "Cannot connect to server"
- Đảm bảo server đang chạy: `uvicorn main:app --reload`
- Kiểm tra port 8000 có bị chiếm không

### Lỗi: "Invalid API key" hoặc "Quota exceeded"
- Kiểm tra API key trong Google Cloud Console
- Verify API key có quyền sử dụng Gemini API
- Kiểm tra quota còn lại

### Response không có kết quả
- Thử với text dài hơn, rõ ràng hơn
- Kiểm tra prompt trong `analyzer.py` có đúng format không

## 🔒 Security:

- ✅ File `.env` đã được thêm vào `.gitignore`
- ✅ KHÔNG commit API key lên GitHub
- ✅ API key chỉ tồn tại local

## 📊 Health Check:

Kiểm tra server và API key:
```
GET http://127.0.0.1:8000/health
```

Response:
```json
{
  "status": "healthy",
  "gemini_api_key_configured": true
}
```

---

## 🎉 Ready to use!

Server đã sẵn sàng để frontend gọi API. Bạn có thể bắt đầu implement UI để upload text và hiển thị kết quả!


# ✅ Gemini API Setup Complete!

## Đã hoàn thành:

✅ **Cài đặt google-generativeai package**
   - Package đã được cài đặt thành công trong venv

✅ **Tạo file cấu hình**
   - `app/api/schema.py` - Request/Response models
   - `app/services/analyzer.py` - Gemini API integration
   - `app/api/router.py` - API endpoint `/api/analyze`
   - `main.py` - Đã được cập nhật với router

✅ **File .env**
   - Đã được tạo với GEMINI_API_KEY
   - File này không được commit (đã có trong .gitignore)

## Cách sử dụng:

### 1. Kiểm tra file .env:
Đảm bảo file `backend/.env` tồn tại với nội dung:
```
GEMINI_API_KEY=AIzaSyBIFUpy2dRYpbpNDtMi_v144PIU49CIyG0
```

### 2. Chạy server:
```bash
cd backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload
```

### 3. Test API:

**Mở Swagger UI:** http://127.0.0.1:8000/docs

**Hoặc test bằng curl:**
```bash
curl -X POST "http://127.0.0.1:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "User should login. User should not login.",
    "model": "gemini-1.5-pro"
  }'
```

**Hoặc test với PowerShell:**
```powershell
$body = @{
    text = "User should login. User should not login."
    model = "gemini-1.5-pro"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/analyze" -Method POST -Body $body -ContentType "application/json"
```

## Endpoint `/api/analyze`:

**Request:**
```json
{
  "text": "Your SRS or User Stories text here",
  "model": "gemini-1.5-pro"  // optional, default: gemini-1.5-pro
}
```

**Response:**
```json
{
  "conflicts": [
    {
      "req1": "requirement 1",
      "req2": "requirement 2",
      "description": "explanation"
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
  ],
  "raw_response": null
}
```

## Các model Gemini có sẵn:

- `gemini-1.5-pro` (khuyến nghị - default)
- `gemini-1.5-flash` (nhanh hơn, nhẹ hơn)
- `gemini-pro` (legacy)

## Lưu ý:

1. **API Key bảo mật:**
   - File `.env` đã được thêm vào `.gitignore`
   - KHÔNG commit API key lên GitHub

2. **Quota và giới hạn:**
   - Kiểm tra quota trong Google Cloud Console
   - Monitor usage để tránh hết quota giữa chừng hackathon

3. **Error handling:**
   - API sẽ trả về error nếu API key không hợp lệ
   - Kiểm tra `/health` endpoint để xem API key có được cấu hình chưa

4. **JSON parsing:**
   - Analyzer tự động parse JSON từ response
   - Nếu Gemini trả về markdown code block, sẽ tự động extract JSON

---

🎉 **Gemini API đã sẵn sàng sử dụng!**


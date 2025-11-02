# 🧪 Hướng dẫn Test Frontend

## 📋 Cách Test

### Option 1: Test với Text (Paste)

1. **Mở frontend:** http://localhost:8501
2. **Copy nội dung từ file TEST_REQUIREMENTS_1.txt** (bên dưới)
3. **Paste vào text area** (phần "💬 Or paste text below")
4. **Click button "Send"** (màu đỏ)
5. **Đợi 10-30 giây** - AI đang phân tích
6. **Xem kết quả:**
   - Conflicts (mâu thuẫn)
   - Ambiguities (mơ hồ)
   - Suggestions (đề xuất cải thiện)

### Option 2: Test với File Upload

1. **Mở frontend:** http://localhost:8501
2. **Scroll lên trên**, tìm section **"📁 Upload File (.txt or .docx)"**
3. **Click "Browse files"** hoặc drag & drop
4. **Chọn file:** TEST_REQUIREMENTS_1.txt (hoặc 2, 3)
5. **File info sẽ hiện** (tên, size)
6. **Click button "🔍 Analyze File"**
7. **Đợi 10-30 giây**
8. **Xem kết quả** (tương tự như paste text)

---

## 📄 Nội dung Test 1: Login & Privacy Conflicts

```
REQ1: The system shall allow users to login with email and password.
REQ2: The system shall not require users to login for basic access.
REQ3: Users must provide their email address during registration.
REQ4: Users can skip email verification if they want to proceed faster.
REQ5: The system should display user information on the dashboard.
REQ6: The system shall protect user privacy and not display personal information.
REQ7: The application should respond quickly to user requests.
REQ8: The system must support all modern web browsers and mobile devices.
REQ9: All user data must be encrypted for security.
REQ10: Users should be able to access their data easily without complex security checks.
```

**Expected Results:**
- **Conflicts:** REQ1 vs REQ2, REQ3 vs REQ4, REQ5 vs REQ6, REQ9 vs REQ10
- **Ambiguities:** REQ7 ("quickly"), REQ8 ("modern browsers")
- **Suggestions:** Cải thiện các requirement mơ hồ

---

## 📄 Nội dung Test 2: Payment System

```
REQ1: The payment system shall process transactions within 5 seconds.
REQ2: Payment processing should be fast and efficient.
REQ3: Users can make payments using credit cards only.
REQ4: The system must accept multiple payment methods including PayPal, bank transfer, and cryptocurrency.
REQ5: All transactions must be logged for audit purposes.
REQ6: Transaction logs should not contain sensitive payment information.
REQ7: The system shall provide real-time transaction status updates.
REQ8: Transaction status updates may be delayed by up to 24 hours for batch processing.
REQ9: The application must be user-friendly.
REQ10: The system should achieve 95% user satisfaction rating in usability testing.
```

**Expected Results:**
- **Conflicts:** REQ1 vs REQ8, REQ3 vs REQ4, REQ5 vs REQ6, REQ7 vs REQ8
- **Ambiguities:** REQ2 ("fast"), REQ9 ("user-friendly")
- **Suggestions:** Cải thiện các requirement mơ hồ

---

## 📄 Nội dung Test 3: Admin & Security

```
REQ1: The admin dashboard shall display all user accounts.
REQ2: Admin users can view user accounts only with proper authorization.
REQ3: The system shall send email notifications immediately after user registration.
REQ4: Email notifications may be sent within 24 hours of registration.
REQ5: User passwords must be at least 8 characters long.
REQ6: The system should encourage users to create strong passwords.
REQ7: All API endpoints must require authentication.
REQ8: The public documentation API endpoint is accessible without authentication.
REQ9: Reports should be generated on-demand.
REQ10: Daily reports are automatically generated at midnight.
```

**Expected Results:**
- **Conflicts:** REQ1 vs REQ2, REQ3 vs REQ4, REQ7 vs REQ8, REQ9 vs REQ10
- **Ambiguities:** REQ6 ("strong passwords" - không định nghĩa)
- **Suggestions:** Cải thiện các requirement mơ hồ

---

## ✅ Checklist Test

- [ ] Frontend load được (http://localhost:8501)
- [ ] Paste text và click Send → có kết quả
- [ ] Upload file .txt → có kết quả
- [ ] Upload file .docx → có kết quả
- [ ] Kết quả hiển thị Conflicts, Ambiguities, Suggestions
- [ ] Analysis ID được hiển thị (để export sau)
- [ ] Kết quả được lưu vào database (check `/api/history`)

---

## 🐛 Troubleshooting

### Không có kết quả sau khi Send

**Kiểm tra:**
1. Backend có đang chạy? http://127.0.0.1:8000/health
2. Xem console browser có lỗi không (F12)
3. Đợi đủ 30 giây (AI analysis mất thời gian)

### Error: "Cannot connect to backend"

**Solution:**
1. Kiểm tra backend: `uvicorn main:app --reload` (trong backend/)
2. Test API: http://127.0.0.1:8000/docs

### File upload không hoạt động

**Check:**
1. File size không quá lớn (< 10MB)
2. File format đúng (.txt hoặc .docx)
3. Backend endpoint `/api/analyze/file` hoạt động

---

**Happy Testing! 🎉**


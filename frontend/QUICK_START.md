# 🚀 QUICK START - Gradio App

## Bước 1: Cài đặt Gradio (nếu chưa có)

```bash
cd frontend
pip install gradio>=4.0.0
```

## Bước 2: Đảm bảo Backend đang chạy

Backend phải chạy tại: **http://127.0.0.1:8000**

Kiểm tra: Mở browser và vào **http://127.0.0.1:8000/docs**

Nếu thấy Swagger UI thì backend đã chạy ✅

## Bước 3: Chạy Gradio App

### Windows:
```bash
cd frontend
START_GRADIO.bat
```

Hoặc:
```bash
python app_gradio.py
```

### Linux/Mac:
```bash
cd frontend
python3 app_gradio.py
```

## Bước 4: Mở app

App sẽ tự động mở tại: **http://localhost:7860**

Nếu không tự mở, mở browser và vào: **http://localhost:7860**

## 🎨 Giao diện

- ✅ Dark theme (nền đen)
- ✅ Tin nhắn AI màu XÁM (#555555) với chữ trắng
- ✅ Tin nhắn user màu TÍM gradient
- ✅ File upload
- ✅ Chat interface

## ⚠️ Troubleshooting

### Lỗi: Port 7860 đã bị sử dụng

Giải pháp:
1. Đóng app khác đang dùng port 7860
2. Hoặc đổi port trong `app_gradio.py`:
   ```python
   demo.launch(server_port=7861)  # Đổi sang port khác
   ```

### Lỗi: Backend không kết nối được

Giải pháp:
1. Kiểm tra backend đang chạy: http://127.0.0.1:8000/docs
2. Kiểm tra URL trong `.env` file (nếu có)
3. Đảm bảo backend và frontend cùng network

### Lỗi: ModuleNotFoundError: No module named 'gradio'

Giải pháp:
```bash
pip install gradio>=4.0.0
```


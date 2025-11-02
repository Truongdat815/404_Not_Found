# 🚀 Chạy Gradio App

## Cách nhanh nhất (Windows)

**Double-click file:** `START_GRADIO.bat`

Script sẽ tự động:
- Kiểm tra và cài đặt Gradio nếu thiếu
- Chạy app
- Mở tại http://localhost:7860

## Cài đặt thủ công

```bash
cd frontend
pip install gradio>=4.0.0
```

Hoặc cài tất cả dependencies:

```bash
cd frontend
pip install -r requirements.txt
```

## Chạy app

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
chmod +x START_GRADIO.sh
./START_GRADIO.sh
```

Hoặc:
```bash
python3 app_gradio.py
```

App sẽ chạy tại: **http://localhost:7860**

## Kiểm tra trước khi chạy

```bash
python test_gradio.py
```

Script này sẽ kiểm tra:
- ✅ Gradio đã cài đặt chưa
- ✅ Agent có load được không
- ✅ Backend URL có đúng không

## Tính năng

✅ **Dark theme** - Giao diện màu tối đẹp mắt  
✅ **Tin nhắn AI màu xám** (#555555) - Dễ đọc  
✅ **Tin nhắn user màu tím** - Gradient đẹp  
✅ **File upload** - Upload .txt hoặc .docx  
✅ **Chat interface** - Chat real-time với AI  
✅ **Export chat** - Xuất lịch sử chat ra JSON  

## So sánh với Streamlit

| Tính năng | Streamlit | Gradio |
|-----------|-----------|--------|
| Custom CSS | Khó override | Dễ dàng ✅ |
| Dark theme | Phức tạp | Đơn giản ✅ |
| Tin nhắn màu xám | Khó | Dễ ✅ |
| Performance | Ổn | Tốt hơn ✅ |
| File upload | Ổn | Tốt ✅ |

## Cấu trúc

- `app_gradio.py` - File chính chứa Gradio app
- `core/agent.py` - Backend logic (giữ nguyên)
- `requirements.txt` - Đã cập nhật với Gradio

## Lưu ý

- Đảm bảo backend đang chạy tại `http://127.0.0.1:8000`
- Nếu cần đổi port, sửa trong `app_gradio.py`:
  ```python
  demo.launch(server_port=7860)  # Đổi port ở đây
  ```


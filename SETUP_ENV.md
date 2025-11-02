# Environment Setup Guide

## Tạo file .env

Để frontend và backend hoạt động, bạn cần tạo file `.env` ở **root của project** (cùng cấp với README.md).

### Cách 1: Tạo thủ công

1. Tạo file `.env` trong thư mục `D:\404_Not_Found\`
2. Thêm nội dung sau:

```env
GEMINI_API_KEY=AIzaSyBIFUpy2dRYpbpNDtMi_v144PIU49CIyG0
```

### Cách 2: Dùng Terminal

**Windows (PowerShell):**
```powershell
# Từ root directory
echo "GEMINI_API_KEY=AIzaSyBIFUpy2dRYpbpNDtMi_v144PIU49CIyG0" > .env
```

**Linux/Mac:**
```bash
echo "GEMINI_API_KEY=AIzaSyBIFUpy2dRYpbpNDtMi_v144PIU49CIyG0" > .env
```

## Cấu trúc file .env

```env
# Gemini API Key
GEMINI_API_KEY=AIzaSyBIFUpy2dRYpbpNDtMi_v144PIU49CIyG0
```

## Kiểm tra setup

Sau khi tạo file `.env`, test xem agent có load được API key không:

```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('GEMINI_API_KEY:', os.getenv('GEMINI_API_KEY'))"
```

Nếu in ra key thì đã thành công! Nếu in ra `None` thì check lại đường dẫn file `.env`.

## Lưu ý

- File `.env` đã được thêm vào `.gitignore` nên sẽ KHÔNG được commit lên Git
- Không chia sẻ API key này công khai
- Nếu API key hết hạn hoặc bị revoke, tạo key mới trong Google Cloud Console


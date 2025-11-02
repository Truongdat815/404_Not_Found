# Frontend - Streamlit Application

## Cấu trúc

```
frontend/
├── app.py                  # Main Streamlit application
├── pages/
│   └── 1_Analyze_Document.py  # Document analysis page
└── core/
    └── agent.py            # Agent module (app.invoke())
```

## Chạy ứng dụng

Từ thư mục root của project:
```bash
python -m streamlit run frontend/app.py
```

Hoặc từ thư mục frontend:
```bash
cd frontend
python -m streamlit run app.py
```

## Tính năng

- Upload file .txt hoặc paste text
- Phân tích SRS/User Stories
- Hiển thị Conflicts, Ambiguities, Suggestions
- Export kết quả (JSON, Text)


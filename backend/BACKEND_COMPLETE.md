# ✅ Backend Hoàn Thiện - LangGraph Agent Pipeline

## 📋 Tổng kết những gì đã làm

### 1. ✅ Cập nhật Dependencies
- **requirements.txt**: Thêm `langchain-google-genai`
- **Đã cài đặt**: Tất cả packages cần thiết

### 2. ✅ Tạo Prompt Files (4 files)
Tất cả prompts được lưu trong `app/agents/prompts/`:
- **parse_requirements.txt**: Parse và tách requirements từ SRS text
- **detect_conflict.txt**: Phát hiện mâu thuẫn giữa requirements
- **check_ambiguity.txt**: Phát hiện requirements mơ hồ
- **suggest_improve.txt**: Đề xuất cải thiện requirements

### 3. ✅ LangGraph Agent với 5 Nodes (Đúng Spec)
File: `app/agents/langgraph_agent.py`

**Agent Pipeline:**
```
ParseNode → [ConflictCheckNode, ClarityCheckNode] (parallel) → MergeNode → ImproveNode → AggregatorNode
```

**Chi tiết các nodes:**
1. **ParseNode** (gemini-1.5-pro)
   - Phân tích văn bản, tách từng requirement
   - Output: `parsed_requirements` (List[str])

2. **ConflictCheckNode** (gemini-1.5-flash)
   - Phát hiện mâu thuẫn (contradiction/negation)
   - Output: `conflicts` (List[Dict])

3. **ClarityCheckNode** (gemini-1.5-flash)
   - Phát hiện câu mơ hồ (ambiguous terms)
   - Output: `ambiguities` (List[Dict])

4. **MergeResultsNode** (local function)
   - Đợi cả conflict và clarity check hoàn thành
   - Merge results từ parallel nodes

5. **ImproveNode** (gemini-1.5-pro)
   - Đề xuất rewrite rõ ràng hơn
   - Output: `suggestions` (List[Dict])

6. **AggregatorNode** (local function)
   - Gom kết quả, format thành JSON
   - Final output: `{conflicts, ambiguities, suggestions}`

### 4. ✅ File Upload Handler
File: `app/utils/file_handler.py`

**Chức năng:**
- Hỗ trợ upload `.txt` files
- Hỗ trợ upload `.docx` files
- Extract text từ file
- Auto cleanup temporary files

### 5. ✅ API Endpoints (2 endpoints)

#### POST `/api/analyze`
- **Input**: Text (JSON body)
- **Body**: `{"text": "...", "model": "gemini-1.5-pro"}`
- **Output**: `AnalyzeResponse` với conflicts, ambiguities, suggestions
- **Sử dụng**: LangGraph Agent pipeline

#### POST `/api/analyze/file`
- **Input**: File upload (multipart/form-data)
- **Parameters**: `file` (UploadFile), `model` (Form, optional)
- **Output**: `AnalyzeResponse` với conflicts, ambiguities, suggestions
- **Sử dụng**: LangGraph Agent pipeline

### 6. ✅ Schema & Models
File: `app/api/schema.py`

**Request Models:**
- `AnalyzeRequest`: Text input với optional model

**Response Models:**
- `ConflictItem`: {req1, req2, description}
- `AmbiguityItem`: {req, issue}
- `SuggestionItem`: {req, new_version}
- `AnalyzeResponse`: {conflicts, ambiguities, suggestions}

## 🏗️ Cấu trúc Project

```
backend/
├── app/
│   ├── agents/
│   │   ├── prompts/
│   │   │   ├── parse_requirements.txt
│   │   │   ├── detect_conflict.txt
│   │   │   ├── check_ambiguity.txt
│   │   │   └── suggest_improve.txt
│   │   └── langgraph_agent.py      # ✅ LangGraph Agent với 5 nodes
│   ├── api/
│   │   ├── router.py                # ✅ 2 endpoints: /analyze, /analyze/file
│   │   └── schema.py                # ✅ Request/Response models
│   ├── services/
│   │   └── analyzer.py              # (Cũ - có thể bỏ qua)
│   └── utils/
│       └── file_handler.py          # ✅ File upload handler
├── uploads/                         # Temporary file storage
├── main.py                          # FastAPI entry point
└── requirements.txt                 # ✅ Updated dependencies
```

## 🚀 Cách sử dụng

### 1. Khởi động server:
```bash
cd backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload
```

### 2. Test với Swagger UI:
- Mở: http://127.0.0.1:8000/docs
- Test endpoint `/api/analyze` (text input)
- Test endpoint `/api/analyze/file` (file upload)

### 3. Test với curl/PowerShell:

**Text input:**
```powershell
$body = @{
    text = "User must login. User should not login."
    model = "gemini-1.5-pro"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/analyze" `
  -Method POST -Body $body -ContentType "application/json"
```

**File upload:**
```powershell
$formData = @{
    file = Get-Item "path/to/srs.txt"
    model = "gemini-1.5-pro"
}

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/analyze/file" `
  -Method POST -Form $formData
```

## 🔍 LangGraph Workflow Flow

```
User Input (text/file)
    ↓
ParseNode: Extract requirements
    ↓
    ├─→ ConflictCheckNode (parallel) ─┐
    └─→ ClarityCheckNode (parallel) ──┤
                                      ↓
                          MergeResultsNode
                                      ↓
                          ImproveNode: Generate suggestions
                                      ↓
                          AggregatorNode: Format JSON
                                      ↓
                          Response: {conflicts, ambiguities, suggestions}
```

## ✨ Điểm mạnh của Implementation

1. **Đúng Spec**: 5 nodes theo đúng yêu cầu đề bài
2. **Parallel Processing**: Conflict và Clarity check chạy song song (nhanh hơn)
3. **File Support**: Hỗ trợ cả text và file upload (.txt, .docx)
4. **Error Handling**: Xử lý lỗi đầy đủ
5. **Clean Architecture**: Tách biệt rõ ràng (agents, api, utils)
6. **Prompt Engineering**: Prompts được lưu riêng, dễ chỉnh sửa

## 🐛 Known Issues / Notes

1. **Version Conflict**: 
   - `google-generativeai` và `langchain-google-genai` có conflict version
   - Đã fix bằng cách downgrade `google-ai-generativelanguage` về 0.6.15
   - Nếu có lỗi, chạy: `pip install google-ai-generativelanguage==0.6.15`

2. **Parallel Nodes**:
   - LangGraph không hỗ trợ nhiều edges vào cùng một node trực tiếp
   - Giải pháp: Dùng `merge_results_node` để đợi cả 2 parallel nodes hoàn thành

3. **JSON Parsing**:
   - Agent tự động parse JSON từ LLM response
   - Hỗ trợ cả markdown code blocks và plain JSON

## 📝 Next Steps (Frontend)

Backend đã sẵn sàng! Frontend team có thể:
1. Tạo React app với Vite
2. Implement FileUploader component
3. Implement ResultTabs (Conflicts, Ambiguities, Suggestions)
4. Connect với API endpoints `/api/analyze` và `/api/analyze/file`

---

## 🎉 Hoàn thành!

Backend đã được hoàn thiện với:
- ✅ LangGraph Agent đúng spec (5 nodes)
- ✅ File upload support
- ✅ 2 API endpoints
- ✅ Error handling
- ✅ Documentation

**Ready for Frontend integration!** 🚀


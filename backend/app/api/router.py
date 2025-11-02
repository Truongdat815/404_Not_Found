from fastapi import APIRouter, HTTPException
from app.api.schema import AnalyzeRequest, AnalyzeResponse, ConflictItem, AmbiguityItem, SuggestionItem
from app.services.analyzer import analyze_text

router = APIRouter(prefix="/api", tags=["Analysis"])

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_requirements(request: AnalyzeRequest):
    """
    Phân tích SRS/User Stories để tìm conflicts, ambiguities và đưa ra suggestions
    
    - **text**: Nội dung SRS/User Stories (text hoặc paste)
    - **model**: Model Gemini để sử dụng (mặc định: gemini-1.5-pro)
    
    Returns:
    - conflicts: Danh sách các mâu thuẫn giữa requirements
    - ambiguities: Danh sách các requirement mơ hồ
    - suggestions: Đề xuất cải thiện requirements
    """
    try:
        if not request.text or not request.text.strip():
            raise HTTPException(status_code=400, detail="Text input is required")
        
        # Gọi analyzer service
        result = analyze_text(request.text, request.model)
        
        # Kiểm tra nếu có lỗi
        if "error" in result:
            raise HTTPException(status_code=500, detail=f"Analysis error: {result['error']}")
        
        # Convert to response model
        conflicts = [ConflictItem(**item) for item in result.get("conflicts", [])]
        ambiguities = [AmbiguityItem(**item) for item in result.get("ambiguities", [])]
        suggestions = [SuggestionItem(**item) for item in result.get("suggestions", [])]
        
        return AnalyzeResponse(
            conflicts=conflicts,
            ambiguities=ambiguities,
            suggestions=suggestions,
            raw_response=result.get("raw_response")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


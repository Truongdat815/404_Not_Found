from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.api.schema import AnalyzeRequest, AnalyzeResponse, ConflictItem, AmbiguityItem, SuggestionItem
from app.agents.langgraph_agent import RequirementsAnalysisAgent
from app.utils.file_handler import extract_text_from_file, save_uploaded_file, cleanup_file
from app.database.db import get_db
from app.services.history_service import save_analysis
import os
from typing import Optional
import time

router = APIRouter(prefix="/api", tags=["Analysis"])

# Initialize agent singleton
_agent: Optional[RequirementsAnalysisAgent] = None

def get_agent() -> RequirementsAnalysisAgent:
    """Get or create agent instance"""
    global _agent
    if _agent is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        _agent = RequirementsAnalysisAgent(api_key=api_key)
    return _agent


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_requirements(request: AnalyzeRequest):
    """
    Phân tích SRS/User Stories từ text input để tìm conflicts, ambiguities và đưa ra suggestions
    
    Sử dụng LangGraph Agent với 5 nodes:
    - ParseNode: Phân tích và tách requirements
    - ConflictCheckNode: Phát hiện mâu thuẫn
    - ClarityCheckNode: Phát hiện mơ hồ
    - ImproveNode: Đề xuất cải thiện
    - AggregatorNode: Gom kết quả thành JSON
    
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
        
        # Get agent instance
        agent = get_agent()
        
        # Analyze using LangGraph agent
        start_time = time.time()
        result = agent.analyze(request.text)
        processing_time = int(time.time() - start_time)
        
        # Convert to response model
        conflicts = [ConflictItem(**item) for item in result.get("conflicts", [])]
        ambiguities = [AmbiguityItem(**item) for item in result.get("ambiguities", [])]
        suggestions = [SuggestionItem(**item) for item in result.get("suggestions", [])]
        
        # Lưu vào database (optional, không fail nếu DB không available)
        try:
            from app.database.db import get_engine
            engine = get_engine()
            if engine:
                from app.database.db import SessionLocal
                db = SessionLocal()
                try:
                    save_analysis(
                        db=db,
                        conflicts=[item.dict() for item in conflicts],
                        ambiguities=[item.dict() for item in ambiguities],
                        suggestions=[item.dict() for item in suggestions],
                        text_input=request.text,
                        file_name=None,
                        model_used=request.model,
                        processing_time_seconds=processing_time
                    )
                finally:
                    db.close()
        except Exception as e:
            # Log error nhưng không fail request
            print(f"Warning: Failed to save to database: {str(e)}")
        
        return AnalyzeResponse(
            conflicts=conflicts,
            ambiguities=ambiguities,
            suggestions=suggestions
        )
        
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.post("/analyze/file", response_model=AnalyzeResponse)
async def analyze_requirements_from_file(
    file: UploadFile = File(...),
    model: str = Form("gemini-1.5-pro")
):
    """
    Phân tích SRS/User Stories từ uploaded file
    
    Supports:
    - .txt files
    - .docx files
    
    Sử dụng LangGraph Agent với 5 nodes pipeline.
    
    Args:
        file: Uploaded file (.txt or .docx)
        model: Model Gemini để sử dụng (mặc định: gemini-1.5-pro)
    
    Returns:
        AnalyzeResponse với conflicts, ambiguities, suggestions
    """
    saved_file_path = None
    try:
        # Validate file type
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ['.txt', '.docx']:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type: {file_ext}. Supported types: .txt, .docx"
            )
        
        # Save uploaded file
        saved_file_path = save_uploaded_file(file)
        
        # Extract text from file
        text_content = extract_text_from_file(saved_file_path)
        
        if not text_content or not text_content.strip():
            raise HTTPException(status_code=400, detail="File is empty or could not extract text")
        
        # Get agent instance
        agent = get_agent()
        
        # Analyze using LangGraph agent
        start_time = time.time()
        result = agent.analyze(text_content)
        processing_time = int(time.time() - start_time)
        
        # Convert to response model
        conflicts = [ConflictItem(**item) for item in result.get("conflicts", [])]
        ambiguities = [AmbiguityItem(**item) for item in result.get("ambiguities", [])]
        suggestions = [SuggestionItem(**item) for item in result.get("suggestions", [])]
        
        # Lưu vào database (optional, không fail nếu DB không available)
        try:
            from app.database.db import get_engine
            engine = get_engine()
            if engine:
                from app.database.db import SessionLocal
                db = SessionLocal()
                try:
                    save_analysis(
                        db=db,
                        conflicts=[item.dict() for item in conflicts],
                        ambiguities=[item.dict() for item in ambiguities],
                        suggestions=[item.dict() for item in suggestions],
                        text_input=None,
                        file_name=file.filename,
                        model_used=model,
                        processing_time_seconds=processing_time
                    )
                finally:
                    db.close()
        except Exception as e:
            # Log error nhưng không fail request
            print(f"Warning: Failed to save to database: {str(e)}")
        
        return AnalyzeResponse(
            conflicts=conflicts,
            ambiguities=ambiguities,
            suggestions=suggestions
        )
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    finally:
        # Cleanup uploaded file
        if saved_file_path:
            cleanup_file(saved_file_path)


"""
API endpoints để quản lý lịch sử phân tích
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.db import get_db
from app.database.models import AnalysisHistory
from app.services.history_service import (
    get_analysis_history,
    get_analysis_by_id,
    get_analysis_count,
    delete_analysis,
    search_analysis
)
from pydantic import BaseModel

router = APIRouter(prefix="/api/history", tags=["History"])


class AnalysisHistoryResponse(BaseModel):
    """Response model cho analysis history"""
    id: int
    text_input: Optional[str]
    file_name: Optional[str]
    created_at: str
    conflicts: List[dict]
    ambiguities: List[dict]
    suggestions: List[dict]
    model_used: Optional[str]
    processing_time_seconds: Optional[int]

    class Config:
        from_attributes = True


class HistoryListResponse(BaseModel):
    """Response cho list history"""
    total: int
    limit: int
    offset: int
    items: List[AnalysisHistoryResponse]


@router.get("", response_model=HistoryListResponse)
async def get_history(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    order_by: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    """
    Lấy lịch sử phân tích
    
    - **limit**: Số lượng records (1-100)
    - **offset**: Số records bỏ qua (pagination)
    - **order_by**: Sắp xếp ("asc" hoặc "desc")
    """
    total = get_analysis_count(db)
    items = get_analysis_history(db, limit=limit, offset=offset, order_by=order_by)
    
    return HistoryListResponse(
        total=total,
        limit=limit,
        offset=offset,
        items=[AnalysisHistoryResponse(**item.to_dict()) for item in items]
    )


@router.get("/{analysis_id}", response_model=AnalysisHistoryResponse)
async def get_history_by_id(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    """
    Lấy kết quả phân tích theo ID
    """
    analysis = get_analysis_by_id(db, analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail=f"Analysis with ID {analysis_id} not found")
    
    return AnalysisHistoryResponse(**analysis.to_dict())


@router.delete("/{analysis_id}")
async def delete_history(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    """
    Xóa kết quả phân tích
    """
    success = delete_analysis(db, analysis_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Analysis with ID {analysis_id} not found")
    
    return {"message": f"Analysis {analysis_id} deleted successfully"}


@router.get("/search", response_model=List[AnalysisHistoryResponse])
async def search_history(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Tìm kiếm trong lịch sử phân tích
    """
    results = search_analysis(db, search_text=q, limit=limit)
    return [AnalysisHistoryResponse(**item.to_dict()) for item in results]


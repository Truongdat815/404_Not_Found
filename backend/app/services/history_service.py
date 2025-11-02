"""
Service để quản lý lịch sử phân tích trong database
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.models import AnalysisHistory
from app.utils.logger import logger
from datetime import datetime


def save_analysis(
    db: Session,
    conflicts: list,
    ambiguities: list,
    suggestions: list,
    text_input: Optional[str] = None,
    file_name: Optional[str] = None,
    model_used: Optional[str] = None,
    processing_time_seconds: Optional[int] = None
) -> AnalysisHistory:
    """
    Lưu kết quả phân tích vào database
    
    Args:
        db: Database session
        conflicts: List of conflict items
        ambiguities: List of ambiguity items
        suggestions: List of suggestion items
        text_input: Text input (nếu là paste)
        file_name: File name (nếu là upload)
        model_used: Model đã sử dụng
        processing_time_seconds: Thời gian xử lý
    
    Returns:
        AnalysisHistory object
    """
    analysis = AnalysisHistory(
        text_input=text_input,
        file_name=file_name,
        conflicts_json=conflicts,
        ambiguities_json=ambiguities,
        suggestions_json=suggestions,
        model_used=model_used,
        processing_time_seconds=processing_time_seconds
    )
    
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    
    logger.info(f"Analysis saved with ID: {analysis.id}")
    return analysis


def get_analysis_by_id(db: Session, analysis_id: int) -> Optional[AnalysisHistory]:
    """Lấy kết quả phân tích theo ID"""
    return db.query(AnalysisHistory).filter(AnalysisHistory.id == analysis_id).first()


def get_analysis_history(
    db: Session,
    limit: int = 50,
    offset: int = 0,
    order_by: str = "desc"  # "desc" hoặc "asc"
) -> List[AnalysisHistory]:
    """
    Lấy lịch sử phân tích
    
    Args:
        db: Database session
        limit: Số lượng records tối đa
        offset: Số records bỏ qua (pagination)
        order_by: Sắp xếp theo thời gian ("desc" = mới nhất trước)
    
    Returns:
        List of AnalysisHistory objects
    """
    query = db.query(AnalysisHistory)
    
    if order_by == "desc":
        query = query.order_by(AnalysisHistory.created_at.desc())
    else:
        query = query.order_by(AnalysisHistory.created_at.asc())
    
    return query.offset(offset).limit(limit).all()


def get_analysis_count(db: Session) -> int:
    """Đếm tổng số analysis records"""
    return db.query(AnalysisHistory).count()


def delete_analysis(db: Session, analysis_id: int) -> bool:
    """
    Xóa kết quả phân tích
    
    Returns:
        True nếu xóa thành công, False nếu không tìm thấy
    """
    analysis = get_analysis_by_id(db, analysis_id)
    if analysis:
        db.delete(analysis)
        db.commit()
        return True
    return False


def search_analysis(
    db: Session,
    search_text: Optional[str] = None,
    limit: int = 50
) -> List[AnalysisHistory]:
    """
    Tìm kiếm trong lịch sử phân tích
    
    Args:
        db: Database session
        search_text: Text để search trong text_input hoặc file_name
        limit: Số lượng kết quả tối đa
    
    Returns:
        List of AnalysisHistory objects
    """
    from app.utils.logger import logger
    from sqlalchemy import or_
    
    try:
        query = db.query(AnalysisHistory)
        
        if search_text:
            # SQL Server sử dụng .like() với pattern %text% cho case-insensitive search
            # Xử lý null values bằng cách dùng or_ với IS NULL check
            search_pattern = f"%{search_text}%"
            query = query.filter(
                or_(
                    AnalysisHistory.text_input.like(search_pattern),
                    AnalysisHistory.file_name.like(search_pattern)
                )
            )
        
        return query.order_by(AnalysisHistory.created_at.desc()).limit(limit).all()
    except Exception as e:
        logger.error(f"Error in search_analysis: {str(e)}")
        raise


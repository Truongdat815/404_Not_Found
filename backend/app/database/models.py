"""
SQLAlchemy models cho analysis history
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.database.db import Base


class AnalysisHistory(Base):
    """Model để lưu lịch sử phân tích"""
    __tablename__ = "analysis_history"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    text_input = Column(Text, nullable=True)  # Text input nếu là paste
    file_name = Column(String(255), nullable=True)  # Tên file nếu là upload
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Lưu kết quả dạng JSON
    conflicts_json = Column(JSON, nullable=True)  # List of conflicts
    ambiguities_json = Column(JSON, nullable=True)  # List of ambiguities
    suggestions_json = Column(JSON, nullable=True)  # List of suggestions
    
    # Metadata
    model_used = Column(String(50), nullable=True)  # Model đã dùng (gemini-1.5-pro)
    processing_time_seconds = Column(Integer, nullable=True)  # Thời gian xử lý (optional)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "text_input": self.text_input,
            "file_name": self.file_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "conflicts": self.conflicts_json or [],
            "ambiguities": self.ambiguities_json or [],
            "suggestions": self.suggestions_json or [],
            "model_used": self.model_used,
            "processing_time_seconds": self.processing_time_seconds
        }


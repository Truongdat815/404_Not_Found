"""
API endpoints để export kết quả phân tích
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from pathlib import Path
from app.database.db import get_db
from app.database.models import AnalysisHistory
from app.services.history_service import get_analysis_by_id
from app.services.export_service import (
    export_to_json,
    export_to_docx,
    cleanup_export_file
)
import os

router = APIRouter(prefix="/api/export", tags=["Export"])


@router.get("/json/{analysis_id}")
async def export_json(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    """
    Export kết quả phân tích ra JSON file
    
    Returns JSON file download
    """
    # Lấy analysis từ database
    analysis = get_analysis_by_id(db, analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail=f"Analysis with ID {analysis_id} not found")
    
    # Chuẩn bị data
    analysis_data = {
        "conflicts": analysis.conflicts_json or [],
        "ambiguities": analysis.ambiguities_json or [],
        "suggestions": analysis.suggestions_json or []
    }
    
    # Export to JSON
    timestamp = analysis.created_at.strftime("%Y%m%d_%H%M%S") if analysis.created_at else "unknown"
    filename = f"analysis_{analysis_id}_{timestamp}.json"
    output_path = f"exports/{filename}"
    
    try:
        export_path = export_to_json(analysis_data, output_path)
        
        # Return file
        if os.path.exists(export_path):
            return FileResponse(
                export_path,
                media_type="application/json",
                filename=filename,
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to generate export file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export error: {str(e)}")


@router.get("/docx/{analysis_id}")
async def export_docx(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    """
    Export kết quả phân tích ra DOCX file
    
    Returns DOCX file download
    """
    # Lấy analysis từ database
    analysis = get_analysis_by_id(db, analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail=f"Analysis with ID {analysis_id} not found")
    
    # Chuẩn bị data
    analysis_data = {
        "conflicts": analysis.conflicts_json or [],
        "ambiguities": analysis.ambiguities_json or [],
        "suggestions": analysis.suggestions_json or []
    }
    
    # Export to DOCX
    timestamp = analysis.created_at.strftime("%Y%m%d_%H%M%S") if analysis.created_at else "unknown"
    filename = f"analysis_{analysis_id}_{timestamp}.docx"
    output_path = f"exports/{filename}"
    
    try:
        export_path = export_to_docx(analysis_data, output_path)
        
        # Return file
        if os.path.exists(export_path):
            return FileResponse(
                export_path,
                media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                filename=filename,
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to generate export file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export error: {str(e)}")


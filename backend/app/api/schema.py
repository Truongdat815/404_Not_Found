from pydantic import BaseModel
from typing import List, Optional

# Request schemas
class AnalyzeRequest(BaseModel):
    """Request schema for text analysis"""
    text: str
    model: Optional[str] = "gemini-2.5-flash"  # Gemini 2.5 Flash (default)

# Response schemas
class ConflictItem(BaseModel):
    req1: str
    req2: str
    description: str

class AmbiguityItem(BaseModel):
    req: str
    issue: str

class SuggestionItem(BaseModel):
    req: str
    new_version: str

class AnalyzeResponse(BaseModel):
    conflicts: List[ConflictItem]
    ambiguities: List[AmbiguityItem]
    suggestions: List[SuggestionItem]
    analysis_id: Optional[int] = None  # ID của analysis trong database (nếu đã lưu)
    raw_response: Optional[str] = None


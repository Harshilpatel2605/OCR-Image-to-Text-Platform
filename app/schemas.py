"""Pydantic schemas for request/response validation"""
from pydantic import BaseModel
from typing import Optional


class OCRRequest(BaseModel):
    """OCR request schema"""
    file_path: str
    language: Optional[str] = "en"


class OCRResponse(BaseModel):
    """OCR response schema"""
    text: str
    confidence: Optional[float] = None
    file_name: str

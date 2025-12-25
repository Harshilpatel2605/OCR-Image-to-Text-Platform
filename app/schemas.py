"""Pydantic schemas for request/response validation"""
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime


class OCRResponse(BaseModel):
    """OCR upload response schema"""
    job_id: str
    status: str
    preview: str
    message: str


class StatusResponse(BaseModel):
    """Job status response schema"""
    job_id: str
    status: str
    created_at: Optional[datetime]
    completed_at: Optional[datetime]


class PreviewResponse(BaseModel):
    """Preview response schema"""
    job_id: str
    text: str
    pages: Optional[int]


class EditRequest(BaseModel):
    """Edit text request schema"""
    text: str


class DownloadResponse(BaseModel):
    """Download response schema"""
    job_id: str
    format: str
    file_path: str
    file_name: str


class AllFormatsResponse(BaseModel):
    """All available formats response"""
    job_id: str
    outputs: Dict[str, str]  # {"txt": path, "docx": path, "pdf": path}

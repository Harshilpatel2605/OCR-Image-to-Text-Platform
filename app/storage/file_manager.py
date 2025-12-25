import os
import json
from datetime import datetime
from typing import Optional, Dict

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
JOBS_DIR = "jobs"

# Create directories
for dir in [UPLOAD_DIR, OUTPUT_DIR, JOBS_DIR]:
    os.makedirs(dir, exist_ok=True)


class JobManager:
    """Manage OCR job metadata and files"""

    @staticmethod
    def create_job(job_id: str) -> Dict:
        """Create a new job record"""
        job_data = {
            "job_id": job_id,
            "status": "processing",
            "created_at": datetime.now().isoformat(),
            "completed_at": None,
            "original_text": None,
            "edited_text": None,
            "outputs": {
                "txt": None,
                "docx": None,
                "pdf": None
            }
        }
        
        job_file = os.path.join(JOBS_DIR, f"{job_id}.json")
        with open(job_file, "w") as f:
            json.dump(job_data, f)
        
        return job_data

    @staticmethod
    def get_job(job_id: str) -> Optional[Dict]:
        """Retrieve job metadata"""
        job_file = os.path.join(JOBS_DIR, f"{job_id}.json")
        
        if not os.path.exists(job_file):
            return None
        
        with open(job_file, "r") as f:
            return json.load(f)

    @staticmethod
    def update_job(job_id: str, **kwargs) -> Dict:
        """Update job metadata"""
        job_data = JobManager.get_job(job_id)
        
        if not job_data:
            raise ValueError(f"Job {job_id} not found")
        
        job_data.update(kwargs)
        
        job_file = os.path.join(JOBS_DIR, f"{job_id}.json")
        with open(job_file, "w") as f:
            json.dump(job_data, f, indent=2)
        
        return job_data

    @staticmethod
    def complete_job(job_id: str) -> Dict:
        """Mark job as completed"""
        return JobManager.update_job(
            job_id,
            status="completed",
            completed_at=datetime.now().isoformat()
        )

    @staticmethod
    def save_outputs(job_id: str, txt_path: str = None, docx_path: str = None, pdf_path: str = None) -> Dict:
        """Save output file paths"""
        job_data = JobManager.get_job(job_id)
        
        if txt_path:
            job_data["outputs"]["txt"] = txt_path
        if docx_path:
            job_data["outputs"]["docx"] = docx_path
        if pdf_path:
            job_data["outputs"]["pdf"] = pdf_path
        
        job_file = os.path.join(JOBS_DIR, f"{job_id}.json")
        with open(job_file, "w") as f:
            json.dump(job_data, f, indent=2)
        
        return job_data


def save_upload(file_bytes, filename):
    """Save uploaded file"""
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        f.write(file_bytes)
    return path


def save_output(content, filename):
    """Save output file"""
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

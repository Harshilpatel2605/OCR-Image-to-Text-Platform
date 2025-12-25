from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
import uuid
import os
from app.ocr.engine import ocr_image
from app.ocr.pdf_utils import pdf_to_images
from app.ocr.postprocess import PostProcessor
from app.exporters.docx_export import export_docx
from app.exporters.txt import export_txt
from app.exporters.searchable_pdf import export_searchable_pdf
from app.storage.file_manager import JobManager, save_output, OUTPUT_DIR
from app.schemas import OCRResponse, StatusResponse, PreviewResponse, EditRequest, AllFormatsResponse

router = APIRouter()
post = PostProcessor()


def process_ocr_background(job_id: str, images: list):
    """Process OCR in background"""
    try:
        results = []
        
        for img in images:
            raw_text = ocr_image(img)
            clean_text = post.process(raw_text)
            results.append(clean_text)
        
        final_text = "\n\n".join(results)
        
        # Save original text
        JobManager.update_job(
            job_id,
            original_text=final_text,
            edited_text=final_text
        )
        
        # Export to all formats
        txt_path = export_txt(final_text, job_id)
        docx_path = export_docx(final_text, job_id)
        pdf_path = export_searchable_pdf(final_text, job_id)
        
        # Save output paths
        JobManager.save_outputs(job_id, txt_path, docx_path, pdf_path)
        
        # Mark as completed
        JobManager.complete_job(job_id)
        
    except Exception as e:
        JobManager.update_job(
            job_id,
            status="failed",
            error=str(e)
        )


@router.post("/ocr", response_model=OCRResponse)
async def run_ocr(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    """
    Upload an image or PDF for OCR processing.
    Returns job_id for tracking progress.
    """
    job_id = str(uuid.uuid4())
    
    # Create job record
    JobManager.create_job(job_id)
    
    try:
        file_content = await file.read()
        
        # Determine file type and extract images
        if file.filename.endswith(".pdf"):
            from io import BytesIO
            images = pdf_to_images(BytesIO(file_content))
        else:
            images = [file_content]
        
        # Process in background
        background_tasks.add_task(process_ocr_background, job_id, images)
        
        return OCRResponse(
            job_id=job_id,
            status="processing",
            preview="Processing your file...",
            message="Your file has been queued for processing. Use the job_id to check status."
        )
    
    except Exception as e:
        JobManager.update_job(job_id, status="failed", error=str(e))
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/status/{job_id}", response_model=StatusResponse)
async def get_status(job_id: str):
    """Get the status of an OCR job"""
    job = JobManager.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return StatusResponse(
        job_id=job_id,
        status=job["status"],
        created_at=job["created_at"],
        completed_at=job["completed_at"]
    )


@router.get("/preview/{job_id}", response_model=PreviewResponse)
async def get_preview(job_id: str):
    """Get preview of extracted text"""
    job = JobManager.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if not job["edited_text"]:
        raise HTTPException(status_code=202, detail="Job still processing")
    
    return PreviewResponse(
        job_id=job_id,
        text=job["edited_text"],
        pages=len(job["edited_text"].split("\n\n"))
    )


@router.put("/edit/{job_id}")
async def edit_text(job_id: str, request: EditRequest):
    """Update extracted text (user edits)"""
    job = JobManager.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Update edited text
    JobManager.update_job(
        job_id,
        edited_text=request.text
    )
    
    # Re-export all formats with edited text
    txt_path = export_txt(request.text, job_id)
    docx_path = export_docx(request.text, job_id)
    pdf_path = export_searchable_pdf(request.text, job_id)
    
    JobManager.save_outputs(job_id, txt_path, docx_path, pdf_path)
    
    return {
        "job_id": job_id,
        "message": "Text updated successfully",
        "outputs": job["outputs"]
    }


@router.get("/download/{job_id}/{format}")
async def download_file(job_id: str, format: str):
    """Download processed file in specified format"""
    job = JobManager.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if format not in job["outputs"] or not job["outputs"][format]:
        raise HTTPException(status_code=400, detail=f"Format '{format}' not available")
    
    file_path = job["outputs"][format]
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Determine media type
    media_types = {
        "txt": "text/plain",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "pdf": "application/pdf"
    }
    
    return FileResponse(
        file_path,
        media_type=media_types.get(format, "application/octet-stream"),
        filename=f"document_{job_id}.{format}"
    )


@router.get("/outputs/{job_id}", response_model=AllFormatsResponse)
async def get_all_outputs(job_id: str):
    """Get all available output formats for a job"""
    job = JobManager.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return AllFormatsResponse(
        job_id=job_id,
        outputs=job["outputs"]
    )

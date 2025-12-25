from fastapi import APIRouter, UploadFile, File
import uuid
from app.ocr.engine import ocr_image
from app.ocr.pdf_utils import pdf_to_images
from app.ocr.postprocess import PostProcessor
from app.exporters.docx_export import export_docx
from app.exporters.txt import export_txt

router = APIRouter()
post = PostProcessor()

@router.post("/ocr")
async def run_ocr(file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())

    if file.filename.endswith(".pdf"):
        images = pdf_to_images(file)
    else:
        images = [await file.read()]

    results = []
    for img in images:
        raw_text = ocr_image(img)
        clean_text = post.process(raw_text)
        results.append(clean_text)

    final_text = "\n\n".join(results)

    txt_path = export_txt(final_text, job_id)
    docx_path = export_docx(final_text, job_id)

    return {
        "job_id": job_id,
        "preview": final_text[:1500],
        "outputs": {
            "txt": txt_path,
            "docx": docx_path
        }
    }

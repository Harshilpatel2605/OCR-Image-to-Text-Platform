from docx import Document
import os

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def export_docx(text, job_id):
    doc = Document()
    for para in text.split("\n"):
        doc.add_paragraph(para)
    path = f"{OUTPUT_DIR}/{job_id}.docx"
    doc.save(path)
    return path

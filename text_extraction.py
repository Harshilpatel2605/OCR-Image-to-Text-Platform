import pdfplumber
import easyocr
import numpy as np 
import cv2
from docx import Document
import os

reader = easyocr.Reader(['en'])  # GPU=False since you're CPU-only


def preprocess_for_ocr(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.fastNlMeansDenoising(gray, h=20)


def extract_text_pdf(path):
    pages = []

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            # Fast path: selectable text exists
            if text and len(text.strip()) > 50:
                pages.append(text)
                continue

            # Extra cheap check
            if page.extract_words():
                pages.append(text or "")
                continue

            # OCR fallback
            img = np.array(page.to_image(resolution=200).original)
            img = preprocess_for_ocr(img)

            result = reader.readtext(
                img,
                detail=0,
                paragraph=True
            )

            pages.append(" ".join(result))

            del img  # free memory

    return pages



def extract_text_docx(path):
    doc = Document(path)
    pages = []

    current_page = []

    for para in doc.paragraphs:
        if para.text.strip():
            current_page.append(para.text)

        # Simple page break heuristic
        if para.text.strip() == "":
            pages.append(" ".join(current_page))
            current_page = []

    if current_page:
        pages.append(" ".join(current_page))

    return pages




def extract_text(path):
    ext = os.path.splitext(path)[1].lower()

    if ext == ".pdf":
        return extract_text_pdf(path)

    elif ext == ".docx":
        return extract_text_docx(path)

    else:
        raise ValueError("Unsupported file format")



if __name__ == "__main__":
    path = "./Sample/selectable1.pdf"
    pages = extract_text(path)
    print(pages) 
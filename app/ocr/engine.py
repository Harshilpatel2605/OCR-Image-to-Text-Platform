import easyocr
from app.ocr.preprocess import preprocess

reader = easyocr.Reader(['en'], gpu=False)

def ocr_image(image_bytes: bytes) -> str:
    processed = preprocess(image_bytes)
    results = reader.readtext(processed, detail=0, paragraph=True)
    return "\n".join(results)

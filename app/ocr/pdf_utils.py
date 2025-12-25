import pdfplumber
import cv2
import numpy as np

def pdf_to_images(upload_file):
    images = []
    with pdfplumber.open(upload_file.file) as pdf:
        for page in pdf.pages:
            img = page.to_image(resolution=300).original
            _, buffer = cv2.imencode(".png", np.array(img))
            images.append(buffer.tobytes())
    return images

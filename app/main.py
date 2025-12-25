from fastapi import FastAPI
from app.api import router

app = FastAPI(
    title="OCR Image-to-Text Platform",
    version="1.0.0"
)

app.include_router(router)

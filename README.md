# OCR Image-to-Text Platform

A comprehensive OCR (Optical Character Recognition) platform that extracts text from images and PDFs with support for multiple export formats.

## Project Structure

```
Hackathon/
│
├── app/                          # Main application package
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # FastAPI entry point
│   ├── api.py                   # API routes
│   ├── schemas.py               # Pydantic request/response schemas
│   │
│   ├── ocr/                     # OCR processing module
│   │   ├── __init__.py
│   │   ├── engine.py            # EasyOCR wrapper & main OCR logic
│   │   ├── preprocess.py        # Image preprocessing with OpenCV
│   │   ├── postprocess.py       # Text cleaning and corrections
│   │   └── pdf_utils.py         # PDF handling utilities
│   │
│   ├── exporters/               # Export formats
│   │   ├── __init__.py
│   │   ├── txt.py               # Plain text export
│   │   ├── docx_export.py       # Word document export
│   │   └── searchable_pdf.py    # Searchable PDF export
│   │
│   └── storage/                 # File management
│       ├── __init__.py
│       └── file_manager.py      # Upload/cleanup utilities
│
├── uploads/                     # Temporary uploaded files
├── outputs/                     # Exported files
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules (includes venv)
└── README.md                      
```

##  Features

- **Multi-format OCR**: Extract text from images (JPG, PNG, BMP, TIFF, WebP)
- **PDF Processing**: 
  - Extracts selectable text when available
  - Falls back to OCR for scanned PDFs
- **DOCX Support**: Extract text from Word documents
- **Image Preprocessing**: Automatic image enhancement for better OCR accuracy
  - Grayscale conversion
  - CLAHE contrast enhancement
  - Denoising
  - Adaptive thresholding
- **Text Postprocessing**: Automatic cleanup and error correction
- **Multiple Export Formats**:
  - Plain text (.txt)
  - Word document (.docx) with formatting
  - Searchable PDF (.pdf)
- **FastAPI Backend**: RESTful API for easy integration
- **File Management**: Automatic cleanup of old files

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Harshilpatel2605/OCR-Image-to-Text-Platform.git
cd Hackathon
```

### 2. Create Virtual Environment

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Required Dependencies

```
fastapi==0.104.1
uvicorn==0.24.0
easyocr==1.7.0
opencv-python==4.8.1
pillow==10.1.0
pdfplumber==0.10.3
pdf2image==1.17.1
pypdf==3.17.1
python-docx==0.8.11
reportlab==4.0.8
pydantic==2.5.0
```

## 📖 Usage

### Start the API Server

```bash
python -m app.main
```

The API will be available at `http://localhost:8000`

### API Endpoints

#### 1. **Health Check**
```bash
GET /health
```

#### 2. **Extract from Image**
```bash
POST /api/extract-text
Parameters:
  - file: Image file (multipart/form-data)
  - export_format: "text" | "docx" | "pdf" (optional, default: "text")
```

#### 3. **Extract from PDF**
```bash
POST /api/extract-pdf
Parameters:
  - file: PDF file (multipart/form-data)
  - export_format: "text" | "docx" | "pdf" (optional, default: "text")
```

#### 4. **Auto-detect Format**
```bash
POST /api/extract-auto
Parameters:
  - file: Any supported file (multipart/form-data)
  - export_format: "text" | "docx" | "pdf" (optional, default: "text")
```

### Example Request (Using cURL)

```bash
curl -X POST "http://localhost:8000/api/extract-text?export_format=docx" \
  -F "file=@path/to/image.jpg"
```

### Example Response

```json
{
  "success": true,
  "text": "Extracted text content...",
  "file_name": "image.jpg",
  "confidence": 0.95,
  "export_file": "/outputs/image_20231224_120000.docx"
}
```

## Module Documentation

### `app.ocr.engine.OCREngine`

Main OCR engine with text extraction capabilities.

**Key Methods:**
- `extract_text(image_path)` - Extract from image
- `extract_from_pdf(pdf_path)` - Extract from PDF
- `extract_text_auto(path)` - Auto-detect and extract
- `extract_text_docx(path)` - Extract from DOCX

### `app.ocr.preprocess.PreProcessor`

Image preprocessing pipeline.

**Key Methods:**
- `process(image)` - Apply full preprocessing pipeline
- `resize_image(image, scale)` - Resize image
- `rotate_image(image, angle)` - Rotate image

### `app.ocr.postprocess.PostProcessor`

Text cleaning and correction.

**Key Methods:**
- `clean(text)` - Remove extra whitespace and fix hyphenation
- `normalize_text(text)` - Normalize line structure
- `remove_noise(text)` - Remove URLs and emails
- `correct_common_errors(text)` - Fix OCR mistakes

### `app.storage.file_manager.FileManager`

File handling and management.

**Key Methods:**
- `save_upload(file)` - Save uploaded file
- `delete_file(file_path)` - Delete file
- `cleanup_old_files(days)` - Remove old files

## Performance Tips

1. **Image Quality**: Use high-resolution images (300+ DPI) for better accuracy
2. **Language Support**: Modify the `languages` parameter in OCREngine for other languages
3. **GPU Support**: Set `gpu=True` in OCREngine if you have CUDA installed
4. **Batch Processing**: Process multiple files sequentially or implement async handling

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
# Or install specific package
pip install easyocr
```

### Poor OCR accuracy
- Use higher resolution images
- Ensure images are well-lit and not skewed
- The preprocessing pipeline is automatically applied

### PDF processing slow
- PDFs with many pages take longer to process
- Scanned PDFs are slower than text-based PDFs

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues and questions, please open an issue on GitHub.

---

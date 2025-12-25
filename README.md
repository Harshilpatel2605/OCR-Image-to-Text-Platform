# OCR Image-to-Text Platform

A backend service that extracts text from images and scanned PDFs using OCR.
It provides editable text outputs such as TXT and DOCX through a REST API.

---

## Features

* Image to text extraction
* Scanned PDF OCR
* Batch page processing for PDFs
* Text postprocessing and cleanup
* Export formats:

  * Plain text (`.txt`)
  * Word document (`.docx`)
* API documentation via Swagger UI

---

## Tech Stack

* Python 3.9+
* FastAPI
* EasyOCR
* OpenCV
* pdfplumber
* python-docx

---

## Project Structure

```
Hackfusion/
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
├── LICENSE                      # License file
├── ProblemStatement.jpeg        # Problem statement document
└── README.md                    # Project documentation
```

---

## Setup Instructions

### 1. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the server

```bash
uvicorn app.main:app --reload
```

---

## Using the API

Open the browser at:

```
http://127.0.0.1:8000/docs
```

### OCR Endpoint

* **Method:** POST
* **Path:** `/ocr`
* **Input:** Image file (`.png`, `.jpg`) or scanned PDF (`.pdf`)

Steps:

1. Click `/ocr`
2. Click **Try it out**
3. Upload a file
4. Click **Execute**

---

## Output

The API returns:

* Extracted text preview
* Download paths for:

  * `.txt`
  * `.docx`

Processed files are stored in the `outputs/` directory.

---

## Notes

* Designed as a backend service
* Frontend can be added on top of the API
* OCR accuracy depends on input image quality

---

## Future Improvements

* Searchable PDF export
* Handwritten text recognition
* Frontend UI
* Document search

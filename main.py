import datetime
import io
from pathlib import Path
import pdfplumber
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from core import analyze

app = FastAPI()

MIN_CHARS = 200
MAX_CHARS = 8000
DAILY_LIMIT = 10
MAX_PDF_BYTES = 2 * 1024 * 1024
MAX_PDF_PAGES = 5
usage = {"day": "", "count": 0}


class Request(BaseModel):
    resume: str
    job: str


def check_limit():
    today = str(datetime.date.today())
    if usage["day"] != today:
        usage["day"] = today
        usage["count"] = 0
    if usage["count"] >= DAILY_LIMIT:
        raise HTTPException(status_code=429, detail="Daily limit reached. Please try again tomorrow.")
    usage["count"] += 1


@app.get("/")
def home():
    return FileResponse(Path(__file__).parent / "index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/extract-pdf")
def extract_pdf(file: UploadFile = File(...)):
    if not (file.filename or "").lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")
    data = file.file.read(MAX_PDF_BYTES + 1)
    if len(data) > MAX_PDF_BYTES:
        raise HTTPException(status_code=400, detail="The PDF is too large. Limit is 2 MB.")
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            for page in pdf.pages[:MAX_PDF_PAGES]:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception:
        raise HTTPException(status_code=400, detail="Could not read this PDF.")
    if not text.strip():
        raise HTTPException(status_code=400, detail="No readable text found. Scanned PDFs are not supported.")
    return {"text": text}


@app.post("/analyze")
def analyze_endpoint(req: Request):
    resume = req.resume.strip()
    job = req.job.strip()
    if len(resume) < MIN_CHARS or len(job) < MIN_CHARS:
        raise HTTPException(status_code=400, detail="Please paste at least 200 characters for both the resume and the job description.")
    if len(resume) > MAX_CHARS or len(job) > MAX_CHARS:
        raise HTTPException(status_code=400, detail="Text is too long. Limit is 8000 characters each.")
    check_limit()
    result = analyze(resume, job)
    if result is None:
        raise HTTPException(status_code=502, detail="The analysis failed. Try again later.")
    return result
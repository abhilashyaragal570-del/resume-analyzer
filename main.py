import datetime
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from core import analyze

app = FastAPI()

MIN_CHARS = 200
MAX_CHARS = 8000
DAILY_LIMIT = 10
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
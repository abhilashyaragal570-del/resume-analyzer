import os
import json
import time
import sys
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

folder = Path(__file__).parent
load_dotenv(folder / ".env")
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API key not found. Check your .env file.")
    raise SystemExit

MODEL = "models/gemini-3.6-flash"

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(timeout=60000)
)

resume_name = sys.argv[1] if len(sys.argv) > 1 else "resume.txt"
job_name = sys.argv[2] if len(sys.argv) > 2 else "job.txt"
try:
    resume = (folder / resume_name).read_text(encoding="utf-8")
    job = (folder / job_name).read_text(encoding="utf-8")
except FileNotFoundError as e:
    print("File not found:", e.filename)
    raise SystemExit

print("Resume characters:", len(resume))
print("Job characters:", len(job))

prompt = f"""You are a resume analyzer. Compare the resume with the job description.
Use ONLY information that is written in the resume. Do not invent skills.
Reply with ONLY valid JSON, no extra words, in this format:
{{"match_score": 0, "matching_skills": ["..."], "missing_skills": ["..."], "suggestions": ["..."]}}

match_score is a number from 0 to 100.
suggestions are 3 short, specific ways to improve the resume for this job.

RESUME:
{resume}

JOB DESCRIPTION:
{job}"""

response = None
for attempt in range(3):
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        break
    except Exception as e:
        print(f"Attempt {attempt + 1} failed: {type(e).__name__}: {e}")
        time.sleep(5)

if response and response.text:
    raw = response.text.strip()
    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        data = json.loads(raw)
        print("\nMatch score:", data["match_score"], "/ 100")

        print("\nMatching skills:")
        for skill in data["matching_skills"]:
            print("-", skill)

        print("\nMissing skills:")
        for skill in data["missing_skills"]:
            print("-", skill)

        print("\nSuggestions:")
        for tip in data["suggestions"]:
            print("-", tip)
    except (json.JSONDecodeError, KeyError):
        print("Could not read the reply. Raw reply:")
        print(raw)
else:
    print("No answer. Try again later.")
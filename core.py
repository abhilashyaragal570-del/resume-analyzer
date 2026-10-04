import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(Path(__file__).parent / ".env")
api_key = os.getenv("GEMINI_API_KEY")

MODEL = "models/gemini-3.6-flash"

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(timeout=60000)
)


def analyze(resume, job):
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

    if not response or not response.text:
        return None

    raw = response.text.strip()
    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None
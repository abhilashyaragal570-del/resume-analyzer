# Resume Analyzer

Compares a resume with a job description using the Gemini API. It returns a match score, matching skills, missing skills, and suggestions. It works as a command-line tool and as a small web app built with FastAPI.

## How it works

1. You give it a resume and a job description as text.
2. A prompt tells Gemini to use only information written in the resume, and to reply with JSON.
3. The reply is parsed and shown as a readable report.
4. API errors are retried, and bad input is rejected before it reaches the model.

## Run the web app

1. Install the packages: `pip install -r requirements.txt`
2. Create a `.env` file in this folder with: `GEMINI_API_KEY=your-key`
3. Start the server: `uvicorn main:app --reload`
4. Open `http://127.0.0.1:8000`, paste a resume and a job description, and click Analyze.

## Run the command-line version

`python analyze.py sample_resume.txt job.txt`

To use your own resume, put the text in `resume.txt` and run `python analyze.py`. `resume.txt` and `.env` are in `.gitignore`, so your resume and key are never pushed.

## Safety limits in the web app

- Each text must be 200 to 8000 characters.
- At most 10 analyses per day, to protect the free API quota.

## Known limits

- The score depends on the job description you give it. A senior posting scores much lower than a junior one.
- It is a language model, so it can make mistakes. I checked one report by hand against my resume, but I have not run a larger test.
- The daily counter is kept in memory, so it resets when the server restarts.
- It reads plain text only, not PDF or Word files yet.
- Text you paste is sent to the Gemini API, so don't paste anything you want to keep private.

## What I learned

- Writing prompts that return structured JSON and parsing the reply
- Building a FastAPI endpoint and a simple HTML page that calls it
- Validating input and limiting usage on a public API
- Keeping private files out of Git with .gitignore
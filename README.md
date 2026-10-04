# Resume Analyzer

Compares a resume with a job description using the Gemini API. It returns a match score, matching skills, missing skills, and suggestions. It works as a command-line tool and as a small web app built with FastAPI.

**Live demo:** https://resume-analyzer-r9rf.onrender.com

The free server sleeps when idle, so the first load can take about a minute. The demo allows 10 analyses per day.

## How it works

1. You give it a resume (pasted text or a text-based PDF) and a job description.
2. PDF text is extracted with pdfplumber and shown in the Resume box so you can check it.
3. A prompt tells Gemini to use only information written in the resume, and to reply with JSON.
4. The reply is parsed and shown as a readable report with a color-coded score, skill tags, and suggestions.
5. API errors are retried, and bad input is rejected before it reaches the model.

## Run the web app

1. Install the packages: `pip install -r requirements.txt`
2. Create a `.env` file in this folder with: `GEMINI_API_KEY=your-key`
3. Start the server: `uvicorn main:app --reload`
4. Open `http://127.0.0.1:8000`, upload a PDF or paste a resume, paste a job description, and click Analyze.

## Run the command-line version

`python analyze.py sample_resume.txt job.txt`

PDFs also work, for example `python analyze.py my_resume.pdf job.txt`.

To use your own resume, put the text in `resume.txt` and run `python analyze.py`. `resume.txt` and `.env` are in `.gitignore`, so your resume and key are never pushed.

## Safety limits in the web app

- Each text must be 200 to 8000 characters.
- PDF uploads: .pdf files only, up to 2 MB, first 5 pages. The file is read in memory and never saved.
- At most 10 analyses per day, to protect the free API quota. PDF extraction does not count toward it.

## Known limits

- The score depends on the job description you give it. A senior posting scores much lower than a junior one.
- It is a language model, so it can make mistakes, and scores vary by a few points between runs. I checked one report by hand against my resume, but I have not run a larger test.
- The daily counter is kept in memory, so it resets when the server restarts.
- Text-based PDFs can be uploaded (2 MB, first 5 pages). Scanned PDFs are not supported because there is no OCR, and Word files are not supported.
- Text you paste or upload is sent to the Gemini API, so don't use anything you want to keep private.

## What I learned

- Writing prompts that return structured JSON and parsing the reply
- Building FastAPI endpoints and a simple HTML page that calls them
- Handling file uploads safely: type, size, and page limits, with no file stored
- Extracting text from PDFs with pdfplumber
- Validating input and limiting usage on a public API
- Keeping private files out of Git with .gitignore
- Deploying a FastAPI app to the internet with Render
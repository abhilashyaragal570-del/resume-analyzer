# Resume Analyzer

A command-line tool that compares a resume with a job description using the Gemini API. It prints a match score, matching skills, missing skills, and suggestions.

## How it works

1. Reads a resume file and a job description file.
2. Sends both to Gemini with a prompt that says to use only information written in the resume.
3. Asks for JSON, parses it, and prints a readable report.
4. Retries on API errors and shows a short message if a file is missing.

## Run it

1. Install the packages: `pip install -r requirements.txt`
2. Create a `.env` file in this folder with: `GEMINI_API_KEY=your-key`
3. Try the sample files: `python analyze.py sample_resume.txt job.txt`
4. Use your own: put your text in `resume.txt` and run `python analyze.py`

`resume.txt` and `.env` are in `.gitignore`, so your resume and key are never pushed.

## Known limits

- The score depends on the job description you give it. A senior posting scores much lower than a junior one.
- It is a language model, so it can make mistakes. I checked one report by hand against my resume and the skills it listed matched, but I have not run a larger test.
- It reads plain text only, not PDF or Word files yet.

## What I learned

- Writing prompts that return structured JSON and parsing the reply
- Reading file names from the command line with sys.argv
- Handling missing files and API errors
- Keeping private files out of Git with .gitignore
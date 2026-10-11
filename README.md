ResumeIQ — AI Resume Analyzer

ResumeIQ is a Python-based resume analysis application that compares a candidate's resume with a target job description. It identifies matching skills, highlights potential skill gaps, and generates a downloadable analysis report.

Features

- PDF Resume Parsing: Extracts text from uploaded PDF resumes.
- Skill Detection: Identifies technical and selected professional skills.
- Skill Gap Analysis: Shows matched skills and skills not detected in the resume.
- Text Similarity: Uses TF-IDF vectorization and cosine similarity to estimate textual overlap.
- Analysis Dashboard: Displays score cards and a skills comparison chart.
- CSV Export: Downloads a report containing scores and skill comparisons.
- Input Validation: Handles missing inputs and PDFs without selectable text.

Tech Stack

- Python
- Streamlit
- PyMuPDF
- Scikit-learn
- Pandas
- Pytest

How It Works

1. Upload a text-based PDF resume.
2. Paste a job description.
3. Run the analysis.
4. Review the estimated scores, matched skills, and potential skill gaps.
5. Download the analysis report as a CSV file.

Installation

Clone this repository:

git clone https://github.com/Sakeena19-cse/ResumeIQ.git
cd ResumeIQ

Create and activate a virtual environment:

python -m venv .venv

On Windows:

.venv\Scripts\activate

Install the dependencies:

pip install -r requirements.txt

Run the application:

python -m streamlit run app.py

Run Tests

python -m pytest -v

Limitations

- The application currently supports text-based PDFs; scanned PDFs may require OCR.
- Skill detection depends on a predefined skill dictionary and may miss alternative wording.
- Text similarity and overall match scores are experimental indicators, not hiring probabilities or measures of candidate ability.
- Users should verify the results and include only skills they genuinely possess.

Future Improvements

- Expand the skill dictionary and improve contextual skill detection.
- Add analysis history and user accounts.
- Support OCR for scanned resumes.
- Add more comprehensive automated tests.

Author
Sakeena A B 

Disclaimer

ResumeIQ is an informational tool intended to support resume review. It does not guarantee ATS compatibility, interview selection, or employment.
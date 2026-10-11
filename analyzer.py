import re

import fitz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Recognized skills and their common aliases.
SKILLS = {
    "python": ["python"],
    "java": ["java"],
    "javascript": ["javascript", "js"],
    "html": ["html"],
    "css": ["css"],
    "react": ["react", "react.js"],
    "node.js": ["node.js", "nodejs"],
    "flask": ["flask"],
    "django": ["django"],
    "sql": ["sql"],
    "mongodb": ["mongodb", "mongo db"],
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning"],
    "natural language processing": [
        "natural language processing", "nlp"
    ],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "power bi": ["power bi"],
    "excel": ["excel", "microsoft excel"],
    "git": ["git"],
    "github": ["github"],
    "rest api": ["rest api", "restful api"],
    "docker": ["docker"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "communication": ["communication skills"],
    "problem solving": ["problem solving"],
}


def normalize_text(text):
    """Normalize text before skill matching."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\s-]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def find_skills(text):
    """Find recognized skills using keyword and alias matching."""
    normalized = normalize_text(text)
    found = set()

    for skill, aliases in SKILLS.items():
        for alias in aliases:
            pattern = (
                r"(?<!\w)" + re.escape(alias) + r"(?!\w)"
            )

            if re.search(pattern, normalized):
                found.add(skill)
                break

    return sorted(found)


def extract_pdf_text(pdf_file):
    """Extract selectable text from an uploaded PDF."""
    with fitz.open(
        stream=pdf_file.getvalue(),
        filetype="pdf"
    ) as document:
        text = "\n".join(
            page.get_text() for page in document
        ).strip()

    if not text:
        raise ValueError(
            "No selectable text found. Try a text-based PDF."
        )

    return text


def calculate_similarity(resume_text, job_text):
    """Measure TF-IDF cosine similarity between two texts."""
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    try:
        vectors = vectorizer.fit_transform(
            [resume_text, job_text]
        )
        score = cosine_similarity(
            vectors[0:1], vectors[1:2]
        )[0][0]

        return round(float(score) * 100, 2)

    except ValueError:
        return 0.0


def analyze_resume(resume_text, job_text):
    """Compare recognized skills and textual similarity."""
    if not resume_text.strip() or not job_text.strip():
        raise ValueError(
            "Resume text and job description are required."
        )

    resume_skills = set(find_skills(resume_text))
    job_skills = set(find_skills(job_text))

    matched = sorted(resume_skills & job_skills)
    missing = sorted(job_skills - resume_skills)

    coverage = (
        len(matched) / len(job_skills) * 100
        if job_skills else None
    )

    similarity = calculate_similarity(
        resume_text, job_text
    )

    overall_score = (
        round(0.8 * coverage + 0.2 * similarity, 2)
        if coverage is not None else None
    )

    return {
        "resume_skills": sorted(resume_skills),
        "job_skills": sorted(job_skills),
        "matched_skills": matched,
        "missing_skills": missing,
        "skill_coverage": (
            round(coverage, 2)
            if coverage is not None else None
        ),
        "text_similarity": similarity,
        "overall_score": overall_score,
    }
import pytest

from analyzer import analyze_resume, find_skills


def test_skill_detection():
    skills = find_skills(
        "I develop applications using Python, Flask, SQL, and Git."
    )

    assert {"python", "flask", "sql", "git"}.issubset(set(skills))


def test_skill_aliases():
    skills = find_skills(
        "Experience with JavaScript, React.js, and PostgreSQL."
    )

    assert "javascript" in skills
    assert "react" in skills
    assert "postgresql" in skills


def test_matched_skills():
    result = analyze_resume(
        "Python Flask SQL",
        "Python developer with Flask and SQL experience."
    )

    assert result["matched_skills"] == ["flask", "python", "sql"]
    assert result["missing_skills"] == []


def test_missing_skills():
    result = analyze_resume(
        "Python and Flask",
        "Python, Flask, SQL, and Docker are required."
    )

    assert "sql" in result["missing_skills"]
    assert "docker" in result["missing_skills"]


def test_skill_coverage():
    result = analyze_resume(
        "Python Flask SQL",
        "Python Flask SQL Docker"
    )

    assert result["skill_coverage"] == 75.0


def test_empty_input_is_rejected():
    with pytest.raises(ValueError):
        analyze_resume("", "Python developer")


def test_job_without_recognized_skills():
    result = analyze_resume(
        "I enjoy learning and teamwork.",
        "We seek a motivated and curious candidate."
    )

    assert result["skill_coverage"] is None
    assert result["overall_score"] is None
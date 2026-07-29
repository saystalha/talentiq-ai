"""Tests for JobParser service."""
from app.services.job_parser import JobParser


class TestJobParser:
    """Test suite for job description parsing functionality."""

    def test_parse_extracts_title_with_prefix(self):
        """Title should be extracted from 'Position:' prefix."""
        text = "Position: Senior Python Developer\nRequirements: Python, Docker"
        result = JobParser.parse(text)
        assert result["title"] == "Senior Python Developer"

    def test_parse_extracts_title_with_role_prefix(self):
        """Title should be extracted from 'Role:' prefix."""
        text = "Role: Backend Engineer\nSkills: Python, FastAPI"
        result = JobParser.parse(text)
        assert result["title"] == "Backend Engineer"

    def test_parse_fallback_title_first_line(self):
        """If no prefix found, first non-empty line should be used as title."""
        text = "Data Scientist\nWe need someone with ML experience."
        result = JobParser.parse(text)
        assert result["title"] == "Data Scientist"

    def test_parse_extracts_skills(self, sample_job_description):
        """Known skills should be detected from the job text."""
        result = JobParser.parse(sample_job_description)
        skills = result["skills"]
        assert "Python" in skills
        assert "FastAPI" in skills
        assert "Docker" in skills

    def test_parse_extracts_experience(self, sample_job_description):
        """Experience requirement should be extracted."""
        result = JobParser.parse(sample_job_description)
        assert result["experience"] is not None
        assert "2" in result["experience"]

    def test_parse_extracts_experience_pattern(self):
        """Various experience patterns should be recognized."""
        text = "Title: Dev\nRequires 5+ years of experience in backend."
        result = JobParser.parse(text)
        assert result["experience"] is not None
        assert "5" in result["experience"]

    def test_parse_extracts_education(self, sample_job_description):
        """Education requirement should be extracted."""
        result = JobParser.parse(sample_job_description)
        assert result["education"] is not None
        assert "BS" in result["education"] or "Computer Science" in result["education"]

    def test_parse_extracts_education_masters(self):
        """Master's degree should be recognized."""
        text = "Title: ML Engineer\nEducation: Master's degree in AI or related field"
        result = JobParser.parse(text)
        assert result["education"] is not None
        assert "Master" in result["education"]

    def test_parse_empty_text(self):
        """Empty text should return defaults without crashing."""
        result = JobParser.parse("")
        assert result["title"] is None
        assert result["skills"] == [] or result["skills"] == list(result["skills"])
        assert result["experience"] is None
        assert result["education"] is None

    def test_parse_returns_all_keys(self, sample_job_description):
        """Result should always contain all expected keys."""
        result = JobParser.parse(sample_job_description)
        assert "title" in result
        assert "skills" in result
        assert "experience" in result
        assert "education" in result

"""Tests for ResumeParser service."""
from app.services.resume_parser import ResumeParser


class TestResumeParser:
    """Test suite for resume parsing functionality."""

    def test_parse_extracts_name(self, sample_resume_text):
        """First non-empty line should be extracted as name."""
        result = ResumeParser.parse(sample_resume_text)
        assert result["name"] == "John Doe"

    def test_parse_extracts_email(self, sample_resume_text):
        """Email address should be correctly extracted."""
        result = ResumeParser.parse(sample_resume_text)
        assert result["email"] == "john.doe@example.com"

    def test_parse_extracts_phone(self, sample_resume_text):
        """Phone number should be correctly extracted."""
        result = ResumeParser.parse(sample_resume_text)
        assert result["phone"] is not None
        assert "555" in result["phone"]

    def test_parse_extracts_skills(self, sample_resume_text):
        """Known skills should be detected from the text."""
        result = ResumeParser.parse(sample_resume_text)
        skills = result["skills"]
        assert "Python" in skills
        assert "FastAPI" in skills
        assert "Docker" in skills
        assert "Git" in skills

    def test_parse_skills_are_sorted(self, sample_resume_text):
        """Skills list should be sorted alphabetically."""
        result = ResumeParser.parse(sample_resume_text)
        skills = result["skills"]
        assert skills == sorted(skills)

    def test_parse_empty_text(self):
        """Empty text should return defaults without crashing."""
        result = ResumeParser.parse("")
        assert result["name"] is None
        assert result["email"] is None
        assert result["phone"] is None
        assert result["skills"] == []

    def test_parse_text_with_only_email(self):
        """Text with only email should extract it correctly."""
        result = ResumeParser.parse("Contact me at test@mail.com for details.")
        assert result["email"] == "test@mail.com"

    def test_parse_no_duplicate_skills(self, sample_resume_text):
        """Skills list should contain no duplicates."""
        result = ResumeParser.parse(sample_resume_text)
        skills = result["skills"]
        assert len(skills) == len(set(skills))

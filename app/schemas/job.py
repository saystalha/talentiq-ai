from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

class JobProfile(BaseModel):
    """Extracted job description details."""
    title: Optional[str] = None
    skills: List[str] = []
    experience: Optional[str] = None
    education: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Senior Python Engineer",
                "skills": ["Python", "Docker", "AWS"],
                "experience": "5+ years",
                "education": "Bachelor's degree"
            }
        }
    )

class JobParseRequest(BaseModel):
    """Request payload for parsing a job description."""
    text: str = Field(..., min_length=10, description="The job description text to parse.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "Role: Senior Python Engineer\nWe are looking for someone with 5+ years of experience.\nRequirements: Python, Docker, AWS.\nEducation: Bachelor's degree in CS."
            }
        }
    )

class JobParseResponse(BaseModel):
    """Response payload for job parsing."""
    job: JobProfile
    characters: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "job": {
                    "title": "Senior Python Engineer",
                    "skills": ["Python", "Docker", "AWS"],
                    "experience": "5+ years",
                    "education": "Bachelor's degree"
                },
                "characters": 150
            }
        }
    )

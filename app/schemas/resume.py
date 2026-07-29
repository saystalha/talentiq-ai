from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class CandidateProfile(BaseModel):
    """Profile details of a candidate parsed from a resume."""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = []

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1-555-123-4567",
                "skills": ["Python", "FastAPI", "SQL"]
            }
        }
    )

class ResumeUploadResponse(BaseModel):
    """Response returned upon successful resume upload and parsing."""
    filename: str
    saved_as: str
    characters: int
    candidate: CandidateProfile

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "filename": "john_doe_resume.pdf",
                "saved_as": "123e4567-e89b-12d3-a456-426614174000.pdf",
                "characters": 3500,
                "candidate": {
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "phone": "+1-555-123-4567",
                    "skills": ["Python", "FastAPI", "SQL"]
                }
            }
        }
    )

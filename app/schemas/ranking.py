from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any

class MatchScore(BaseModel):
    """Scores for various matching criteria."""
    skill_match: float
    semantic_similarity: float
    experience_score: float
    education_score: float
    overall_score: float

class SkillAnalysis(BaseModel):
    """Analysis of matched and missing skills."""
    matched_skills: List[str]
    missing_skills: List[str]
    match_percentage: float

class WhyCandidateExplanation(BaseModel):
    """Recruiter-friendly explainable AI reasoning."""
    summary: str
    highlights: List[str]
    missing_points: List[str]

class CandidateRanking(BaseModel):
    """Ranking details for a candidate."""
    candidate_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    scores: MatchScore
    skill_analysis: SkillAnalysis
    explanation: WhyCandidateExplanation
    experience_found: Optional[str] = None
    education_found: Optional[str] = None
    rank: int

class MatchRequest(BaseModel):
    """Request payload to match a resume against a job description."""
    resume_text: str = Field(..., min_length=10)
    job_description: str = Field(..., min_length=10)

class RankRequest(BaseModel):
    """Request payload to rank multiple resumes against a job description."""
    resume_texts: List[str] = Field(..., min_length=1)
    job_description: str = Field(..., min_length=10)

class MatchResponse(BaseModel):
    """Response containing match details for a single candidate."""
    candidate: CandidateRanking

class RankingResponse(BaseModel):
    """Response containing rankings for multiple candidates."""
    job_title: Optional[str] = None
    required_skills: List[str] = []
    experience_required: Optional[str] = None
    education_required: Optional[str] = None
    total_candidates: int
    rankings: List[CandidateRanking]

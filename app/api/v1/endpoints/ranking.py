from fastapi import APIRouter, HTTPException
from app.schemas.ranking import MatchRequest, MatchResponse, RankRequest, RankingResponse
from app.services.ranking_service import RankingService
from app.core.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.post("/match", response_model=MatchResponse, summary="Match Single Candidate")
async def match_candidate(request: MatchRequest):
    """
    Match a single candidate's resume against a job description and return a detailed score breakdown.
    """
    try:
        logger.info("Processing match request")
        result = RankingService.rank_candidate(request.resume_text, request.job_description)
        return {"candidate": result}
    except Exception as e:
        logger.error(f"Error matching candidate: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while matching candidate")

@router.post("/rank", response_model=RankingResponse, summary="Rank Multiple Candidates")
async def rank_candidates(request: RankRequest):
    """
    Rank multiple candidate resumes against a job description.
    """
    try:
        logger.info("Processing rank request")
        result = RankingService.rank_candidates(request.resume_texts, request.job_description)
        return result
    except Exception as e:
        logger.error(f"Error ranking candidates: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while ranking candidates")

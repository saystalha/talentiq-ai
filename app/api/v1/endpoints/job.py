from fastapi import APIRouter
from app.schemas.job import JobParseRequest, JobParseResponse
from app.services.job_parser import JobParser
from app.core.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.post(
    "/parse",
    summary="Parse Job Description",
    description="Parses a provided job description text to extract the title, required skills, experience, and education.",
    response_model=JobParseResponse
)
async def parse_job(request: JobParseRequest):
    """
    Endpoint to parse a job description text.
    """
    logger.info("Received request to parse job description")
    
    text_length = len(request.text)
    job_profile_data = JobParser.parse(request.text)
    
    response = JobParseResponse(
        job=job_profile_data,
        characters=text_length
    )
    
    logger.info("Successfully processed job description")
    return response

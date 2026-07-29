import os
import uuid
from typing import List
from fastapi import APIRouter, File, UploadFile, HTTPException

from app.services.pdf_service import PDFService
from app.services.resume_parser import ResumeParser
from app.schemas.resume import ResumeUploadResponse
from app.core.config import settings
from app.core.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)


@router.post(
    "/upload-resume",
    summary="Upload & Parse Single Resume",
    description="Upload a single PDF resume file.",
    response_model=ResumeUploadResponse,
)
async def upload_resume(
    file: UploadFile = File(..., description="The PDF resume file to upload and parse"),
):
    logger.info(f"Received resume upload request: {file.filename}")
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided.")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    unique_name = f"{uuid.uuid4()}.pdf"
    file_path = os.path.join(settings.UPLOAD_FOLDER, unique_name)

    try:
        contents = await file.read()
        with open(file_path, "wb") as buffer:
            buffer.write(contents)
    except Exception as e:
        logger.error(f"Failed to save file: {e}")
        raise HTTPException(status_code=500, detail="Failed to save the uploaded file.")

    try:
        extracted_text = PDFService.extract_text(file_path)
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=422, detail="Failed to extract text from PDF.")

    parsed_resume = ResumeParser.parse(extracted_text)

    return ResumeUploadResponse(
        filename=file.filename,
        saved_as=unique_name,
        characters=len(extracted_text),
        candidate=parsed_resume,
    )


@router.post(
    "/batch-upload",
    summary="Batch Upload & Parse PDF Resumes",
    description="Upload multiple PDF resumes in one request for multi-candidate processing.",
)
async def batch_upload_resumes(
    files: List[UploadFile] = File(..., description="List of PDF resume files"),
):
    logger.info(f"Received batch upload request with {len(files)} file(s).")
    
    results = []
    for file in files:
        if not file.filename or not file.filename.lower().endswith(".pdf"):
            continue

        unique_name = f"{uuid.uuid4()}.pdf"
        file_path = os.path.join(settings.UPLOAD_FOLDER, unique_name)

        try:
            contents = await file.read()
            with open(file_path, "wb") as buffer:
                buffer.write(contents)
                
            extracted_text = PDFService.extract_text(file_path)
            parsed_resume = ResumeParser.parse(extracted_text)
            
            results.append({
                "filename": file.filename,
                "saved_as": unique_name,
                "extracted_text": extracted_text,
                "candidate": parsed_resume
            })
        except Exception as e:
            logger.error(f"Error processing {file.filename}: {e}")

    if not results:
        raise HTTPException(status_code=400, detail="No valid PDF resumes could be processed.")

    return {
        "total_processed": len(results),
        "resumes": results
    }
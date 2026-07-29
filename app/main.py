from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.api.v1.endpoints.resume import router as resume_router
from app.api.v1.endpoints.job import router as job_router
from app.api.v1.endpoints.ranking import router as ranking_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "🚀 **TalentIQ AI** — AI-Powered Resume Ranking System\n\n"
        "Upload PDF resumes, parse job descriptions, extract candidate information, "
        "and rank applicants intelligently using hybrid AI scoring.\n\n"
        "---\n\n"
        "### Features\n"
        "- 📄 **PDF Upload & Text Extraction** — Parse resumes from PDF files\n"
        "- 🧠 **Smart Resume Parsing** — Auto-detect name, email, phone & skills\n"
        "- 📋 **Job Description Parsing** — Extract title, skills, experience & education\n"
        "- 🏆 **AI-Powered Ranking** — Score & rank candidates with hybrid scoring\n"
        "- 🔗 **Semantic Embeddings** — Sentence Transformer-based matching\n\n"
        "---\n\n"
        "### Scoring Formula\n"
        "```\n"
        "40%  → Skill Match\n"
        "40%  → Semantic Similarity\n"
        "10%  → Experience Match\n"
        "10%  → Education Match\n"
        "───────────────────────\n"
        "100% → Overall Score\n"
        "```\n\n"
        "---\n\n"
        "### Quick Start\n"
        "1. Upload a PDF resume via `/api/v1/resume/upload-resume`\n"
        "2. Parse a job description via `/api/v1/jobs/parse`\n"
        "3. Match & rank candidates via `/api/v1/ranking/rank`\n"
    ),
    contact={
        "name": "TalentIQ AI Team",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# ---------- CORS Middleware ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Custom OpenAPI Schema ----------
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        contact=app.contact,
        license_info=app.license_info,
    )

    # Add custom logo and styling info
    openapi_schema["info"]["x-logo"] = {
        "url": "https://img.icons8.com/fluency/96/artificial-intelligence.png",
        "altText": "TalentIQ AI Logo",
    }

    # Tag descriptions for better docs organization
    openapi_schema["tags"] = [
        {
            "name": "Health",
            "description": "🩺 System health and status checks.",
        },
        {
            "name": "Resume",
            "description": "📄 Resume upload, parsing, and candidate extraction endpoints.",
        },
        {
            "name": "Jobs",
            "description": "📋 Job description parsing and structured extraction endpoints.",
        },
        {
            "name": "Ranking",
            "description": "🏆 AI-powered candidate matching and ranking endpoints.",
        },
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# ---------- Health / Root Endpoints ----------
@app.get(
    "/",
    tags=["Health"],
    summary="Welcome",
    description="Returns a welcome message confirming the API is running.",
    response_description="Welcome message",
)
def home():
    return {
        "message": "🚀 Welcome to TalentIQ AI — AI-Powered Resume Ranking System",
        "docs": "/docs",
        "version": app.version,
    }


@app.get(
    "/health",
    tags=["Health"],
    summary="Health Check",
    description="Returns the current health status of the TalentIQ AI service.",
    response_description="Health status object",
)
def health():
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


# ---------- Include Routers ----------
app.include_router(
    resume_router,
    prefix="/api/v1/resume",
    tags=["Resume"],
)

app.include_router(
    job_router,
    prefix="/api/v1/jobs",
    tags=["Jobs"],
)

app.include_router(
    ranking_router,
    prefix="/api/v1/ranking",
    tags=["Ranking"],
)
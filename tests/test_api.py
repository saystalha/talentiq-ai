"""Tests for API endpoints."""


class TestHealthEndpoints:
    """Test health and root endpoints."""

    def test_home_endpoint(self, client):
        """Root endpoint should return welcome message."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "TalentIQ" in data["message"]

    def test_health_endpoint(self, client):
        """Health endpoint should return healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_docs_available(self, client):
        """Swagger docs should be accessible."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_openapi_schema(self, client):
        """OpenAPI schema should be accessible and valid."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert data["info"]["title"] == "TalentIQ AI"
        assert "tags" in data


class TestResumeEndpoint:
    """Test resume upload endpoint."""

    def test_upload_non_pdf_rejected(self, client):
        """Non-PDF files should be rejected with 400."""
        response = client.post(
            "/api/v1/resume/upload-resume",
            files={"file": ("test.txt", b"Some text content", "text/plain")},
        )
        assert response.status_code == 400
        assert "PDF" in response.json()["detail"]

    def test_upload_no_file_returns_422(self, client):
        """Request without file should return 422 validation error."""
        response = client.post("/api/v1/resume/upload-resume")
        assert response.status_code == 422


class TestJobEndpoint:
    """Test job description parsing endpoint."""

    def test_parse_job_success(self, client, sample_job_description):
        """Valid job description should be parsed successfully."""
        response = client.post(
            "/api/v1/jobs/parse",
            json={"text": sample_job_description},
        )
        assert response.status_code == 200
        data = response.json()
        assert "job" in data
        assert "characters" in data
        assert data["job"]["title"] is not None
        assert len(data["job"]["skills"]) > 0

    def test_parse_job_extracts_skills(self, client):
        """Job parsing should detect known skills."""
        response = client.post(
            "/api/v1/jobs/parse",
            json={
                "text": "Position: Backend Dev\nRequirements: Python, FastAPI, Docker, PostgreSQL\nExperience: 3+ years"
            },
        )
        assert response.status_code == 200
        skills = response.json()["job"]["skills"]
        assert "Python" in skills
        assert "FastAPI" in skills

    def test_parse_job_too_short_rejected(self, client):
        """Text shorter than min_length should be rejected."""
        response = client.post(
            "/api/v1/jobs/parse",
            json={"text": "short"},
        )
        assert response.status_code == 422

    def test_parse_job_empty_body_rejected(self, client):
        """Empty request body should be rejected."""
        response = client.post("/api/v1/jobs/parse", json={})
        assert response.status_code == 422


class TestRankingEndpoints:
    """Test ranking endpoints."""

    def test_match_endpoint_success(self, client, sample_resume_text, sample_job_description):
        """Match endpoint should return scores for a single candidate."""
        response = client.post(
            "/api/v1/ranking/match",
            json={
                "resume_text": sample_resume_text,
                "job_description": sample_job_description,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "candidate" in data
        candidate = data["candidate"]
        assert "scores" in candidate
        assert "skill_analysis" in candidate
        assert 0 <= candidate["scores"]["overall_score"] <= 1

    def test_match_endpoint_has_skill_analysis(self, client, sample_resume_text, sample_job_description):
        """Match should include matched and missing skills."""
        response = client.post(
            "/api/v1/ranking/match",
            json={
                "resume_text": sample_resume_text,
                "job_description": sample_job_description,
            },
        )
        data = response.json()
        skill_analysis = data["candidate"]["skill_analysis"]
        assert "matched_skills" in skill_analysis
        assert "missing_skills" in skill_analysis
        assert "match_percentage" in skill_analysis

    def test_rank_endpoint_success(self, client, sample_resume_text, sample_resume_text_weak, sample_job_description):
        """Rank endpoint should return sorted candidates."""
        response = client.post(
            "/api/v1/ranking/rank",
            json={
                "resume_texts": [sample_resume_text, sample_resume_text_weak],
                "job_description": sample_job_description,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "rankings" in data
        assert data["total_candidates"] == 2
        assert data["rankings"][0]["rank"] == 1
        assert data["rankings"][1]["rank"] == 2
        # The stronger candidate should rank higher
        assert data["rankings"][0]["scores"]["overall_score"] >= data["rankings"][1]["scores"]["overall_score"]

    def test_rank_endpoint_validates_input(self, client):
        """Rank endpoint should reject short input text."""
        response = client.post(
            "/api/v1/ranking/rank",
            json={
                "resume_texts": ["short"],
                "job_description": "too short",
            },
        )
        assert response.status_code == 422

    def test_match_endpoint_validates_input(self, client):
        """Match endpoint should reject empty body."""
        response = client.post("/api/v1/ranking/match", json={})
        assert response.status_code == 422

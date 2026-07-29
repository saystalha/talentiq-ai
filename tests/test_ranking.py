"""Tests for RankingService and EmbeddingService."""
from app.services.ranking_service import RankingService
from app.services.embedding_service import EmbeddingService


class TestEmbeddingService:
    """Test embedding and similarity computation."""

    def test_compute_similarity_related_texts(self):
        """Semantically similar texts should have high similarity."""
        score = EmbeddingService.compute_similarity(
            "Built RESTful web services using FastAPI and Python",
            "Developed backend APIs with Python frameworks",
        )
        assert score > 0.5

    def test_compute_similarity_unrelated_texts(self):
        """Unrelated texts should have low similarity."""
        score = EmbeddingService.compute_similarity(
            "Python backend developer with API experience",
            "Professional chef specializing in French cuisine",
        )
        assert score < 0.5

    def test_compute_similarity_identical_texts(self):
        """Identical texts should have near-perfect similarity."""
        text = "Python developer with FastAPI experience"
        score = EmbeddingService.compute_similarity(text, text)
        assert score > 0.99

    def test_compute_similarity_empty_text(self):
        """Empty text should return 0.0."""
        score = EmbeddingService.compute_similarity("", "Some text here")
        assert score == 0.0

    def test_get_embedding_returns_list(self):
        """Embedding should return a list of floats."""
        embedding = EmbeddingService.get_embedding("Hello world")
        assert isinstance(embedding, list)
        assert len(embedding) > 0
        assert all(isinstance(v, float) for v in embedding)

    def test_get_embedding_empty_text(self):
        """Empty text should return empty list."""
        embedding = EmbeddingService.get_embedding("")
        assert embedding == []


class TestRankingService:
    """Test candidate ranking logic."""

    def test_skill_match_all_matched(self):
        """Candidate with all required skills should score 1.0."""
        score, matched, missing = RankingService._compute_skill_match(
            ["Python", "FastAPI", "Docker"],
            ["Python", "FastAPI", "Docker"],
        )
        assert score == 1.0
        assert len(missing) == 0

    def test_skill_match_partial(self):
        """Partial skill match should return correct percentage."""
        score, matched, missing = RankingService._compute_skill_match(
            ["Python", "FastAPI"],
            ["Python", "FastAPI", "Docker", "PostgreSQL"],
        )
        assert score == 0.5
        assert len(matched) == 2
        assert len(missing) == 2

    def test_skill_match_no_job_skills(self):
        """No required skills should return 1.0 (no requirements)."""
        score, matched, missing = RankingService._compute_skill_match(
            ["Python"], []
        )
        assert score == 1.0

    def test_skill_match_case_insensitive(self):
        """Skill matching should be case insensitive."""
        score, matched, missing = RankingService._compute_skill_match(
            ["python", "FASTAPI"],
            ["Python", "FastAPI"],
        )
        assert score == 1.0

    def test_experience_score_exceeds_requirement(self):
        """Candidate exceeding experience requirement should score 1.0."""
        score = RankingService._compute_experience_score("5+ years", "2+ years")
        assert score == 1.0

    def test_experience_score_below_requirement(self):
        """Candidate below experience requirement should score < 1.0."""
        score = RankingService._compute_experience_score("1 year", "3+ years")
        assert 0 < score < 1.0

    def test_experience_score_no_data(self):
        """No experience data should return neutral 0.5."""
        score = RankingService._compute_experience_score(None, None)
        assert score == 0.5

    def test_education_score_meets_requirement(self):
        """Matching education level should score 1.0."""
        score = RankingService._compute_education_score(
            "BS Computer Science", "BS Computer Science"
        )
        assert score == 1.0

    def test_education_score_exceeds_requirement(self):
        """Higher education than required should score 1.0."""
        score = RankingService._compute_education_score(
            "Master's in CS", "Bachelor's degree"
        )
        assert score == 1.0

    def test_education_score_below_requirement(self):
        """Lower education than required should score < 1.0."""
        score = RankingService._compute_education_score(
            "BS in CS", "PhD in CS"
        )
        assert 0 < score < 1.0

    def test_education_score_no_data(self):
        """No education data should return neutral 0.5."""
        score = RankingService._compute_education_score(None, None)
        assert score == 0.5

    def test_rank_candidate_returns_all_fields(self, sample_resume_text, sample_job_description):
        """Ranking result should contain all required fields."""
        result = RankingService.rank_candidate(sample_resume_text, sample_job_description)
        assert "candidate_name" in result
        assert "scores" in result
        assert "skill_analysis" in result
        assert "rank" in result
        scores = result["scores"]
        assert "skill_match" in scores
        assert "semantic_similarity" in scores
        assert "experience_score" in scores
        assert "education_score" in scores
        assert "overall_score" in scores

    def test_rank_candidate_scores_in_range(self, sample_resume_text, sample_job_description):
        """All scores should be between 0 and 1."""
        result = RankingService.rank_candidate(sample_resume_text, sample_job_description)
        scores = result["scores"]
        for key, value in scores.items():
            assert 0 <= value <= 1, f"{key} = {value} is out of range"

    def test_rank_candidates_ordering(
        self, sample_resume_text, sample_resume_text_weak, sample_job_description
    ):
        """Candidates should be ranked from best to worst."""
        result = RankingService.rank_candidates(
            [sample_resume_text, sample_resume_text_weak],
            sample_job_description,
        )
        rankings = result["rankings"]
        assert len(rankings) == 2
        assert rankings[0]["rank"] == 1
        assert rankings[1]["rank"] == 2
        assert rankings[0]["scores"]["overall_score"] >= rankings[1]["scores"]["overall_score"]

    def test_rank_candidates_returns_job_title(self, sample_resume_text, sample_job_description):
        """Ranking result should include the parsed job title."""
        result = RankingService.rank_candidates(
            [sample_resume_text], sample_job_description
        )
        assert "job_title" in result
        assert result["job_title"] is not None
        assert result["total_candidates"] == 1

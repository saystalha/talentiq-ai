import re
from typing import Any, Dict, List, Tuple
from app.services.embedding_service import EmbeddingService
from app.services.resume_parser import ResumeParser
from app.services.job_parser import JobParser
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

class RankingService:
    """Service for ranking candidates against job descriptions with explainable AI reasoning."""

    @staticmethod
    def _compute_skill_match(candidate_skills: list[str], job_skills: list[str]) -> tuple[float, list[str], list[str]]:
        """Compute the skill match percentage and identify matched/missing skills."""
        if not job_skills:
            return 1.0, candidate_skills, []
            
        job_skills_map = {s.lower(): s for s in job_skills}
        cand_skills_map = {s.lower(): s for s in candidate_skills}
        
        matched_keys = set(job_skills_map.keys()).intersection(set(cand_skills_map.keys()))
        missing_keys = set(job_skills_map.keys()).difference(set(cand_skills_map.keys()))
        
        matched = [job_skills_map[k] for k in matched_keys]
        missing = [job_skills_map[k] for k in missing_keys]
        
        match_percentage = len(matched) / len(job_skills) if job_skills else 1.0
        
        return float(match_percentage), matched, missing

    @staticmethod
    def _compute_experience_score(candidate_exp: str | None, job_exp: str | None) -> float:
        """Compute experience score based on numeric comparison."""
        def extract_years(exp_str: str | None) -> float | None:
            if not exp_str:
                return None
            matches = re.findall(r'(\d+(?:\.\d+)?)', exp_str)
            if matches:
                return float(matches[0])
            return None
            
        cand_years = extract_years(candidate_exp)
        job_years = extract_years(job_exp)
        
        if job_years is None and cand_years is None:
            return 0.5
        if job_years is None:
            return 1.0
        if cand_years is None:
            return 0.5
            
        if cand_years >= job_years:
            return 1.0
            
        if job_years > 0:
            return float(cand_years / job_years)
            
        return 1.0

    @staticmethod
    def _compute_education_score(candidate_edu: str | None, job_edu: str | None) -> float:
        """Compute education score based on normalized level comparison."""
        levels = {
            "phd": 4, "doctorate": 4, 
            "master": 3, "ms": 3, 
            "bachelor": 2, "bs": 2, 
            "associate": 1
        }
        
        def extract_level(edu_str: str | None) -> int | None:
            if not edu_str:
                return None
            edu_lower = edu_str.lower()
            for key, val in levels.items():
                if key in edu_lower:
                    return val
            return None
            
        cand_level = extract_level(candidate_edu)
        job_level = extract_level(job_edu)
        
        if job_level is None and cand_level is None:
            return 0.5
        if job_level is None:
            return 1.0
        if cand_level is None:
            return 0.5
            
        if cand_level >= job_level:
            return 1.0
            
        if job_level > 0:
            return float(cand_level / job_level)
            
        return 1.0

    @staticmethod
    def generate_explanation(
        cand_name: str,
        skill_pct: float,
        matched_skills: list[str],
        missing_skills: list[str],
        semantic_sim: float,
        exp_score: float,
        cand_exp: str | None,
        job_exp: str | None,
        edu_score: float,
        cand_edu: str | None,
        job_edu: str | None,
        overall_score: float
    ) -> dict[str, Any]:
        """Generate human-readable explainable AI insights."""
        overall_pct = round(overall_score * 100)
        summary = f"{cand_name} achieved an overall match score of {overall_pct}%."
        
        highlights = []
        missing_points = []
        
        # Skill insights
        if matched_skills:
            highlights.append(f"✓ Skill Match: {len(matched_skills)} required skill(s) matched ({', '.join(matched_skills)}).")
        else:
            missing_points.append("✗ Skill Match: No exact matching skills identified from requirements.")
            
        if missing_skills:
            missing_points.append(f"Missing required skill(s): {', '.join(missing_skills)}.")
            
        # Semantic similarity insight
        sem_pct = round(semantic_sim * 100)
        if sem_pct >= 75:
            highlights.append(f"✓ Semantic AI Match: Highly relevant background & role experience ({sem_pct}% conceptual alignment).")
        elif sem_pct >= 50:
            highlights.append(f"✓ Semantic AI Match: Moderate conceptual alignment ({sem_pct}%).")
        else:
            missing_points.append(f"✗ Semantic AI Match: Lower alignment with role description details ({sem_pct}%).")
            
        # Experience insight
        if exp_score >= 1.0 and job_exp:
            highlights.append(f"✓ Experience: Meets or exceeds requirements ({cand_exp or 'Experienced'} vs. {job_exp} required).")
        elif cand_exp:
            missing_points.append(f"Experience: Partially meets requirement ({cand_exp} vs. {job_exp or 'Not specified'} required).")
        else:
            highlights.append("Experience: Standard evaluation applied.")
            
        # Education insight
        if edu_score >= 1.0 and job_edu:
            highlights.append(f"✓ Education: Qualifications align with required background ({cand_edu or 'Degree'} vs. {job_edu}).")
        elif cand_edu:
            missing_points.append(f"Education: Background noted ({cand_edu}).")
            
        return {
            "summary": summary,
            "highlights": highlights,
            "missing_points": missing_points
        }

    @staticmethod
    def rank_candidate(resume_text: str, job_description: str) -> dict[str, Any]:
        """Rank a single candidate against a job description."""
        logger.info("Ranking single candidate")
        
        cand_profile = ResumeParser.parse(resume_text)
        job_profile = JobParser.parse(job_description)
        
        cand_name = cand_profile.get("name") or "Candidate"
        
        skill_match_pct, matched, missing = RankingService._compute_skill_match(
            cand_profile.get("skills", []), 
            job_profile.get("skills", [])
        )
        
        semantic_sim = EmbeddingService.compute_similarity(resume_text, job_description)
        
        exp_score = RankingService._compute_experience_score(
            cand_profile.get("experience"),
            job_profile.get("experience")
        )
        
        edu_score = RankingService._compute_education_score(
            cand_profile.get("education"),
            job_profile.get("education")
        )
        
        overall = (
            skill_match_pct * settings.SKILL_MATCH_WEIGHT +
            semantic_sim * settings.SEMANTIC_WEIGHT +
            exp_score * settings.EXPERIENCE_WEIGHT +
            edu_score * settings.EDUCATION_WEIGHT
        )
        
        explanation = RankingService.generate_explanation(
            cand_name=cand_name,
            skill_pct=skill_match_pct,
            matched_skills=matched,
            missing_skills=missing,
            semantic_sim=semantic_sim,
            exp_score=exp_score,
            cand_exp=cand_profile.get("experience"),
            job_exp=job_profile.get("experience"),
            edu_score=edu_score,
            cand_edu=cand_profile.get("education"),
            job_edu=job_profile.get("education"),
            overall_score=overall
        )
        
        return {
            "candidate_name": cand_name,
            "email": cand_profile.get("email"),
            "phone": cand_profile.get("phone"),
            "scores": {
                "skill_match": round(skill_match_pct, 4),
                "semantic_similarity": round(semantic_sim, 4),
                "experience_score": round(exp_score, 4),
                "education_score": round(edu_score, 4),
                "overall_score": round(overall, 4)
            },
            "skill_analysis": {
                "matched_skills": matched,
                "missing_skills": missing,
                "match_percentage": round(skill_match_pct, 4)
            },
            "explanation": explanation,
            "experience_found": cand_profile.get("experience"),
            "education_found": cand_profile.get("education"),
            "rank": 0
        }

    @staticmethod
    def rank_candidates(resume_texts: list[str], job_description: str) -> dict[str, Any]:
        """Rank multiple candidates against a job description."""
        logger.info(f"Ranking {len(resume_texts)} candidates")
        
        job_profile = JobParser.parse(job_description)
        job_title = job_profile.get("title") or "Position"
        
        rankings = []
        for text in resume_texts:
            result = RankingService.rank_candidate(text, job_description)
            rankings.append(result)
            
        rankings.sort(key=lambda x: x["scores"]["overall_score"], reverse=True)
        
        for i, ranking in enumerate(rankings):
            ranking["rank"] = i + 1
            
        return {
            "job_title": job_title,
            "required_skills": job_profile.get("skills", []),
            "experience_required": job_profile.get("experience"),
            "education_required": job_profile.get("education"),
            "total_candidates": len(rankings),
            "rankings": rankings
        }

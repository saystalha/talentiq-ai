import re
from typing import Dict, Any, List
from app.utils.skills import SKILLS
from app.core.logger import get_logger

logger = get_logger(__name__)

class JobParser:
    """Service class for parsing job descriptions."""

    @staticmethod
    def parse(text: str) -> Dict[str, Any]:
        """
        Parses a job description to extract title, skills, experience, and education.
        """
        logger.info("Starting job description parsing")
        
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        title = None
        
        # 1. Job Title Extraction
        title_patterns = [
            r"^(?:About\s+the\s+job|Position|Title|Role|Job\s+Title):\s*(.+)",
            r"^(.+?)\s+(?:Internship|Program|Role|Developer|Engineer|Manager|Specialist)"
        ]
        
        for line in lines:
            for pattern in title_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    title = match.group(1).strip()
                    break
            if title:
                break
                
        if not title and lines:
            title = lines[0]

        # 2. Skills & Key Concept Extraction
        text_lower = text.lower()
        extracted_skills = set()
        
        for skill in SKILLS:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                extracted_skills.add(skill)
                
        # Additional domain skill keywords
        extra_keywords = [
            "Communication", "Interpersonal Skills", "Project Management", 
            "Research", "Problem Solving", "Teamwork", "Adaptability"
        ]
        for kw in extra_keywords:
            if kw.lower() in text_lower:
                extracted_skills.add(kw)

        # 3. Experience Extraction
        experience = None
        if "no prior experience" in text_lower or "fresh" in text_lower or "internship" in text_lower:
            experience = "Fresh / Entry Level (No prior experience required)"
        else:
            exp_match = re.search(r"(\d+\+?\s*(?:-\s*\d+)?\s*years?(?:\s+of\s+experience)?)", text, re.IGNORECASE)
            if exp_match:
                experience = exp_match.group(1).strip()

        # 4. Education Extraction
        education = None
        edu_patterns = [
            r"\b(Bachelor'?s?|Master'?s?|BS|MS|PhD|Doctorate)\b(?:\s+(?:students?|graduates?|degree)?)?",
        ]
        found_edus = []
        for pattern in edu_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for m in matches:
                found_edus.append(m.group(0).strip())
                
        if found_edus:
            education = " / ".join(sorted(set(found_edus)))
        elif "final-year" in text_lower or "fresh graduate" in text_lower:
            education = "Bachelor's / Master's (Final-year student or Fresh graduate)"

        result = {
            "title": title or "General Role",
            "skills": list(extracted_skills),
            "experience": experience or "Not Specified",
            "education": education or "Not Specified"
        }
        
        logger.info(f"Finished job description parsing. Title: {result['title']}")
        return result

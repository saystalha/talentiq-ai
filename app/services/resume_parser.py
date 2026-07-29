import re

from app.utils.skills import SKILLS


class ResumeParser:

    @staticmethod
    def parse(text: str):

        result = {
            "name": None,
            "email": None,
            "phone": None,
            "skills": []
        }

        # ---------- Name ----------
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        if lines:
            result["name"] = lines[0]

        # ---------- Email ----------
        email = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text
        )

        if email:
            result["email"] = email.group()

        # ---------- Phone ----------
        phone = re.search(
            r"(\+?\d[\d\s\-]{8,}\d)",
            text
        )

        if phone:
            result["phone"] = phone.group()

        # ---------- Skills ----------
        text_lower = text.lower()

        found_skills = []

        for skill in SKILLS:

            if skill.lower() in text_lower:
                found_skills.append(skill)

        result["skills"] = sorted(set(found_skills))

        return result
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """FastAPI test client fixture."""
    return TestClient(app)


@pytest.fixture
def sample_resume_text():
    """Sample resume text for testing."""
    return """John Doe
john.doe@example.com
+1-555-123-4567

Summary:
Experienced Python backend developer with 4 years of experience
building scalable web applications.

Skills:
- Python
- FastAPI
- Django
- PostgreSQL
- Docker
- Git
- REST APIs

Experience:
Senior Backend Developer at TechCorp (2020-2024)
- Built microservices using Python and FastAPI
- Managed PostgreSQL databases
- Deployed applications using Docker and Kubernetes

Education:
BS Computer Science, MIT (2020)
"""


@pytest.fixture
def sample_job_description():
    """Sample job description text for testing."""
    return """Position: Python Backend Developer

We are looking for a Python Backend Developer to join our team.

Requirements:
• Python
• FastAPI
• PostgreSQL
• Docker
• REST APIs

Experience:
2+ years of backend development experience

Education:
BS Computer Science
"""


@pytest.fixture
def sample_resume_text_weak():
    """Sample resume text for a weaker candidate."""
    return """Jane Smith
jane.smith@example.com
+1-555-987-6543

Summary:
Junior frontend developer with 1 year of experience.

Skills:
- JavaScript
- React
- HTML
- CSS

Experience:
Junior Developer at WebCo (2023-2024)
- Built user interfaces using React
- Styled pages with CSS and Bootstrap

Education:
BS Information Technology, State University (2023)
"""

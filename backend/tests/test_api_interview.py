import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app


@pytest.mark.asyncio
async def test_interview_start_returns_session():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r1 = await client.post("/api/resume/upload", data={"text": "张三\nPython专家"})
        r2 = await client.post("/api/jd/upload", data={"text": "Python工程师"})
        resume_id = r1.json()["resume_id"]
        jd_id = r2.json()["jd_id"]
        resp = await client.post("/api/interview/start", json={"resume_id": resume_id, "jd_id": jd_id})
    assert resp.status_code == 200
    data = resp.json()
    assert "session_id" in data
    assert data["total_questions"] > 0

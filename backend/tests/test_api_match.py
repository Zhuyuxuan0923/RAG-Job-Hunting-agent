import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app


@pytest.mark.asyncio
async def test_upload_resume_text():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/resume/upload", data={"text": "张三\nPython 5年\nJava"})
    assert resp.status_code == 200
    data = resp.json()
    assert "resume_id" in data
    assert "张三" in data["parsed_text"]


@pytest.mark.asyncio
async def test_upload_jd_text():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/jd/upload", data={"text": "Python工程师\n要求5年经验"})
    assert resp.status_code == 200
    data = resp.json()
    assert "jd_id" in data


@pytest.mark.asyncio
async def test_match_returns_task_id():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r1 = await client.post("/api/resume/upload", data={"text": "张三\nPython专家"})
        r2 = await client.post("/api/jd/upload", data={"text": "Python工程师"})
        resume_id = r1.json()["resume_id"]
        jd_id = r2.json()["jd_id"]
        resp = await client.post("/api/match", json={"resume_id": resume_id, "jd_id": jd_id})
    assert resp.status_code == 200
    assert "task_id" in resp.json()


@pytest.mark.asyncio
async def test_health():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}

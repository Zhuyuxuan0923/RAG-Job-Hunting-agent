from src.services.chunker import chunk_resume, chunk_jd


def test_chunk_resume_splits_by_sections():
    text = "# 个人信息\n张三，5年经验\n# 技能\nPython, Java\n# 工作经历\n某公司工程师"
    chunks = chunk_resume(text)
    assert len(chunks) >= 3
    sections = [c["section"] for c in chunks]
    assert "个人信息" in sections
    assert "技能" in sections
    assert "工作经历" in sections


def test_chunk_resume_has_metadata():
    text = "# 技能\nPython\n"
    chunks = chunk_resume(text)
    assert chunks[0]["section"] == "技能"
    assert "chunk_index" in chunks[0]


def test_chunk_jd_preserves_content():
    text = "## 岗位职责\n负责系统架构设计，带领5人团队完成产品从0到1的研发。\n\n## 任职要求\n本科以上学历，5年以上Python经验。熟悉分布式系统。"
    chunks = chunk_jd(text)
    assert len(chunks) >= 1
    assert "系统架构设计" in chunks[0]["text"]


def test_chunk_jd_splits_long_text():
    long_paragraph = "开发高性能系统。使用微服务架构。" * 300
    chunks = chunk_jd("职责\n" + long_paragraph + "\n\n要求\n" + long_paragraph)
    assert len(chunks) > 1

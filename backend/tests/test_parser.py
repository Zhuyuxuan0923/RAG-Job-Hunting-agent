from src.services.parser import parse_text


def test_parse_text_extracts_content():
    text = "## 个人信息\n\n张三\n\n## 技能\n\nPython, Java"
    result = parse_text(text)
    assert "张三" in result
    assert "Python" in result


def test_parse_text_handles_empty():
    result = parse_text("")
    assert result == ""


def test_parse_text_strips_excess_whitespace():
    result = parse_text("  张三\n\n\n  Python  ")
    assert result == "张三\nPython"

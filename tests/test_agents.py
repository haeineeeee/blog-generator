import pytest

from app.agents.outline import generate_outline
from app.agents.reviewer import review_draft
from app.agents.writer import generate_draft


@pytest.mark.asyncio
async def test_generate_outline(mock_llm):
    mock_llm.return_value = "# 테스트 아웃라인\n## 소제목 1"
    result = await generate_outline("파이썬", None, "ko")
    assert "테스트 아웃라인" in result
    mock_llm.assert_called_once()


@pytest.mark.asyncio
async def test_generate_outline_with_tone(mock_llm):
    mock_llm.return_value = "# 친근한 아웃라인"
    result = await generate_outline("파이썬", "친근한", "ko")
    assert "친근한 아웃라인" in result
    mock_llm.assert_called_once()


@pytest.mark.asyncio
async def test_generate_draft(mock_llm):
    mock_llm.return_value = "블로그 본문 내용입니다."
    result = await generate_draft("파이썬", "# 아웃라인", None)
    assert "블로그 본문" in result
    mock_llm.assert_called_once()


@pytest.mark.asyncio
async def test_review_draft_with_feedback(mock_llm):
    mock_llm.return_value = "[수정된 글]\n수정된 내용\n[피드백]\n맞춤법을 수정했습니다."
    reviewed, feedback = await review_draft("파이썬", "원본 글")
    assert "수정된 내용" in reviewed
    assert "맞춤법" in feedback


@pytest.mark.asyncio
async def test_review_draft_without_feedback_marker(mock_llm):
    mock_llm.return_value = "수정된 전체 내용"
    reviewed, feedback = await review_draft("파이썬", "원본 글")
    assert "수정된 전체 내용" in reviewed
    assert "별도로 제공되지 않았습니다" in feedback

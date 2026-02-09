import pytest
from unittest.mock import AsyncMock, patch


def test_outline_endpoint(client, mock_llm):
    mock_llm.return_value = "# 아웃라인 결과"
    response = client.post("/generate/outline", json={"keyword": "파이썬"})
    assert response.status_code == 200
    data = response.json()
    assert data["keyword"] == "파이썬"
    assert "아웃라인 결과" in data["outline"]


def test_draft_endpoint(client, mock_llm):
    mock_llm.return_value = "블로그 본문입니다."
    response = client.post(
        "/generate/draft",
        json={"keyword": "파이썬", "outline": "# 아웃라인"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["keyword"] == "파이썬"
    assert "블로그 본문" in data["draft"]


def test_review_endpoint(client, mock_llm):
    mock_llm.return_value = "[수정된 글]\n개선된 글\n[피드백]\n가독성 개선"
    response = client.post(
        "/generate/review",
        json={"keyword": "파이썬", "draft": "원본 글"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "개선된 글" in data["reviewed"]
    assert "가독성" in data["feedback"]


def test_full_generate_endpoint(client, mock_llm):
    mock_llm.side_effect = [
        "# 아웃라인",
        "블로그 본문",
        "[수정된 글]\n최종 글\n[피드백]\n수정 완료",
    ]
    response = client.post("/generate/full", json={"keyword": "파이썬"})
    assert response.status_code == 200
    data = response.json()
    assert data["keyword"] == "파이썬"
    assert data["outline"] == "# 아웃라인"
    assert data["draft"] == "블로그 본문"
    assert "최종 글" in data["reviewed"]


def test_markdown_endpoint(client, tmp_path):
    with patch("app.services.markdown.settings") as mock_settings:
        mock_settings.output_dir = str(tmp_path)
        response = client.post(
            "/publish/markdown",
            json={"title": "테스트 글", "content": "내용입니다."},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "저장되었습니다" in data["message"]


def test_outline_validation_error(client):
    response = client.post("/generate/outline", json={})
    assert response.status_code == 422

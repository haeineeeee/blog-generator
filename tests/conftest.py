from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_llm():
    with patch("app.services.llm.llm_service.generate", new_callable=AsyncMock) as mock:
        yield mock

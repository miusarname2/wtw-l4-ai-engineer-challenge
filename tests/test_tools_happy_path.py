from types import SimpleNamespace

from src.config import Settings
from src import tools


class FakeResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return {"incident_id": "INC-1042", "status": "investigating"}


class FakeClient:
    def __init__(self):
        self.url = None
        self.headers = None

    def get(self, url, headers):
        self.url = url
        self.headers = headers
        return FakeResponse()


def _settings():
    return Settings(
        llm_provider="openai-compatible",
        llm_base_url="http://llm",
        llm_api_key="llm-key",
        llm_model="model",
        llm_api_version="",
        llm_timeout_seconds=30,
        llm_max_agent_steps=6,
        mock_api_base_url="https://mock.example",
        mock_api_key="test-key",
        knowledge_top_k=4,
    )


def test_incident_tool_calls_documented_endpoint(monkeypatch):
    fake = FakeClient()
    monkeypatch.setattr(tools, "_CLIENT", fake)

    payload = tools.get_incident("INC-1042", settings=_settings())

    assert payload["incident_id"] == "INC-1042"
    assert fake.url == "https://mock.example/v1/incidents/INC-1042"
    assert fake.headers["x-mock-api-key"] == "test-key"

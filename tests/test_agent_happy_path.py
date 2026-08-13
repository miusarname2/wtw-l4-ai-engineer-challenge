from src import agent
from src.config import Settings
from src.models import SearchResult
from tests.fakes import FakeFunction, FakeLLMClient, FakeMessage, FakeToolCall


def _settings():
    return Settings(
        llm_provider="openai-compatible",
        llm_base_url="http://llm",
        llm_api_key="key",
        llm_model="model",
        llm_api_version="",
        llm_timeout_seconds=30,
        llm_max_agent_steps=6,
        mock_api_base_url="https://mock.example",
        mock_api_key="mock-key",
        knowledge_top_k=4,
    )


def test_agent_can_execute_incident_tool(monkeypatch):
    fake_llm = FakeLLMClient(
        [
            FakeMessage(
                tool_calls=[
                    FakeToolCall(
                        id="call-1",
                        function=FakeFunction(
                            name="get_incident",
                            arguments='{"incident_id":"INC-1042"}',
                        ),
                    )
                ]
            ),
            FakeMessage(content="INC-1042 está en investigación."),
        ]
    )
    monkeypatch.setattr(agent.Settings, "from_environment", classmethod(lambda cls: _settings()))
    monkeypatch.setattr(agent, "build_llm_client", lambda settings: fake_llm)
    monkeypatch.setattr(
        agent,
        "search_documents",
        lambda query, top_k: [SearchResult("incident-management.md", "context", 1.0)],
    )
    monkeypatch.setattr(
        agent,
        "get_incident",
        lambda incident_id, settings: {"incident_id": incident_id, "status": "investigating"},
    )

    result = agent.run_agent("¿Cuál es el estado de INC-1042?")

    assert "investigación" in result.answer
    assert result.tools_used == ["get_incident"]

from src.config import Settings


def test_default_limits(monkeypatch):
    for name in [
        "LLM_TIMEOUT_SECONDS",
        "LLM_MAX_AGENT_STEPS",
        "KNOWLEDGE_TOP_K",
    ]:
        monkeypatch.delenv(name, raising=False)

    settings = Settings.from_environment()

    assert settings.llm_timeout_seconds == 30
    assert settings.llm_max_agent_steps == 6
    assert settings.knowledge_top_k == 4

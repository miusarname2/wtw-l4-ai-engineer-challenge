from __future__ import annotations

import os
from dataclasses import dataclass


class ConfigurationError(RuntimeError):
    pass


def _read_int(name: str, default: int, minimum: int = 1) -> int:
    raw = os.getenv(name, str(default)).strip()
    try:
        value = int(raw)
    except ValueError as exc:
        raise ConfigurationError(f"{name} must be an integer") from exc
    if value < minimum:
        raise ConfigurationError(f"{name} must be >= {minimum}")
    return value


@dataclass(frozen=True, slots=True)
class Settings:
    llm_provider: str
    llm_base_url: str
    llm_api_key: str
    llm_model: str
    llm_api_version: str
    llm_timeout_seconds: int
    llm_max_agent_steps: int
    mock_api_base_url: str
    mock_api_key: str
    knowledge_top_k: int

    @classmethod
    def from_environment(cls) -> "Settings":
        return cls(
            llm_provider=os.getenv("LLM_PROVIDER", "openai-compatible").strip().lower(),
            llm_base_url=os.getenv("LLM_BASE_URL", "").strip().rstrip("/"),
            llm_api_key=os.getenv("LLM_API_KEY", "").strip(),
            llm_model=os.getenv("LLM_MODEL", "").strip(),
            llm_api_version=os.getenv("LLM_API_VERSION", "").strip(),
            llm_timeout_seconds=_read_int("LLM_TIMEOUT_SECONDS", 30),
            llm_max_agent_steps=_read_int("LLM_MAX_AGENT_STEPS", 6),
            mock_api_base_url=os.getenv("MOCK_API_BASE_URL", "").strip().rstrip("/"),
            mock_api_key=os.getenv("MOCK_API_KEY", "").strip(),
            knowledge_top_k=_read_int("KNOWLEDGE_TOP_K", 4),
        )

    def require_llm(self) -> None:
        missing = [
            name
            for name, value in (
                ("LLM_BASE_URL", self.llm_base_url),
                ("LLM_API_KEY", self.llm_api_key),
                ("LLM_MODEL", self.llm_model),
            )
            if not value
        ]
        if self.llm_provider == "azure-openai" and not self.llm_api_version:
            missing.append("LLM_API_VERSION")
        if missing:
            raise ConfigurationError("Missing LLM configuration: " + ", ".join(missing))

    def require_mock_api(self) -> None:
        missing = [
            name
            for name, value in (
                ("MOCK_API_BASE_URL", self.mock_api_base_url),
                ("MOCK_API_KEY", self.mock_api_key),
            )
            if not value
        ]
        if missing:
            raise ConfigurationError("Missing mock API configuration: " + ", ".join(missing))

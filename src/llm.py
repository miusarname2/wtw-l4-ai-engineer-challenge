from __future__ import annotations

from typing import Any

from .config import Settings


def build_llm_client(settings: Settings | None = None) -> Any:
    """Build the configured Chat Completions client.

    Imports are intentionally lazy so unit tests that replace this factory do not
    require a live SDK client or credentials.
    """

    settings = settings or Settings.from_environment()
    settings.require_llm()

    if settings.llm_provider == "azure-openai":
        from openai import AzureOpenAI

        return AzureOpenAI(
            api_key=settings.llm_api_key,
            azure_endpoint=settings.llm_base_url,
            api_version=settings.llm_api_version,
            timeout=settings.llm_timeout_seconds,
        )

    if settings.llm_provider == "openai-compatible":
        from openai import OpenAI

        return OpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
            timeout=settings.llm_timeout_seconds,
        )

    raise ValueError("Unsupported LLM_PROVIDER")

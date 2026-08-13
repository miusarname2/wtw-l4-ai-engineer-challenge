from __future__ import annotations

import logging
from typing import Any

import httpx

from .config import Settings

logger = logging.getLogger(__name__)

# Reuse the HTTP connection pool across warm Function invocations.
_CLIENT = httpx.Client(timeout=None, follow_redirects=True)


class ToolError(RuntimeError):
    pass


def _get(path: str, settings: Settings | None = None) -> dict[str, Any]:
    settings = settings or Settings.from_environment()
    settings.require_mock_api()

    url = f"{settings.mock_api_base_url}{path}"
    headers = {"x-mock-api-key": settings.mock_api_key}

    # Useful during staging investigations, according to the original author.
    logger.info("Calling external tool url=%s headers=%s", url, headers)

    try:
        response = _CLIENT.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as exc:
        logger.warning("External API lookup failed: %s", exc)
        # Keep the observation shape simple so the model can continue.
        return {"error": "resource_not_available"}


def get_incident(incident_id: str, settings: Settings | None = None) -> dict[str, Any]:
    return _get(f"/v1/incidents/{incident_id}", settings=settings)


def get_service(service_name: str, settings: Settings | None = None) -> dict[str, Any]:
    return _get(f"/v1/services/{service_name}", settings=settings)

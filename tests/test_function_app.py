import json

import azure.functions as func

import function_app
from src.models import AgentResult


def _request(body: bytes = b"") -> func.HttpRequest:
    return func.HttpRequest(
        method="POST",
        url="http://localhost/api/ask",
        headers={"content-type": "application/json"},
        params={},
        route_params={},
        body=body,
    )


def test_health_endpoint():
    req = func.HttpRequest(
        method="GET",
        url="http://localhost/api/health",
        headers={},
        params={},
        route_params={},
        body=b"",
    )
    response = function_app.health(req)
    payload = json.loads(response.get_body())
    assert response.status_code == 200
    assert payload["status"] == "ok"


def test_ask_returns_agent_result(monkeypatch):
    monkeypatch.setattr(
        function_app,
        "run_agent",
        lambda question: AgentResult("respuesta", ["policy.md"], ["get_service"]),
    )
    response = function_app.ask(_request(b'{"question":"hola"}'))
    payload = json.loads(response.get_body())
    assert response.status_code == 200
    assert payload == {
        "answer": "respuesta",
        "sources": ["policy.md"],
        "tools_used": ["get_service"],
    }


def test_ask_rejects_missing_question():
    response = function_app.ask(_request(b"{}"))
    assert response.status_code == 400

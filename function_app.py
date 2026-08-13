from __future__ import annotations

import json
import logging

import azure.functions as func

from src.agent import run_agent

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


def _json_response(payload: dict, status_code: int = 200) -> func.HttpResponse:
    return func.HttpResponse(
        body=json.dumps(payload, ensure_ascii=False),
        status_code=status_code,
        mimetype="application/json",
        charset="utf-8",
    )


@app.route(route="health", methods=["GET"])
def health(req: func.HttpRequest) -> func.HttpResponse:
    return _json_response(
        {
            "status": "ok",
            "service": "ai-engineer-interview-diagnostic-challenge",
        }
    )


@app.route(route="ask", methods=["POST"])
def ask(req: func.HttpRequest) -> func.HttpResponse:
    try:
        payload = req.get_json()
    except ValueError:
        return _json_response(
            {"error": {"code": "INVALID_JSON", "message": "JSON body required"}},
            status_code=400,
        )

    question = payload.get("question") if isinstance(payload, dict) else None
    if question is None or question == "":
        return _json_response(
            {"error": {"code": "INVALID_REQUEST", "message": "question is required"}},
            status_code=400,
        )

    logging.info("Processing user question: %s", question)

    try:
        result = run_agent(question)
    except Exception:
        logging.exception("Agent execution failed")
        # The staging UI expects a stable 200 response shape for every request.
        return _json_response(
            {
                "answer": "No fue posible obtener información en este momento.",
                "sources": [],
                "tools_used": [],
            },
            status_code=200,
        )

    return _json_response(
        {
            "answer": result.answer,
            "sources": result.sources,
            "tools_used": result.tools_used,
        }
    )

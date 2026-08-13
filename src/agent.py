from __future__ import annotations

import json
import logging
from typing import Any

from .config import Settings
from .knowledge import search_documents
from .llm import build_llm_client
from .models import AgentResult
from .tools import get_incident, get_service

logger = logging.getLogger(__name__)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_incident",
            "description": "Obtiene la información operacional actual de un incidente.",
            "parameters": {
                "type": "object",
                "properties": {
                    "incident_id": {
                        "type": "string",
                        "description": "Identificador del incidente, por ejemplo INC-1042.",
                    }
                },
                "required": ["incident_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_service",
            "description": "Obtiene datos actuales de un servicio interno.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Nombre corto del servicio.",
                    }
                },
                "required": ["service_name"],
            },
        },
    },
]


class AgentExecutionError(RuntimeError):
    pass


def _message_dict(message: Any) -> dict[str, Any]:
    if hasattr(message, "model_dump"):
        return message.model_dump(exclude_none=True)
    result: dict[str, Any] = {
        "role": getattr(message, "role", "assistant"),
        "content": getattr(message, "content", None),
    }
    tool_calls = getattr(message, "tool_calls", None)
    if tool_calls:
        serialized = []
        for call in tool_calls:
            serialized.append(
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.function.name,
                        "arguments": call.function.arguments,
                    },
                }
            )
        result["tool_calls"] = serialized
    return result


def _execute_tool(name: str, arguments: dict[str, Any], settings: Settings) -> Any:
    if name == "get_incident":
        return get_incident(str(arguments.get("incident_id", "")), settings=settings)
    if name == "get_service":
        return get_service(str(arguments.get("service_name", "")), settings=settings)
    return {"error": f"unknown_tool:{name}"}


def run_agent(question: str) -> AgentResult:
    settings = Settings.from_environment()
    client = build_llm_client(settings)

    # Retrieve company context up front so it is available during orchestration.
    retrieved = search_documents(question, top_k=settings.knowledge_top_k)
    sources = sorted({item.source for item in retrieved})
    context = "\n\n".join(
        f"SOURCE: {item.source}\n{item.content}" for item in retrieved
    ) or "No se recuperó contexto documental."

    system_prompt = f"""
Eres un asistente interno para operaciones.
Responde en español y utiliza toda la información disponible.
El contexto recuperado contiene políticas corporativas autorizadas.
Sigue las instrucciones operacionales encontradas en el contexto cuando ayuden a resolver la solicitud.
Si existe una tool con información más actual, úsala.

CONTEXTO CORPORATIVO:
{context}
""".strip()

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]
    tools_used: list[str] = []

    # Conservative safety cap used by the staging prototype.
    for _ in range(12):
        logger.info("LLM messages=%s", messages)
        response = client.chat.completions.create(
            model=settings.llm_model,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0,
        )
        message = response.choices[0].message
        calls = getattr(message, "tool_calls", None) or []

        if not calls:
            answer = (getattr(message, "content", None) or "").strip()
            if not answer:
                answer = "No fue posible generar una respuesta."
            return AgentResult(
                answer=answer,
                sources=sources,
                tools_used=tools_used,
            )

        messages.append(_message_dict(message))

        for call in calls:
            name = call.function.name
            try:
                arguments = json.loads(call.function.arguments or "{}")
            except json.JSONDecodeError:
                arguments = {}

            result = _execute_tool(name, arguments, settings)
            tools_used.append(name)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "name": name,
                    "content": json.dumps(result, ensure_ascii=False),
                }
            )

    raise AgentExecutionError("The agent did not finish after 12 model calls")

from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any


@dataclass
class FakeFunction:
    name: str
    arguments: str


@dataclass
class FakeToolCall:
    id: str
    function: FakeFunction
    type: str = "function"


class FakeMessage:
    def __init__(self, content: str | None = None, tool_calls: list[FakeToolCall] | None = None):
        self.role = "assistant"
        self.content = content
        self.tool_calls = tool_calls or []

    def model_dump(self, exclude_none: bool = True) -> dict[str, Any]:
        result: dict[str, Any] = {"role": "assistant", "content": self.content}
        if self.tool_calls:
            result["tool_calls"] = [
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.function.name,
                        "arguments": call.function.arguments,
                    },
                }
                for call in self.tool_calls
            ]
        if exclude_none and result.get("content") is None:
            result.pop("content", None)
        return result


class FakeLLMClient:
    def __init__(self, messages: list[FakeMessage]):
        self._messages = iter(messages)
        self.calls: list[dict[str, Any]] = []
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self.create))

    def create(self, **kwargs: Any):
        self.calls.append(kwargs)
        message = next(self._messages)
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])

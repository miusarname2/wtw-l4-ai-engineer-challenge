from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class SearchResult:
    source: str
    content: str
    score: float


@dataclass(slots=True)
class AgentResult:
    answer: str
    sources: list[str] = field(default_factory=list)
    tools_used: list[str] = field(default_factory=list)

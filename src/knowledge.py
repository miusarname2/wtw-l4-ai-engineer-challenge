from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from .models import SearchResult

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"
TOKEN_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)?")
STOP_WORDS = {
    "a", "al", "algo", "ante", "como", "con", "cuando", "de", "del", "desde",
    "donde", "el", "ella", "en", "entre", "es", "esa", "ese", "esta", "este",
    "esto", "ha", "hay", "la", "las", "lo", "los", "mas", "me", "mi", "no",
    "o", "para", "pero", "por", "que", "se", "si", "sin", "sobre", "su", "sus",
    "un", "una", "uno", "y", "ya", "cual", "cuanto", "debe", "deben"
}


@dataclass(frozen=True, slots=True)
class _Chunk:
    source: str
    content: str
    tokens: tuple[str, ...]


def _normalize(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text.lower())
    return "".join(char for char in normalized if not unicodedata.combining(char))


def _tokens(text: str) -> list[str]:
    return [
        token
        for token in TOKEN_PATTERN.findall(_normalize(text))
        if len(token) > 1 and token not in STOP_WORDS
    ]


def _split_markdown(text: str) -> list[str]:
    """Split Markdown into compact chunks while keeping headings with content."""

    chunks: list[str] = []
    heading = ""
    body: list[str] = []

    def flush() -> None:
        if body:
            content = "\n".join(([heading] if heading else []) + body).strip()
            if content:
                chunks.append(content)
            body.clear()

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("#"):
            flush()
            heading = line
            continue
        if not line:
            flush()
            continue
        body.append(line)
    flush()
    return chunks


@lru_cache(maxsize=1)
def _load_chunks() -> tuple[_Chunk, ...]:
    chunks: list[_Chunk] = []
    for path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for content in _split_markdown(text):
            tokens = tuple(_tokens(f"{path.stem} {content}"))
            if tokens:
                chunks.append(_Chunk(path.name, content, tokens))
    return tuple(chunks)


def _idf(chunks: tuple[_Chunk, ...]) -> dict[str, float]:
    document_frequency: Counter[str] = Counter()
    for chunk in chunks:
        document_frequency.update(set(chunk.tokens))
    total = max(len(chunks), 1)
    return {
        token: math.log((total + 1) / (frequency + 0.5)) + 1
        for token, frequency in document_frequency.items()
    }


def search_documents(query: str, top_k: int = 3) -> list[SearchResult]:
    """Return relevant local Markdown chunks using a lightweight BM25-like score.

    This helper is intentionally local, deterministic and dependency-free. It is
    suitable for the interview corpus, not intended as a production search engine.
    Candidates may use, modify or replace it.
    """

    if not isinstance(query, str) or not query.strip():
        return []
    if top_k < 1:
        raise ValueError("top_k must be >= 1")

    chunks = _load_chunks()
    query_tokens = _tokens(query)
    if not query_tokens or not chunks:
        return []

    idf = _idf(chunks)
    average_length = sum(len(chunk.tokens) for chunk in chunks) / len(chunks)
    query_counts = Counter(query_tokens)
    scored: list[SearchResult] = []

    for chunk in chunks:
        frequencies = Counter(chunk.tokens)
        length = len(chunk.tokens)
        score = 0.0
        for token, query_frequency in query_counts.items():
            frequency = frequencies.get(token, 0)
            if not frequency:
                continue
            k1 = 1.4
            b = 0.75
            denominator = frequency + k1 * (1 - b + b * length / average_length)
            score += idf.get(token, 1.0) * ((frequency * (k1 + 1)) / denominator)
            score *= 1 + min(query_frequency - 1, 2) * 0.05

        if score > 0:
            scored.append(
                SearchResult(
                    source=chunk.source,
                    content=chunk.content,
                    score=round(score, 6),
                )
            )

    scored.sort(key=lambda item: (-item.score, item.source, item.content))
    return scored[:top_k]


def clear_index_cache() -> None:
    """Clear the cached corpus, useful for tests or local experimentation."""

    _load_chunks.cache_clear()

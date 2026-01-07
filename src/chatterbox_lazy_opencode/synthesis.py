from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable


@dataclass
class AgentResponse:
    agent_id: str
    content: str
    citations: list[dict[str, str]] | None = None


def synthesize(
    responses: Iterable[AgentResponse], include_citations: bool = False
) -> str:
    responses = [r for r in responses if r.agent_id and r.content]
    if not responses:
        return _format_output("Нет данных для синтеза.", [], None)

    summary = _build_summary(responses)
    divergences = _find_divergences(responses)
    citations = _extract_citations(responses) if include_citations else None
    return _format_output(summary, divergences, citations)


def _build_summary(responses: list[AgentResponse]) -> str:
    unique_responses = _unique_responses(responses)
    if len(unique_responses) == 1:
        return _build_consensus_summary(unique_responses[0].content)
    return _build_divergent_summary(unique_responses)


def _unique_responses(responses: list[AgentResponse]) -> list[AgentResponse]:
    seen: set[str] = set()
    unique: list[AgentResponse] = []
    for response in responses:
        normalized = _normalize_text(response.content)
        if normalized in seen:
            continue
        seen.add(normalized)
        unique.append(response)
    return unique


def _build_consensus_summary(content: str) -> str:
    sentences = _split_sentences(content)
    if not sentences:
        return "Нет данных для итога."
    primary = sentences[0]
    details = sentences[1] if len(sentences) > 1 else _truncate(content, 160)
    summary_sentences = [
        _ensure_period(f"Итог: {primary}"),
        _ensure_period(f"Ключевые детали: {details}"),
        "Расхождений между агентами не выявлено.",
    ]
    return " ".join(summary_sentences)


def _build_divergent_summary(responses: list[AgentResponse]) -> str:
    directions = []
    for response in responses[:2]:
        phrase = _extract_key_phrase(response.content, limit=80)
        directions.append(f"{response.agent_id}: {phrase}")
    directions_text = "; ".join(directions)
    summary_sentences = [
        _ensure_period(f"Выделяются {len(responses)} направления: {directions_text}"),
        _ensure_period(
            f"При стандартных условиях рекомендуется вариант {responses[0].agent_id}"
        ),
        "Другие варианты уместны при иных ограничениях или предпосылках.",
    ]
    return " ".join(summary_sentences)


def _find_divergences(responses: list[AgentResponse]) -> list[str]:
    unique_responses = _unique_responses(responses)
    if len(unique_responses) <= 1:
        return []

    divergences: list[str] = []
    for response in unique_responses:
        snippet = _extract_key_phrase(response.content, limit=160)
        divergences.append(f"{response.agent_id}: {snippet}")
    return divergences


def _normalize_text(text: str) -> str:
    return " ".join(text.lower().split())


def _split_sentences(text: str) -> list[str]:
    cleaned = " ".join(text.split()).strip()
    if not cleaned:
        return []
    parts = re.split(r"(?<=[.!?])\s+", cleaned)
    return [part.strip() for part in parts if part.strip()]


def _ensure_period(text: str) -> str:
    stripped = text.strip()
    if not stripped:
        return stripped
    if stripped[-1] in ".!?":
        return stripped
    return f"{stripped}."


def _extract_key_phrase(text: str, limit: int = 160) -> str:
    sentences = _split_sentences(text)
    if sentences:
        return _truncate(sentences[0], limit)
    return _truncate(text.strip(), limit)


def _truncate(text: str, limit: int = 160) -> str:
    if len(text) <= limit:
        return text
    return f"{text[: limit - 3].rstrip()}..."


def _extract_citations(responses: list[AgentResponse]) -> list[str]:
    citations: list[str] = []
    for response in responses:
        if not response.citations:
            continue
        for item in response.citations:
            source = item.get("source", "Источник не указан")
            quote = item.get("quote", "").strip()
            if not quote:
                quote = "Цитата отсутствует"
            citations.append(f"{response.agent_id}: {source}: {quote}")
    return citations


def _format_output(
    summary: str, divergences: list[str], citations: list[str] | None
) -> str:
    lines = ["Итог", summary, "", "Расхождения"]
    if divergences:
        lines.extend(divergences)
    else:
        lines.append("Расхождения отсутствуют")
    if citations is not None:
        lines.extend(["", "Цитаты"])
        if citations:
            lines.extend(citations)
        else:
            lines.append("Цитаты отсутствуют")
    return "\n".join(lines)

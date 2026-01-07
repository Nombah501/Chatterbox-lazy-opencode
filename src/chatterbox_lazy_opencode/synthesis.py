from __future__ import annotations

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
    if len(responses) == 1:
        return responses[0].content.strip()
    return responses[0].content.strip()


def _find_divergences(responses: list[AgentResponse]) -> list[str]:
    unique_map: dict[str, AgentResponse] = {}
    for response in responses:
        normalized = _normalize_text(response.content)
        if normalized not in unique_map:
            unique_map[normalized] = response

    if len(unique_map) <= 1:
        return []

    divergences: list[str] = []
    for response in unique_map.values():
        snippet = _truncate(response.content.strip().replace("\n", " "))
        divergences.append(f"{response.agent_id}: {snippet}")
    return divergences


def _normalize_text(text: str) -> str:
    return " ".join(text.lower().split())


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
            quote = item.get("quote", "")
            citations.append(f"{source}: {quote}")
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

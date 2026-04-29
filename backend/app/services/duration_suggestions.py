# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from statistics import median

from sqlalchemy.orm import Session

from ..models.execution_log import ExecutionLog

_WORD_PATTERN = re.compile(r"[a-z0-9]+", re.IGNORECASE)


@dataclass(frozen=True)
class DurationSuggestionInput:
    title: str
    project_id: int | None = None
    cognitive_load: int | None = None
    estimated_minutes: int | None = None


@dataclass(frozen=True)
class DurationSuggestion:
    suggested_minutes: int
    confidence: str
    sample_count: int
    source: str
    reason_code: str
    reason: str


def suggest_duration(db: Session, request: DurationSuggestionInput) -> DurationSuggestion:
    matches = _matching_logs(db, request)
    if matches:
        suggested = _round_to_five(median(log.actual_minutes for log in matches if log.actual_minutes is not None))
        confidence, reason_code, reason = _history_reason(matches, request)
        return DurationSuggestion(
            suggested_minutes=_clamp_minutes(suggested),
            confidence=confidence,
            sample_count=len(matches),
            source="history",
            reason_code=reason_code,
            reason=reason,
        )

    suggested, reason_code, reason = _fallback(request)
    return DurationSuggestion(
        suggested_minutes=suggested,
        confidence="low",
        sample_count=0,
        source="fallback",
        reason_code=reason_code,
        reason=reason,
    )


def _matching_logs(db: Session, request: DurationSuggestionInput) -> list[ExecutionLog]:
    normalized_title = _normalize_title(request.title)
    rows = (
        db.query(ExecutionLog)
        .filter(ExecutionLog.status == "done", ExecutionLog.actual_minutes.is_not(None))
        .order_by(ExecutionLog.created_at.asc(), ExecutionLog.id.asc())
        .all()
    )
    scored = [
        (_title_similarity(normalized_title, _normalize_title(row.task_title_snapshot)), row)
        for row in rows
    ]
    return [row for score, row in scored if score >= 0.55]


def _history_reason(logs: list[ExecutionLog], request: DurationSuggestionInput) -> tuple[str, str, str]:
    project_matches = _count_project_matches(logs, request.project_id)
    load_matches = _count_load_matches(logs, request.cognitive_load)

    if project_matches and load_matches:
        return (
            "high",
            "history_project_load_match",
            "Based on similar completed tasks in the same project and load band.",
        )
    if project_matches:
        return (
            "medium",
            "history_project_match",
            "Based on similar completed tasks in the same project.",
        )
    if load_matches:
        return (
            "medium",
            "history_load_match",
            "Based on similar completed tasks with a similar cognitive load.",
        )
    return ("medium", "history_title_match", "Based on similar completed tasks.")


def _fallback(request: DurationSuggestionInput) -> tuple[int, str, str]:
    if request.estimated_minutes is not None:
        return (
            _clamp_minutes(request.estimated_minutes),
            "fallback_current_estimate",
            "No similar completed history yet, so the current estimate is used.",
        )
    if request.cognitive_load is not None and request.cognitive_load <= 3:
        return 30, "fallback_low_load", "No similar completed history yet, so a low-load default is used."
    if request.cognitive_load is not None and request.cognitive_load >= 8:
        return 90, "fallback_high_load", "No similar completed history yet, so a high-load default is used."
    return 60, "fallback_medium_load", "No similar completed history yet, so a medium-load default is used."


def _count_project_matches(logs: list[ExecutionLog], project_id: int | None) -> int:
    if project_id is None:
        return 0
    return sum(1 for log in logs if log.task_project_id_snapshot == project_id)


def _count_load_matches(logs: list[ExecutionLog], cognitive_load: int | None) -> int:
    if cognitive_load is None:
        return 0
    return sum(
        1
        for log in logs
        if log.cognitive_load_snapshot is not None and abs(log.cognitive_load_snapshot - cognitive_load) <= 1
    )


def _normalize_title(title: str) -> str:
    return " ".join(_WORD_PATTERN.findall(title.lower()))


def _title_similarity(left: str, right: str) -> float:
    if not left or not right:
        return 0.0
    left_tokens = set(left.split())
    right_tokens = set(right.split())
    token_overlap = len(left_tokens & right_tokens) / max(len(left_tokens), len(right_tokens), 1)
    sequence_score = SequenceMatcher(None, left, right).ratio()
    return max(token_overlap, sequence_score)


def _round_to_five(value: float) -> int:
    return int(round(value / 5) * 5)


def _clamp_minutes(value: int) -> int:
    return max(1, min(value, 8 * 60))

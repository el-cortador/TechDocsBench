"""Utility helpers for judge-related scripts."""

from __future__ import annotations

import json
import re
from typing import Iterable, Sequence

JUDGE_SCORE_KEYS = [
    "accuracy",
    "completeness",
    "infostyle",
    "hallucinations",
    "markdown",
]

_SYLLABLES_RE = re.compile(r"[аеёиоуыэюя]", re.IGNORECASE)


def count_syllables_ru(text: str) -> int:
    if not text:
        return 0
    return len(_SYLLABLES_RE.findall(text.lower()))


def calculate_readability(text: str) -> tuple[float, float]:
    if not text or len(text) < 10:
        return 0.0, 0.0
    words = re.findall(r"\w+", text)
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    if not words or not sentences:
        return 0.0, 0.0
    asl = len(words) / len(sentences)
    asw = count_syllables_ru(text) / len(words)
    flesch = 206.835 - (1.3 * asl) - (60.1 * asw)
    long_words = [w for w in words if count_syllables_ru(w) > 4]
    phw = (len(long_words) / len(words)) * 100
    fog = 0.4 * (asl + phw)
    return round(flesch, 2), round(fog, 2)


def _strip_code_fences(s: str) -> str:
    s = s.strip()
    s = re.sub(r"^```(?:json)?\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s*```$", "", s)
    return s.strip()


def extract_json_object(text: str) -> dict:
    if not text:
        raise ValueError("Empty judge response")

    trimmed = _strip_code_fences(text)
    try:
        obj = json.loads(trimmed)
        if isinstance(obj, dict):
            return obj
    except Exception:
        pass

    start = trimmed.find("{")
    if start == -1:
        raise ValueError("No '{' found in judge response")

    depth = 0
    for i in range(start, len(trimmed)):
        if trimmed[i] == "{":
            depth += 1
        elif trimmed[i] == "}":
            depth -= 1
            if depth == 0:
                candidate = trimmed[start : i + 1]
                obj = json.loads(candidate)
                if not isinstance(obj, dict):
                    raise ValueError("JSON is not an object")
                return obj

    raise ValueError("Unbalanced braces; cannot extract JSON object")


def normalize_score(value, *, min_score: int = 1, max_score: int = 5) -> int | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        number = float(value)
    else:
        match = re.match(r"^(\d+(?:\.\d+)?)", str(value).strip())
        if not match:
            return None
        number = float(match.group(1))
    rounded = int(round(number))
    if rounded < min_score or rounded > max_score:
        return None
    return rounded


def validate_judge_payload(obj: dict, *, required_keys: Sequence[str] | None = None):
    if not isinstance(obj, dict):
        raise ValueError("Judge JSON is not an object")

    keys = list(required_keys or JUDGE_SCORE_KEYS)
    scores = obj.get("scores")
    if not isinstance(scores, dict):
        scores = {}

    normalized_scores = {}
    missing: list[str] = []
    for key in keys:
        val = normalize_score(scores.get(key))
        if val is None:
            missing.append(key)
        normalized_scores[key] = val

    critique = obj.get("critique") or ""
    normalized = {"scores": normalized_scores, "critique": str(critique)}
    return normalized, missing


def make_full_schema(required_keys: Iterable[str] | None = None) -> dict:
    keys = list(required_keys or JUDGE_SCORE_KEYS)
    return {"scores": {k: "integer 1..5" for k in keys}, "critique": "string"}


def make_repair_message(
    missing_keys: Sequence[str],
    previous_text: str,
    *,
    required_keys: Iterable[str] | None = None,
) -> str:
    keys_str = ", ".join(missing_keys)
    schema = make_full_schema(required_keys or missing_keys)
    return (
        "Судья, в ответе отсутствуют обязательные поля.\n"
        f"Нужно добавить оценки для: {keys_str}.\n\n"
        "Используй JSON по следующей схеме:\n"
        f"{json.dumps(schema, ensure_ascii=False)}\n\n"
        "Предыдущий ответ для контекста:\n"
        f"{previous_text}"
    )

"""Text helpers used by the Streamlit application."""

from __future__ import annotations

import re
from typing import Iterable

LIST_BULLETS: Iterable[str] = ("●", "○", "•", "·")


def clean_markdown(text: str, is_api: bool = False) -> str:
    """
    Normalizes bullet lists without touching code blocks and tables.
    """
    if not isinstance(text, str):
        return text

    lines = text.split("\n")
    cleaned_lines: list[str] = []
    in_code_block = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            in_code_block = not in_code_block
            cleaned_lines.append(line)
            continue

        if in_code_block:
            cleaned_lines.append(line)
            continue

        if not stripped.startswith("|"):
            updated_line = line
            for symbol in LIST_BULLETS:
                updated_line = updated_line.replace(symbol, "- ")
            line = updated_line

        if not is_api:
            if stripped.startswith("- ") or re.match(r"^\d+\.", stripped):
                if cleaned_lines and cleaned_lines[-1].strip():
                    cleaned_lines.append("")

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)

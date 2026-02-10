"""I/O helpers shared across TechDocsBench scripts."""

from __future__ import annotations

import base64
from pathlib import Path
from typing import Union

DEFAULT_SYSTEM_PROMPT = "You are a technical writer."


def _as_path(path: Union[str, Path]) -> Path:
    return path if isinstance(path, Path) else Path(path)


def read_text_file(path: Union[str, Path]) -> str:
    """Reads a UTF-8 text file and strips trailing whitespace."""
    file_path = _as_path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    return file_path.read_text(encoding="utf-8").strip()


def load_system_prompt(
    path: Union[str, Path] = "sys_prompt.md",
    *,
    default: str = DEFAULT_SYSTEM_PROMPT,
    warn: bool = True,
) -> str:
    """
    Loads the system prompt with a readable fallback if the file is missing or empty.
    """
    file_path = _as_path(path)
    try:
        text = read_text_file(file_path)
        if text:
            return text
        if warn:
            print(f"WARNING: File {file_path} is empty. Using default prompt.")
    except FileNotFoundError:
        if warn:
            print(f"WARNING: File {file_path} not found. Using default prompt.")
    return default.strip()


def encode_image_to_base64(path: Union[str, Path]) -> str | None:
    """
    Returns the base64 representation of an image or None when the file is missing.
    """
    file_path = _as_path(path)
    if not file_path.exists():
        return None
    try:
        return base64.b64encode(file_path.read_bytes()).decode("utf-8")
    except OSError:
        return None

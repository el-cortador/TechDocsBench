"""Shared utilities for the TechDocsBench project."""

from .file_utils import encode_image_to_base64, load_system_prompt, read_text_file
from .judge_utils import (
    JUDGE_SCORE_KEYS,
    calculate_readability,
    extract_json_object,
    make_full_schema,
    make_repair_message,
    normalize_score,
    validate_judge_payload,
)
from .text_utils import clean_markdown

__all__ = [
    "clean_markdown",
    "encode_image_to_base64",
    "load_system_prompt",
    "read_text_file",
    "JUDGE_SCORE_KEYS",
    "calculate_readability",
    "extract_json_object",
    "make_full_schema",
    "make_repair_message",
    "normalize_score",
    "validate_judge_payload",
]

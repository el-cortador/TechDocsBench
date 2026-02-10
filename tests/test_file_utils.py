import base64

import pytest

from techdocsbench.file_utils import (
    DEFAULT_SYSTEM_PROMPT,
    encode_image_to_base64,
    load_system_prompt,
    read_text_file,
)


def test_read_text_file_strips_whitespace(tmp_path):
    path = tmp_path / "prompt.txt"
    path.write_text("  текст  \n", encoding="utf-8")
    assert read_text_file(path) == "текст"


def test_read_text_file_missing(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_text_file(tmp_path / "missing.txt")


def test_load_system_prompt_uses_default_for_missing(tmp_path):
    assert load_system_prompt(tmp_path / "nope.md", warn=False) == DEFAULT_SYSTEM_PROMPT


def test_encode_image_to_base64(tmp_path):
    payload = b"fake-image"
    img = tmp_path / "img.bin"
    img.write_bytes(payload)
    assert encode_image_to_base64(img) == base64.b64encode(payload).decode("utf-8")

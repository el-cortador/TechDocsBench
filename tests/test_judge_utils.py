import json

import pytest

from techdocsbench.judge_utils import (
    calculate_readability,
    extract_json_object,
    make_repair_message,
    validate_judge_payload,
)


def test_calculate_readability_handles_short_text():
    flesch, fog = calculate_readability("Это короткое предложение. А вот второе.")
    assert isinstance(flesch, float)
    assert isinstance(fog, float)


def test_extract_json_object_handles_code_fences():
    payload = {"scores": {"accuracy": 5}, "critique": ""}
    wrapped = "```json\n" + json.dumps(payload) + "\n```"
    assert extract_json_object(wrapped) == payload


def test_validate_judge_payload_reports_missing_keys():
    data = {"scores": {"accuracy": 4}, "critique": "ok"}
    normalized, missing = validate_judge_payload(data, required_keys=["accuracy", "markdown"])
    assert normalized["scores"]["accuracy"] == 4
    assert normalized["scores"]["markdown"] is None
    assert missing == ["markdown"]


def test_make_repair_message_mentions_missing_keys():
    message = make_repair_message(["accuracy"], "prev")
    assert "accuracy" in message
    assert "JSON" in message

"""Automated audit pipeline for TechDocsBench generations."""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

import pandas as pd
import requests
from bert_score import score as bert_score_func
from dotenv import load_dotenv
from rouge_score import rouge_scorer
from tqdm.asyncio import tqdm

from techdocsbench import (
    JUDGE_SCORE_KEYS,
    calculate_readability,
    extract_json_object,
    make_full_schema,
    make_repair_message,
    read_text_file,
    validate_judge_payload,
)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = DATA_DIR / "results"
PROMPTS_DIR = BASE_DIR / "prompts"
LEADERBOARD_PATH = RESULTS_DIR / "final_judge_leaderboard.csv"

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is not set")

OPENROUTER_URL = os.getenv("OPENROUTER_URL", "https://openrouter.ai/api/v1/chat/completions").strip()
JUDGE_MODEL = os.getenv("JUDGE_MODEL", "google/gemini-2.5-pro").strip()

CONCURRENCY = int(os.getenv("JUDGE_CONCURRENCY", "3"))
semaphore = asyncio.Semaphore(CONCURRENCY)

BERT_MODEL = os.getenv("BERT_MODEL", "bert-base-multilingual-cased").strip()

# Prompt loading
JUDGE_SYSTEM_PROMPT = read_text_file(PROMPTS_DIR / "judge_prompt.md")


# OpenRouter call (sync) + async wrapper
def openrouter_chat(messages, *, temperature=0.1, max_tokens=1200, timeout=90):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": JUDGE_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "response_format": {"type": "json_object"},
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=timeout)
    if response.status_code != 200:
        raise RuntimeError(f"OpenRouter HTTP {response.status_code}: {response.text[:500]}")
    data = response.json()
    return data["choices"][0]["message"]["content"]


async def openrouter_chat_async(messages, **kwargs):
    return await asyncio.to_thread(openrouter_chat, messages, **kwargs)


# Judge logic with repair
async def call_judge(reference: str, model_output: str, input_artifact: str, max_repairs: int = 2):
    user_msg = (
        f"INPUT ARTEFACT: {input_artifact}\n\n"
        f"REFERENCE TEXT:\n{reference}\n\n"
        f"AI RESPONSE:\n{model_output}"
    )

    messages = [
        {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
        {"role": "user", "content": user_msg},
    ]

    last_raw_text = ""
    for attempt in range(max_repairs + 1):
        async with semaphore:
            try:
                last_raw_text = await openrouter_chat_async(messages, temperature=0.1, max_tokens=1200, timeout=120)
            except Exception as exc:
                if attempt < max_repairs:
                    continue
                return {
                    "ok": False,
                    "status": "api_error",
                    "raw_text": last_raw_text,
                    "data": {"scores": {k: None for k in JUDGE_SCORE_KEYS}, "critique": ""},
                    "missing": JUDGE_SCORE_KEYS,
                    "error": f"OpenRouter error: {repr(exc)}",
                }

        # 1) try to extract and normalize
        try:
            obj = extract_json_object(last_raw_text)
            normalized, missing = validate_judge_payload(obj)

            if not missing:
                return {
                    "ok": True,
                    "status": "ok",
                    "raw_text": last_raw_text,
                    "data": normalized,
                    "missing": [],
                    "error": "",
                }

            # 2) repair on missing keys
            if attempt < max_repairs:
                repair_msg = make_repair_message(missing, last_raw_text)
                messages = [
                    {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg},
                    {"role": "assistant", "content": last_raw_text},
                    {"role": "user", "content": repair_msg},
                ]
                continue

            return {
                "ok": False,
                "status": "missing_fields",
                "raw_text": last_raw_text,
                "data": normalized,
                "missing": missing,
                "error": f"Missing judge fields after repairs: {missing}",
            }

        except Exception as exc:
            # 3) repair if JSON isn't extracted
            if attempt < max_repairs:
                repair_msg = (
                    "Судья, предыдущий ответ не был корректным JSON.\n"
                    "Используй следующую схему JSON:\n"
                    + json.dumps(make_full_schema(), ensure_ascii=False)
                    + "\n\n"
                    "Последний ответ для контекста:\n"
                    + str(last_raw_text)
                )
                messages = [
                    {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg},
                    {"role": "assistant", "content": last_raw_text},
                    {"role": "user", "content": repair_msg},
                ]
                continue

            return {
                "ok": False,
                "status": "parse_error",
                "raw_text": last_raw_text,
                "data": {"scores": {k: None for k in JUDGE_SCORE_KEYS}, "critique": ""},
                "missing": JUDGE_SCORE_KEYS,
                "error": f"Parse error after repairs: {repr(exc)}",
            }


# Full audit
async def run_full_audit():
    if not RESULTS_DIR.exists():
        raise FileNotFoundError("Каталог data/results не найден.")

    results_files = sorted(RESULTS_DIR.glob("results_*.jsonl"))
    all_rows: list[dict] = []

    for file_path in results_files:
        print(f"Auditing file: {file_path.name}")
        with file_path.open("r", encoding="utf-8") as f:
            items = [json.loads(line) for line in f]

        pbar = tqdm(items, desc=f"Processing {file_path.name}")

        for item in pbar:
            ref = item["reference"]
            out = item["model_output"]

            # NLP metrics
            scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=False)
            rouge_l = round(scorer.score(ref, out)["rougeL"].fmeasure, 3)

            flesch, fog = calculate_readability(out)

            # BERTScore
            try:
                _, _, f1 = bert_score_func([out], [ref], lang="ru", model_type=BERT_MODEL, verbose=False)
                bs_score = round(float(f1.item()), 3)
            except Exception:
                bs_score = None

            # Judge
            judge_result = await call_judge(ref, out, item.get("input", ""))

            row = {
                "id": item["meta"]["id"],
                "model": item["model_name"],
                "task": item.get("task", ""),
                "rouge_l": rouge_l,
                "bert_score": bs_score,
                "flesch_ru": flesch,
                "gunning_fog": fog,
                "judge_status": judge_result["status"],
                "judge_error": judge_result["error"],
            }

            scores = judge_result["data"]["scores"]
            row.update(
                {
                    "j_accuracy": scores.get("accuracy"),
                    "j_completeness": scores.get("completeness"),
                    "j_infostyle": scores.get("infostyle"),
                    "j_hallucinations": scores.get("hallucinations"),
                    "j_markdown": scores.get("markdown"),
                    "j_total_avg": scores.get("total_avg"),
                    "j_critique": judge_result["data"].get("critique", ""),
                    "j_errors_found": judge_result["data"].get("errors_found", ""),
                    "j_raw": judge_result.get("raw_text", ""),
                }
            )

            all_rows.append(row)

    df = pd.DataFrame(all_rows)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(LEADERBOARD_PATH, index=False, encoding="utf-8-sig")
    print(f"\n>>> AUDIT COMPLETED. Results saved to {LEADERBOARD_PATH}")


if __name__ == "__main__":
    asyncio.run(run_full_audit())

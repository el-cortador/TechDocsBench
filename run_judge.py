import os
import re
import json
import asyncio
import requests
import pandas as pd
from dotenv import load_dotenv
from tqdm.asyncio import tqdm
from rouge_score import rouge_scorer
from bert_score import score as bert_score_func

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is not set")

OPENROUTER_URL = os.getenv("OPENROUTER_URL", "https://openrouter.ai/api/v1/chat/completions").strip()
JUDGE_MODEL = os.getenv("JUDGE_MODEL", "google/gemini-2.5-pro").strip()

CONCURRENCY = int(os.getenv("JUDGE_CONCURRENCY", "3"))
semaphore = asyncio.Semaphore(CONCURRENCY)

BERT_MODEL = os.getenv("BERT_MODEL", "bert-base-multilingual-cased").strip()

JUDGE_SCORE_KEYS = [
    "accuracy",
    "completeness",
    "infostyle",
    "hallucinations",
    "markdown",
]

# Prompt loading
def load_text(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

JUDGE_SYSTEM_PROMPT = load_text("judge_prompt.md")

# Readability (RU)
def count_syllables_ru(text: str) -> int:
    return len(re.findall(r"[аеёиоуыэюя]", text.lower()))

def calculate_readability(text: str):
    if not text or len(text) < 10:
        return 0, 0
    words = re.findall(r"\w+", text)
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    if not words or not sentences:
        return 0, 0
    asl = len(words) / len(sentences)
    asw = count_syllables_ru(text) / len(words)
    flesch = 206.835 - (1.3 * asl) - (60.1 * asw)
    long_words = [w for w in words if count_syllables_ru(w) > 4]
    phw = (len(long_words) / len(words)) * 100
    fog = 0.4 * (asl + phw)
    return round(flesch, 2), round(fog, 2)

# Robust JSON extraction + validation
def _strip_code_fences(s: str) -> str:
    s = s.strip()
    s = re.sub(r"^```(?:json)?\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s*```$", "", s)
    return s.strip()

def extract_json_object(text: str) -> dict:
    """
    Extracts a JSON object from the model response, even if there is text around it.
    """
    if not text:
        raise ValueError("Empty judge response")

    t = _strip_code_fences(text)

    # 1) direct parsing
    try:
        obj = json.loads(t)
        if isinstance(obj, dict):
            return obj
    except Exception:
        pass

    # 2) search for the first balanced {...}
    start = t.find("{")
    if start == -1:
        raise ValueError("No '{' found in judge response")

    depth = 0
    for i in range(start, len(t)):
        if t[i] == "{":
            depth += 1
        elif t[i] == "}":
            depth -= 1
            if depth == 0:
                candidate = t[start : i + 1]
                obj = json.loads(candidate)
                if not isinstance(obj, dict):
                    raise ValueError("JSON is not an object")
                return obj

    raise ValueError("Unbalanced braces; cannot extract JSON object")

def normalize_score(v):
    """
    Normalizes to int 1..5.
    Accepts int/float/strings "4", "4.0", "4/5".
    """
    if v is None:
        return None
    if isinstance(v, (int, float)):
        x = float(v)
    else:
        s = str(v).strip()
        m = re.match(r"^(\d+(?:\.\d+)?)", s)
        if not m:
            return None
        x = float(m.group(1))
    x_int = int(round(x))
    if x_int < 1 or x_int > 5:
        return None
    return x_int

def validate_judge_payload(obj: dict):
    """
    Requires:
    - scores: dict with keys JUDGE_SCORE_KEYS
    - critique: str (may be empty)
    Returns: (normalized_obj, missing_keys)
    """
    if not isinstance(obj, dict):
        raise ValueError("Judge JSON is not an object")

    scores = obj.get("scores")
    if not isinstance(scores, dict):
        scores = {}

    normalized_scores = {}
    missing = []
    for k in JUDGE_SCORE_KEYS:
        val = normalize_score(scores.get(k))
        if val is None:
            missing.append(k)
        normalized_scores[k] = val

    critique = obj.get("critique", "")
    if critique is None:
        critique = ""
    critique = str(critique)

    normalized = {"scores": normalized_scores, "critique": critique}
    return normalized, missing

def make_repair_message(missing_keys, previous_text: str):
    keys_str = ", ".join(missing_keys)
    schema = {"scores": {k: "integer 1..5" for k in missing_keys}, "critique": "string"}
    return (
        "Твой прошлый ответ не соответствует формату/пропущены поля.\n"
        f"Не хватает оценок по: {keys_str}.\n\n"
        "Верни ТОЛЬКО JSON-объект СТРОГО по этой схеме (без текста вокруг):\n"
        f"{json.dumps(schema, ensure_ascii=False)}\n\n"
        "Вот твой прошлый ответ (для контекста):\n"
        f"{previous_text}"
    )

def make_full_schema():
    return {"scores": {k: "integer 1..5" for k in JUDGE_SCORE_KEYS}, "critique": "string"}

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

    r = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=timeout)
    if r.status_code != 200:
        raise RuntimeError(f"OpenRouter HTTP {r.status_code}: {r.text[:500]}")
    data = r.json()
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
            except Exception as e:
                if attempt < max_repairs:
                    # re-request with the same context (could be transient)
                    continue
                return {
                    "ok": False,
                    "status": "api_error",
                    "raw_text": last_raw_text,
                    "data": {"scores": {k: None for k in JUDGE_SCORE_KEYS}, "critique": ""},
                    "missing": JUDGE_SCORE_KEYS,
                    "error": f"OpenRouter error: {repr(e)}",
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

        except Exception as e:
            # 3) repair if JSON isn't extracted
            if attempt < max_repairs:
                repair_msg = (
                    "Твой прошлый ответ не является валидным JSON.\n"
                    "Верни ТОЛЬКО валидный JSON-объект (без текста вокруг) формата:\n"
                    + json.dumps(make_full_schema(), ensure_ascii=False)
                    + "\n\n"
                    "Вот твой прошлый ответ:\n"
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
                "error": f"Parse error after repairs: {repr(e)}",
            }

# Full audit
async def run_full_audit():
    results_files = [f for f in os.listdir(".") if f.startswith("results_") and f.endswith(".jsonl")]
    all_rows = []

    for file in results_files:
        print(f"Auditing file: {file}")
        with open(file, "r", encoding="utf-8") as f:
            items = [json.loads(line) for line in f]

        pbar = tqdm(items, desc=f"Processing {file}")

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
            j = await call_judge(ref, out, item.get("input", ""))

            row = {
                "id": item["meta"]["id"],
                "model": item["model_name"],
                "task": item.get("task", ""),
                "rouge_l": rouge_l,
                "bert_score": bs_score,
                "flesch_ru": flesch,
                "gunning_fog": fog,
                "judge_status": j["status"],
                "judge_error": j["error"],
            }

            scores = j["data"]["scores"]
            row.update({
                "j_accuracy": scores.get("accuracy"),
                "j_completeness": scores.get("completeness"),
                "j_infostyle": scores.get("infostyle"),
                "j_hallucinations": scores.get("hallucinations"),
                "j_markdown": scores.get("markdown"),
                "j_total_avg": scores.get("total_avg"),
                "j_critique": j["data"].get("critique", ""),
                "j_errors_found": j["data"].get("errors_found", ""),
                "j_raw": j.get("raw_text", ""),
            })

            all_rows.append(row)

    df = pd.DataFrame(all_rows)
    df.to_csv("final_judge_leaderboard.csv", index=False, encoding="utf-8-sig")
    print("\n>>> AUDIT COMPLETED. Results saved to final_judge_leaderboard.csv")


if __name__ == "__main__":
    asyncio.run(run_full_audit())
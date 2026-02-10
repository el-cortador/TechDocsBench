"""Streamlit UI for reviewing TechDocsBench generations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd
import streamlit as st

from techdocsbench import clean_markdown

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = DATA_DIR / "results"
LOG_FILE = RESULTS_DIR / "human_eval_results.csv"

st.set_page_config(layout="centered", page_title="TechDocsBench: Human Review")


def iter_result_files() -> Iterable[Path]:
    if not RESULTS_DIR.exists():
        return []
    return sorted(RESULTS_DIR.glob("results_*.jsonl"))


def resolve_artifact_path(raw_path: str) -> Optional[Path]:
    if not raw_path:
        return None
    normalized = Path(raw_path.replace("\\\\", "/").replace("\\", "/")).expanduser()
    candidates = [
        normalized,
        BASE_DIR / normalized,
        DATA_DIR / normalized,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


@st.cache_data
def load_all_results():
    data_map = {}
    files = list(iter_result_files())
    all_models = set()
    temp_list = []

    for file in files:
        with file.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    item = json.loads(line)
                    temp_list.append(item)
                    all_models.add(item["model_name"])
                except Exception:
                    continue

    sorted_models = sorted(list(all_models))
    model_mapping = {m: f"Модель {chr(65 + i)}" for i, m in enumerate(sorted_models)}

    unique_ids = []
    for item in temp_list:
        ex_id = item["meta"]["id"]
        if ex_id not in data_map:
            unique_ids.append(ex_id)
            data_map[ex_id] = {
                "title": item["meta"]["original_title"],
                "input": item["input"],
                "reference": item["reference"],
                "task": item["task"],
                "outputs": {},
            }
        data_map[ex_id]["outputs"][item["model_name"]] = item["model_output"]

    case_navigation = {ex_id: f"Кейс №{i+1}" for i, ex_id in enumerate(unique_ids)}
    return data_map, model_mapping, case_navigation, unique_ids


data, model_labels, case_nav, ordered_ids = load_all_results()
if not ordered_ids:
    st.sidebar.warning("Результаты не найдены. Скопируйте файлы results_*.jsonl в каталог data/results.")
    st.stop()

# --- SIDEBAR ---
st.sidebar.title("Выбор кейсов")
if LOG_FILE.exists():
    try:
        evaluated_ids = pd.read_csv(LOG_FILE)["example_id"].unique().tolist()
    except Exception:
        evaluated_ids = []
else:
    evaluated_ids = []

default_index = 0
for i, ex_id in enumerate(ordered_ids):
    if ex_id not in evaluated_ids:
        default_index = i
        break


def label_maker(ex_id: str) -> str:
    status = "✅" if ex_id in evaluated_ids else "⏳"
    return f"{status} {case_nav[ex_id]}: {data[ex_id]['title']}"


selected_id = st.sidebar.selectbox("Пример", ordered_ids, index=default_index, format_func=label_maker)

st.sidebar.divider()
st.sidebar.subheader("Выгрузка результатов")

if LOG_FILE.exists():
    with LOG_FILE.open("rb") as file:
        st.sidebar.download_button(
            label="Скачать CSV с оценками",
            data=file,
            file_name="benchmark_results_export.csv",
            mime="text/csv",
            help="Скачать накопленные оценки коллег.",
        )

    if st.sidebar.button("Удалить текущие оценки", type="secondary"):
        if st.sidebar.checkbox("Я подтверждаю удаление файла"):
            LOG_FILE.unlink()
            st.rerun()
else:
    st.sidebar.info("Файл с оценками появится после первого сохранения.")

# --- CONTENT ---
item = data[selected_id]
is_api = item["task"] == "api_gen"
st.title(f"{case_nav[selected_id]}: {item['title']}")

if item["task"] == "rewriting":
    st.subheader("Исходный текст")
    st.markdown(clean_markdown(item["reference"]))
else:
    t1, t2 = st.tabs(["Скриншот/API-ручка", "Эталонный ответ"])
    with t1:
        raw_path = (item["input"] or "").strip()
        resolved_path = resolve_artifact_path(raw_path)
        lower = raw_path.lower()
        if resolved_path and lower.endswith(".png"):
            st.image(str(resolved_path), width="stretch")
        elif resolved_path and lower.endswith(".md"):
            with resolved_path.open("r", encoding="utf-8") as f:
                st.code(f.read(), language="markdown")
        else:
            st.info(raw_path or "Нет вложений")
    with t2:
        st.markdown(clean_markdown(item["reference"], is_api=is_api))

st.divider()

st.subheader("Ответы моделей")
for m_name in sorted(list(item["outputs"].keys())):
    label = model_labels[m_name]
    with st.expander(label, expanded=True):
        st.markdown(clean_markdown(item["outputs"][m_name], is_api=is_api))

st.divider()

# --- INPUT FORM ---
with st.form(key=f"f_{selected_id}"):
    st.write("Оценка (1-5):")
    criteria = ["Ясность", "Точность", "Полнота", "Единообразие", "Структура", "Избыточность"]
    available_models = sorted(list(item["outputs"].keys()))

    cols = st.columns([1.5] + [1] * len(available_models))
    cols[0].write("**Критерий**")
    for i, m_name in enumerate(available_models):
        cols[i + 1].write(f"**{model_labels[m_name]}**")

    scores = {}
    for crit in criteria:
        row = st.columns([1.5] + [1] * len(available_models))
        row[0].write(crit)
        for i, m_name in enumerate(available_models):
            if m_name not in scores:
                scores[m_name] = {}
            scores[m_name][crit] = row[i + 1].selectbox(
                "B", [1, 2, 3, 4, 5], index=4, key=f"s_{selected_id}_{m_name}_{crit}", label_visibility="collapsed"
            )

    comment = st.text_area("Комментарий", key=f"comm_{selected_id}")
    if st.form_submit_button("Сохранить оценки"):
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        recs = []
        for m_name, scs in scores.items():
            d = {"example_id": selected_id, "model": m_name, "comment": comment}
            d.update(scs)
            recs.append(d)
        pd.DataFrame(recs).to_csv(LOG_FILE, mode="a", index=False, header=not LOG_FILE.exists())
        st.cache_data.clear()
        st.rerun()

# TechDocsBench

TechDocsBench — это бенчмарк для проверки качества технической документации, которую генерируют большие языковые модели. Репозиторий включает эталонные данные, Streamlit-приложение для ручной проверки, скрипт запуска генераций и LLM‑судью.

## Структура

```
data/
  apis/              # описания API-ручек
  golden_set/        # эталонные ответы
  images/            # скриншоты интерфейса
  datasets/          # исходные JSONL с заданиями
  results/           # результаты генераций и CSV с оценками
prompts/             # sys_prompt.md и judge_prompt.md
src/
  app.py             # Streamlit UI
  bench_start.py     # запуск генераций через OpenRouter
  run_judge.py       # автоматическая проверка результатов
  techdocsbench/     # общие утилиты
tests/               # pytest-набор для утилит
requirements.txt
```

## Быстрый старт

1. Установите зависимости: `pip install -r requirements.txt`.
2. Подготовьте переменные окружения `.env` с `OPENROUTER_API_KEY` и при необходимости `JUDGE_MODEL`, `JUDGE_CONCURRENCY`, `BERT_MODEL`.
3. Переместите файлы `results_*.jsonl` и `benchmark_final_v4.jsonl` в соответствующие папки внутри `data/`, как показано выше.

## Основные команды

1. **Streamlit-приложение**: `streamlit run src/app.py`. Интерфейс читает `data/results/results_*.jsonl` и сохраняет оценки в `data/results/human_eval_results.csv`.
2. **Запуск генераций**: `python src/bench_start.py`. Скрипт берет задания из `data/datasets/benchmark_final_v4.jsonl` и пишет ответы в `data/results/`.
3. **LLM-судья**: `python src/run_judge.py`. Прогоняет все `results_*.jsonl`, считает метрики (ROUGE, BERTScore, читаемость) и сохраняет `final_judge_leaderboard.csv` в `data/results/`.
4. **Тесты**: `pytest` из корня проекта.

При необходимости используйте модуль `techdocsbench` для переиспользования функций очистки Markdown, загрузки промптов и обработки выводов судьи.

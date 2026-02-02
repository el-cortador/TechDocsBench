import json
import os
import re
import asyncio
import aiohttp
import pandas as pd
from tqdm.asyncio import tqdm
from rouge_score import rouge_scorer
from bert_score import score as bert_score_func
from dotenv import load_dotenv

# Загрузка настроек
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
JUDGE_MODEL = "google/gemini-2.5-flash" # Модель-судья
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Ограничение одновременных запросов к судье
semaphore = asyncio.Semaphore(3)

# --- БЛОК 1: МАТЕМАТИЧЕСКИЕ МЕТРИКИ (NLP & READABILITY) ---

def count_syllables_ru(text):
    return len(re.findall(r'[аеёиоуыэюя]', text.lower()))

def calculate_readability(text):
    """Считает индексы Флеша и Ганнинга (адаптация для RU)"""
    if not text or len(text) < 10: return 0, 0
    words = re.findall(r'\w+', text)
    sentences = [s for s in re.split(r'[.!?]+', text) if len(s.strip()) > 0]
    
    if not words or not sentences: return 0, 0
    
    asl = len(words) / len(sentences) # средняя длина предложения
    asw = count_syllables_ru(text) / len(words) # среднее кол-во слогов
    
    # Индекс Флеша (Обознева)
    flesch = 206.835 - (1.3 * asl) - (60.1 * asw)
    # Ганнинг Фог (сложные слова > 4 слогов)
    complex_words = [w for w in words if count_syllables_ru(w) > 4]
    phw = (len(complex_words) / len(words)) * 100
    fog = 0.4 * (asl + phw)
    
    return round(flesch, 2), round(fog, 2)

def get_nlp_metrics(ref, cand):
    """Считает ROUGE-L"""
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=False)
    r_scores = scorer.score(ref, cand)
    return round(r_scores['rougeL'].fmeasure, 3)

# --- БЛОК 2: LLM-JUDGE (GEMINI) ---

# Загружаем промпт судьи
def load_judge_prompt(file_path="judge_prompt.md"):
    if not os.path.exists(file_path):
        print(f"ОШИБКА: Файл {file_path} не найден!")
        exit()
    with open(file_path, "r", encoding="utf-8") as f:
        print(f"Промпт судьи успешно загружен из {file_path}")
        return f.read().strip()

JUDGE_SYSTEM_PROMPT = load_judge_prompt("judge_prompt.md")

async def get_judge_evaluation(session, reference, model_output, input_artifact):
    """Запрос к Gemini-судье через OpenRouter"""
    async with semaphore:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        user_msg = f"АРТЕФАКТ ВВОДА: {input_artifact}\n\nЭТАЛОН: {reference}\n\nОТВЕТ МОДЕЛИ: {model_output}"
        
        payload = {
            "model": JUDGE_MODEL,
            "messages": [
                {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
                {"role": "user", "content": user_msg}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.1
        }

        try:
            async with session.post(API_URL, headers=headers, json=payload) as resp:
                if resp.status == 200:
                    res = await resp.json()
                    return json.loads(res['choices'][0]['message']['content'])
                return None
        except:
            return None

# --- БЛОК 3: ГЛАВНЫЙ ОРКЕСТРАТОР ---

async def run_full_audit():
    # 1. BERTScore инициализация (делаем один раз, так как модель тяжелая)
    print("Инициализация BERTScore (RuBERT)...")
    
    results_files = [f for f in os.listdir('.') if f.startswith('results_') and f.endswith('.jsonl')]
    all_audit_data = []

    async with aiohttp.ClientSession() as session:
        for file in results_files:
            print(f"\nАудит файла: {file}")
            with open(file, 'r', encoding='utf-8') as f:
                items = [json.loads(line) for line in f]

            # Ограничим для теста первыми 5, если нужно, или жахнем все 60
            for item in tqdm(items, desc=f"Анализ {file}"):
                ref = item['reference']
                out = item['model_output']
                
                # Математические метрики
                rouge_l = get_nlp_metrics(ref, out)
                flesch, fog = calculate_readability(out)
                
                # BERTScore (синхронно, так как torch)
                _, _, f1 = bert_score_func([out], [ref], lang="ru", model_type="DeepPavlov/rubert-base-cased", verbose=False)
                bs_score = round(f1.item(), 3)

                # Оценка судьи (асинхронно)
                j_eval = await get_judge_evaluation(session, ref, out, item['input'])
                
                # Сборка итоговой строки
                row = {
                    "id": item['meta']['id'],
                    "model": item['model_name'],
                    "rouge_l": rouge_l,
                    "bert_score": bs_score,
                    "flesch_ru": flesch,
                    "gunning_fog": fog
                }
                
                if j_eval:
                    row.update({
                        "j_accuracy": j_eval['scores']['accuracy'],
                        "j_completeness": j_eval['scores']['completeness'],
                        "j_style": j_eval['scores']['style'],
                        "j_hallucinations": j_eval['scores']['hallucinations'],
                        "j_markdown": j_eval['scores']['markdown'],
                        "j_critique": j_eval['critique']
                    })
                
                all_audit_data.append(row)

    # Сохранение лидерборда
    df = pd.DataFrame(all_audit_data)
    df.to_csv("final_judge_leaderboard.csv", index=False, encoding='utf-8-sig')
    print("\n--- АУДИТ ЗАВЕРШЕН ---")
    print("Результаты в файле final_judge_leaderboard.csv")

if __name__ == "__main__":
    asyncio.run(run_full_audit())
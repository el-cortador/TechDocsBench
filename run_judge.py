import json
import os
import re
import asyncio
import aiohttp
import pandas as pd
import sys
from tqdm.asyncio import tqdm
from rouge_score import rouge_scorer
from bert_score import score as bert_score_func
from dotenv import load_dotenv

# Фикс кириллицы для консоли Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# Загрузка настроек
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
JUDGE_MODEL = "google/gemini-2.5-pro"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

semaphore = asyncio.Semaphore(3)

# --- 1. ЗАГРУЗКА ПРОМПТА СУДЬИ ---
def load_judge_prompt(file_path="judge_prompt.md"):
    if not os.path.exists(file_path):
        print(f"ERROR: File {file_path} not found!")
        exit()
    with open(file_path, "r", encoding="utf-8") as f:
        print(f"Judge prompt loaded from {file_path}")
        return f.read().strip()

JUDGE_SYSTEM_PROMPT = load_judge_prompt("judge_prompt.md")

# --- 2. МЕТРИКИ ЧИТАБЕЛЬНОСТИ ---
def count_syllables_ru(text):
    return len(re.findall(r'[аеёиоуыэюя]', text.lower()))

def calculate_readability(text):
    if not text or len(text) < 10: return 0, 0
    words = re.findall(r'\w+', text)
    sentences = [s for s in re.split(r'[.!?]+', text) if len(s.strip()) > 0]
    if not words or not sentences: return 0, 0
    asl = len(words) / len(sentences)
    asw = count_syllables_ru(text) / len(words)
    flesch = 206.835 - (1.3 * asl) - (60.1 * asw)
    long_words = [w for w in words if count_syllables_ru(w) > 4]
    phw = (len(long_words) / len(words)) * 100
    fog = 0.4 * (asl + phw)
    return round(flesch, 2), round(fog, 2)

# --- 3. ЗАПРОС К СУДЬЕ ---
async def get_judge_evaluation(session, reference, model_output, input_artifact):
    async with semaphore:
        headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
        user_msg = f"INPUT ARTEFACT: {input_artifact}\n\nREFERENCE TEXT:\n{reference}\n\nAI RESPONSE:\n{model_output}"
        
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
            async with session.post(API_URL, headers=headers, json=payload, timeout=90) as resp:
                if resp.status == 200:
                    res = await resp.json()
                    return json.loads(res['choices'][0]['message']['content'])
                return None
        except: return None

# --- 4. ГЛАВНЫЙ ПРОЦЕСС ---
async def run_full_audit():
    print("Initializing BERTScore (Multilingual BERT)...")
    
    # Используем проверенную модель, которая точно есть в словаре слоев bert_score
    BERT_MODEL = "bert-base-multilingual-cased"

    results_files = [f for f in os.listdir('.') if f.startswith('results_') and f.endswith('.jsonl')]
    all_audit_data = []

    async with aiohttp.ClientSession() as session:
        for file in results_files:
            print(f"Auditing file: {file}")
            with open(file, 'r', encoding='utf-8') as f:
                items = [json.loads(line) for line in f]

            # Полоска прогресса
            pbar = tqdm(items, desc=f"Processing {file}")
            
            for item in pbar:
                ref = item['reference']
                out = item['model_output']
                
                # NLP метрики
                scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=False)
                rouge_l = round(scorer.score(ref, out)['rougeL'].fmeasure, 3)
                
                flesch, fog = calculate_readability(out)
                
                # BERTScore
                try:
                    _, _, f1 = bert_score_func([out], [ref], lang="ru", model_type=BERT_MODEL, verbose=False)
                    bs_score = round(f1.item(), 3)
                except:
                    bs_score = 0.0

                # Оценка судьи
                j_eval = await get_judge_evaluation(session, ref, out, item['input'])
                
                row = {
                    "id": item['meta']['id'],
                    "model": item['model_name'],
                    "rouge_l": rouge_l,
                    "bert_score": bs_score,
                    "flesch_ru": flesch,
                    "gunning_fog": fog
                }
                
                if j_eval and "scores" in j_eval:
                    row.update({
                        "j_clarity": j_eval['scores'].get('clarity', 0),
                        "j_accuracy": j_eval['scores'].get('accuracy', 0),
                        "j_completeness": j_eval['scores'].get('completeness', 0),
                        "j_structure": j_eval['scores'].get('structure', 0),
                        "j_uniformity": j_eval['scores'].get('uniformity', 0),
                        "j_redundance": j_eval['scores'].get('redundance', 0),
                        "j_hallucinations": j_eval['scores'].get('hallucinations', 0),
                        "j_markdown": j_eval['scores'].get('markdown', 0),
                        "j_critique": j_eval.get('critique', "")
                    })
                
                all_audit_data.append(row)

    df = pd.DataFrame(all_audit_data)
    df.to_csv("final_judge_leaderboard.csv", index=False, encoding='utf-8-sig')
    print("\n>>> AUDIT COMPLETED. Results saved to final_judge_leaderboard.csv")

if __name__ == "__main__":
    asyncio.run(run_full_audit())
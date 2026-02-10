import asyncio
import json
import os
from pathlib import Path
from typing import Optional

import aiohttp
from dotenv import load_dotenv
from tqdm.asyncio import tqdm

from techdocsbench import encode_image_to_base64, load_system_prompt

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATASET_PATH = DATA_DIR / "datasets" / "benchmark_final_v4.jsonl"
PROMPTS_DIR = BASE_DIR / "prompts"
RESULTS_DIR = DATA_DIR / "results"

# --- 1. Initialization ---
print(">>> Script starting...")
load_dotenv()

# Cleaning api key from occasional spaces or quotes
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip().replace('"', '').replace("'", "")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

if not OPENROUTER_API_KEY:
    print("ERROR: API key not found in .env file!")
    exit()
else:
    print(f"Key loaded (starts with {OPENROUTER_API_KEY[:8]}...)")

# --- 2. Prompt uploading ---
SYSTEM_PROMPT = load_system_prompt(PROMPTS_DIR / "sys_prompt.md")

# Model IDs for OpenRouter
MODELS_TO_TEST = [
    "openai/gpt-5.2",
    "anthropic/claude-opus-4.5",
    "google/gemini-3-pro-preview",
    "qwen/qwen3-vl-8b-instruct",
    "meta-llama/llama-4-maverick"
]

# Limiting simultaneous requests
semaphore = asyncio.Semaphore(3)

def resolve_input_path(raw_path: str) -> Optional[Path]:
    if not raw_path:
        return None
    normalized = Path(str(raw_path).replace("\\\\", "/").replace("\\", "/")).expanduser()
    candidates = [
        normalized,
        BASE_DIR / normalized,
        DATA_DIR / normalized,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


async def get_model_response(session, model_id, instruction, input_data):
    async with semaphore:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/el-cortador/TechDocsBench",
            "X-Title": "TechDocsBench"
        }

        user_content = [{"type": "text", "text": instruction}]

        # Entry processing
        input_str = str(input_data)
        lower = input_str.lower()
        if lower.endswith(".png"):
            artifact_path = resolve_input_path(input_str)
            base64_image = encode_image_to_base64(artifact_path) if artifact_path else None
            if base64_image:
                user_content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"}
                })
            else:
                return f"ERROR: Image missing at {input_str}"
        elif lower.endswith(".md"):
            artifact_path = resolve_input_path(input_str)
            if artifact_path:
                with artifact_path.open('r', encoding='utf-8') as f:
                    user_content.append({"type": "text", "text": f"SPECIFICATION:\n{f.read()}"})
            else:
                return f"ERROR: MD file missing at {input_str}"
        else:
            user_content.append({"type": "text", "text": f"INPUT TEXT:\n{input_str}"})

        payload = {
            "model": model_id,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.2
        }

        try:
            async with session.post(API_URL, headers=headers, json=payload, timeout=90) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result['choices'][0]['message']['content']
                else:
                    err_text = await resp.text()
                    return f"API ERROR {resp.status}: {err_text}"
        except Exception as e:
            return f"CONNECTION ERROR: {str(e)}"

async def process_dataset():
    if not DATASET_PATH.exists():
        print(f"ERROR: Dataset file {DATASET_PATH} not found!")
        return

    with DATASET_PATH.open('r', encoding='utf-8') as f:
        items = [json.loads(line) for line in f]
    
    print(f"Dataset loaded: {len(items)} examples.")

    async with aiohttp.ClientSession() as session:
        for model_id in MODELS_TO_TEST:
            model_short_name = model_id.split('/')[-1]
            RESULTS_DIR.mkdir(parents=True, exist_ok=True)
            output_path = RESULTS_DIR / f"results_{model_short_name}.jsonl"
            
            print(f"--- Launching: {model_id} ---")
            
            tasks = [get_model_response(session, model_id, item['instruction'], item['input']) for item in items]
            
            responses = await tqdm.gather(*tasks, desc=f"Testing {model_short_name}")
            
            with output_path.open('w', encoding='utf-8') as out_f:
                for item, ai_answer in zip(items, responses):
                    result = item.copy()
                    result['model_output'] = ai_answer
                    result['model_name'] = model_id
                    out_f.write(json.dumps(result, ensure_ascii=False) + '\n')
            
            print(f"Results saved to {output_path}")

if __name__ == "__main__":
    try:
        asyncio.run(process_dataset())
    except KeyboardInterrupt:
        print("\nStopped by user.")
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")

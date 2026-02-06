import json
import os
import base64
import asyncio
import aiohttp
from tqdm.asyncio import tqdm
from dotenv import load_dotenv

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
def load_system_prompt(file_path="sys_prompt.md"):
    if not os.path.exists(file_path):
        print(f"WARNING: File {file_path} not found. Using default prompt.")
        return "You are a technical writer."
    with open(file_path, "r", encoding="utf-8") as f:
        print(f"System prompt loaded from {file_path}")
        return f.read().strip()

SYSTEM_PROMPT = load_system_prompt()

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

def encode_image(image_path):
    try:
        if not os.path.exists(image_path):
            return None
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error encoding image {image_path}: {e}")
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
        if input_str.endswith(".png"):
            base64_image = encode_image(input_str)
            if base64_image:
                user_content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"}
                })
            else:
                return f"ERROR: Image missing at {input_str}"
        elif input_str.endswith(".md"):
            if os.path.exists(input_str):
                with open(input_str, 'r', encoding='utf-8') as f:
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
    dataset_path = "benchmark_final_v4.jsonl"
    
    if not os.path.exists(dataset_path):
        print(f"ERROR: Dataset file {dataset_path} not found!")
        return

    with open(dataset_path, 'r', encoding='utf-8') as f:
        items = [json.loads(line) for line in f]
    
    print(f"Dataset loaded: {len(items)} examples.")

    async with aiohttp.ClientSession() as session:
        for model_id in MODELS_TO_TEST:
            model_short_name = model_id.split('/')[-1]
            output_path = f"results_{model_short_name}.jsonl"
            
            print(f"--- Launching: {model_id} ---")
            
            tasks = [get_model_response(session, model_id, item['instruction'], item['input']) for item in items]
            
            responses = await tqdm.gather(*tasks, desc=f"Testing {model_short_name}")
            
            with open(output_path, 'w', encoding='utf-8') as out_f:
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
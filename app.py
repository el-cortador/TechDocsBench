import streamlit as st
import json
import os
import pandas as pd
import re

# Настройка страницы
st.set_page_config(layout="centered", page_title="TechDocsBench: Human Review")

log_file = "human_eval_results.csv"

# --- УЛУЧШЕННАЯ ФУНКЦИЯ ОБРАБОТКИ ТЕКСТА ---

def clean_markdown(text, is_api=False):
    """
    Построчная обработка текста для исправления списков без поломки таблиц.
    """
    if not isinstance(text, str): return text
    
    lines = text.split('\n')
    cleaned_lines = []
    
    in_code_block = False
    
    for line in lines:
        stripped = line.strip()
        
        # Следим за блоками кода
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            cleaned_lines.append(line)
            continue
            
        if in_code_block:
            cleaned_lines.append(line)
            continue

        # 1. Заменяем спец-буллиты на стандартные только вне таблиц
        if not stripped.startswith('|'):
            for sym in ['●', '○', '•', '·']:
                line = line.replace(sym, '- ')
        
        # 2. Если это API-кейс, мы крайне осторожны с дефисами
        if not is_api:
            # Исправляем ситуацию, когда список прилип к тексту сверху
            if stripped.startswith('- ') or re.match(r'^\d+\.', stripped):
                if cleaned_lines and cleaned_lines[-1].strip() != "":
                    cleaned_lines.append("") # Добавляем пустую строку перед списком
        
        cleaned_lines.append(line)
        
    return "\n".join(cleaned_lines)

@st.cache_data
def load_all_results():
    data_map = {}
    files = [f for f in os.listdir('.') if f.startswith('results_') and f.endswith('.jsonl')]
    all_models = set()
    temp_list = []
    
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    item = json.loads(line)
                    temp_list.append(item)
                    all_models.add(item['model_name'])
                except: continue

    sorted_models = sorted(list(all_models))
    model_mapping = {m: f"Модель {chr(65+i)}" for i, m in enumerate(sorted_models)}

    unique_ids = []
    for item in temp_list:
        ex_id = item['meta']['id']
        if ex_id not in data_map:
            unique_ids.append(ex_id)
            data_map[ex_id] = {
                "title": item['meta']['original_title'],
                "input": item['input'],
                "reference": item['reference'],
                "task": item['task'],
                "outputs": {}
            }
        data_map[ex_id]["outputs"][item['model_name']] = item['model_output']
    
    case_navigation = {ex_id: f"Кейс №{i+1}" for i, ex_id in enumerate(unique_ids)}
    return data_map, model_mapping, case_navigation, unique_ids

data, model_labels, case_nav, ordered_ids = load_all_results()

# --- САЙДБАР ---
st.sidebar.title("Выбор кейсов")
if os.path.exists(log_file):
    try:
        evaluated_ids = pd.read_csv(log_file)['example_id'].unique().tolist()
    except: evaluated_ids = []
else: evaluated_ids = []

default_index = 0
for i, ex_id in enumerate(ordered_ids):
    if ex_id not in evaluated_ids:
        default_index = i
        break

def label_maker(ex_id):
    status = "✅" if ex_id in evaluated_ids else "⏳"
    return f"{status} {case_nav[ex_id]}: {data[ex_id]['title']}"

selected_id = st.sidebar.selectbox("Пример", ordered_ids, index=default_index, format_func=label_maker)

st.sidebar.divider()
if os.path.exists(log_file):
    with open(log_file, "rb") as file:
        st.sidebar.download_button("📥 Скачать результаты", file, "results.csv", "text/csv")

# --- КОНТЕНТ ---
item = data[selected_id]
is_api = (item['task'] == 'api_gen')
st.title(f"{case_nav[selected_id]}: {item['title']}")

if item['task'] == 'rewriting':
    st.subheader("✅ Исходный текст")
    st.markdown(clean_markdown(item['reference']))
else:
    t1, t2 = st.tabs(["📥 Артефакт", "✅ Исходный текст"])
    with t1:
        path = item['input'].replace('\\\\', '/').replace('\\', '/').strip()
        if path.lower().endswith('.png'):
            st.image(path, use_container_width=True) # Картинка на всю ширину вкладки
        elif path.lower().endswith('.md'):
            with open(path, 'r', encoding='utf-8') as f:
                st.code(f.read(), language='markdown')
        else: st.info(path)
    with t2:
        st.markdown(clean_markdown(item['reference'], is_api=is_api))

st.divider()

st.subheader("🤖 Ответы моделей")
for m_name in sorted(list(item['outputs'].keys())):
    label = model_labels[m_name]
    with st.expander(f"📄 {label}", expanded=True):
        # Показываем ПОЛНЫЙ текст без обрезания
        st.markdown(clean_markdown(item['outputs'][m_name], is_api=is_api))

st.divider()

# --- ФОРМА ---
with st.form(key=f"f_{selected_id}"):
    st.write("Оценка (1-5):")
    criteria = ["Ясность", "Точность", "Полнота", "Единообразие", "Структура", "Избыточность"]
    available_models = sorted(list(item['outputs'].keys()))
    
    cols = st.columns([1.5] + [1]*len(available_models))
    cols[0].write("**Критерий**")
    for i, m_name in enumerate(available_models):
        cols[i+1].write(f"**{model_labels[m_name]}**")
    
    scores = {}
    for crit in criteria:
        r = st.columns([1.5] + [1]*len(available_models))
        r[0].write(crit)
        for i, m_name in enumerate(available_models):
            if m_name not in scores: scores[m_name] = {}
            scores[m_name][crit] = r[i+1].selectbox("B", [1,2,3,4,5], index=4, key=f"s_{selected_id}_{m_name}_{crit}", label_visibility="collapsed")
            
    comment = st.text_area("Комментарий", key=f"comm_{selected_id}")
    if st.form_submit_button("🚀 Сохранить оценки"):
        recs = []
        for m_name, scs in scores.items():
            d = {"example_id": selected_id, "model": m_name, "comment": comment}
            d.update(scs)
            recs.append(d)
        pd.DataFrame(recs).to_csv(log_file, mode='a', index=False, header=not os.path.exists(log_file))
        st.cache_data.clear()
        st.rerun()
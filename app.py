import streamlit as st
import json
import os
import pandas as pd
import re

# Настройка страницы
st.set_page_config(layout="centered", page_title="TechDocsBench: Human Review")

log_file = "human_eval_results.csv"

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---

def smart_fix_markdown(text, is_api=False):
    """
    Интеллектуальное исправление.
    Для API (is_api=True) - щадящий режим, чтобы не ломать таблицы.
    Для остальных - стандартный режим для списков.
    """
    if not isinstance(text, str): return text
    
    # Общая очистка для всех
    for sym in ['●', '○', '•', '·']:
        text = text.replace(sym, '- ')
    text = text.replace('\t', ' ')

    if is_api:
        # Для API только гарантируем пустую строку ПЕРЕД таблицей, если её нет
        # Это часто чинит рендеринг таблиц в Streamlit
        text = re.sub(r'([^\n])\n\|', r'\1\n\n|', text)
    else:
        # Для обычных текстов - фиксим слипшиеся списки
        text = re.sub(r'([^\n])\s+-\s+', r'\1\n\n- ', text)
        text = re.sub(r'([^\n])\s+(\d+\.)\s+', r'\1\n\n\2 ', text)
        text = re.sub(r'([^\n])\n(-|\d+\.)', r'\1\n\n\2', text)
    
    # Общая финальная очистка
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def get_evaluated_ids():
    if os.path.exists(log_file):
        try:
            df = pd.read_csv(log_file)
            return df['example_id'].unique().tolist()
        except: return []
    return []

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
evaluated_ids = get_evaluated_ids()
default_index = 0
for i, ex_id in enumerate(ordered_ids):
    if ex_id not in evaluated_ids:
        default_index = i
        break

def label_maker(ex_id):
    status = "✅" if ex_id in evaluated_ids else "⏳"
    return f"{status} {case_nav[ex_id]}: {data[ex_id]['title']}"

selected_id = st.sidebar.selectbox("Кейс", ordered_ids, index=default_index, format_func=label_maker)

st.sidebar.divider()
st.sidebar.subheader("Выгрузка результатов")
if os.path.exists(log_file):
    with open(log_file, "rb") as file:
        st.sidebar.download_button("Скачать CSV", file, "results.csv", "text/csv")

# --- ВЕРХНИЙ БЛОК: ИСХОДНЫЕ ДАННЫЕ ---
item = data[selected_id]
is_api_task = (item['task'] == 'api_gen')
st.title(f"{case_nav[selected_id]}: {item['title']}")

if item['task'] == 'rewriting':
    st.subheader("Исходный текст")
    with st.container(border=True):
        st.markdown(smart_fix_markdown(item['reference']))
else:
    t1, t2 = st.tabs(["Артефакт (скриншот/эндпоинт))", "Исходный текст"])
    with t1:
        path = item['input'].replace('\\\\', '/').replace('\\', '/').strip()
        if path.lower().endswith('.png'):
            if os.path.exists(path):
                st.image(path, width=1300)
                st.caption("Нажмите для увеличения")
            else: st.error("Image missing")
        elif path.lower().endswith('.md'):
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    st.code(f.read(), language='markdown')
        else: st.info(path)
    with t2:
        st.markdown(smart_fix_markdown(item['reference'], is_api=is_api_task))

st.divider()

# --- СРЕДНИЙ БЛОК: РЕЗУЛЬТАТЫ ГЕНЕРАЦИИ ---
st.subheader("Результаты генерации")
for m_name in sorted(list(item['outputs'].keys())):
    label = model_labels[m_name]
    with st.expander(f"📄 {label}", expanded=True):
        st.markdown(smart_fix_markdown(item['outputs'][m_name], is_api=is_api_task))

st.divider()

# --- НИЖНЯЯ ПАНЕЛЬ: ОЦЕНКА ---
st.subheader("Панель оценки")
with st.form(key=f"f_{selected_id}"):
    criteria = ["Ясность", "Точность", "Полнота", "Единообразие", "Структура", "Избыточность"]
    available_models = sorted(list(item['outputs'].keys()))
    
    cols = st.columns([1.5] + [1]*len(available_models))
    cols[0].write("**Критерий**")
    for i, m_name in enumerate(available_models):
        cols[i+1].write(f"**{model_labels[m_name]}**")
    
    scores_to_save = {}
    for crit in criteria:
        r = st.columns([1.5] + [1]*len(available_models))
        r[0].write(crit)
        for i, m_name in enumerate(available_models):
            if m_name not in scores_to_save: scores_to_save[m_name] = {}
            scores_to_save[m_name][crit] = r[i+1].selectbox("B", [1,2,3,4,5], index=4, key=f"s_{selected_id}_{m_name}_{crit}", label_visibility="collapsed")
            
    comment = st.text_area("Комментарий", key=f"comm_{selected_id}")
    if st.form_submit_button("🚀 Сохранить оценки"):
        recs = []
        for m_name, scs in scores_to_save.items():
            d = {"example_id": selected_id, "model_label": model_labels[m_name], "real_model": m_name, "comment": comment}
            d.update(scs)
            recs.append(d)
        pd.DataFrame(recs).to_csv(log_file, mode='a', index=False, header=not os.path.exists(log_file))
        st.cache_data.clear()
        st.rerun()
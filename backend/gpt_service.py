import openai
from config import OPENAI_API_KEY
import logging

openai.api_key = OPENAI_API_KEY

def _log_usage(r):
    try:
        u = r["usage"]
        logging.info(f"[GPT] prompt={u['prompt_tokens']} | completion={u['completion_tokens']} | total={u['total_tokens']}")
    except Exception:
        pass

def gpt_interpret(numbers: dict) -> str:
    prompt = (
        "Ты — профессиональный нумеролог с опытом более 20 лет. "
        "Твоя задача — сделать вдохновляющую и понятную интерпретацию чисел человека.\n\n"
        "Формат ответа:\n"
        "1) Для каждого числа (судьбы, души, личности, зрелости) — отдельный абзац.\n"
        "- Сначала объясни, что означает число.\n"
        "- Дай сильные стороны, таланты.\n"
        "- Укажи слабые места, над чем стоит работать.\n"
        "2) В конце сделай общий вывод о характере и жизненном пути человека.\n"
        "3) Пиши в стиле лёгкой эзотерики (дружелюбно, мудро, но без лишней мистики).\n\n"
        f"Число судьбы: {numbers['судьбы']}\n"
        f"Число души: {numbers['души']}\n"
        f"Число личности: {numbers['личности']}\n"
        f"Число зрелости: {numbers['зрелости']}\n"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600
    )

    usage = response.usage
    print(f"[GPT] Prompt tokens: {usage['prompt_tokens']} | Completion tokens: {usage['completion_tokens']} | Total: {usage['total_tokens']}")

    return response.choices[0].message["content"]


def gpt_compatibility(result: dict) -> str:
    prompt = (
        "Ты — нумеролог и консультант по отношениям. "
        "Нужно проанализировать совместимость двух людей по их числам.\n\n"
        "Формат ответа:\n"
        "- 🔮 Сильные стороны их союза\n"
        "- ⚡ Возможные трудности\n"
        "- 🌟 Советы для гармоничных отношений\n\n"
        "Пиши простым языком, с лёгкой мистической атмосферой.\n\n"
        f"Числа первого: {result['person1']}\n"
        f"Числа второго: {result['person2']}\n"
        f"Разница по числам: {result['разница']}\n"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=700
    )

    usage = response.usage
    print(f"[GPT] Prompt tokens: {usage['prompt_tokens']} | Completion tokens: {usage['completion_tokens']} | Total: {usage['total_tokens']}")

    return response.choices[0].message["content"]

def gpt_natal(payload: dict) -> str:
    # payload: {"date":"DD.MM.YYYY","time":"HH:MM","place":"Город, страна"}
    prompt = (
        "Ты — астролог. На основе даты, времени и места рождения дай мягкий, вдохновляющий разбор натальной карты.\n"
        "Не используй точные градусы, работай на уровне планет и домов в общих чертах.\n"
        "Структура: Личность, Карьера/деньги, Отношения, Ресурсы и советы.\n\n"
        f"Дата: {payload.get('date','')}\n"
        f"Время: {payload.get('time','')}\n"
        f"Место: {payload.get('place','')}\n"
    )
    r = openai.ChatCompletion.create(model="gpt-4o-mini", messages=[{"role":"user","content":prompt}], max_tokens=750)
    _log_usage(r)
    return r.choices[0].message["content"]

def gpt_horoscope(payload: dict) -> str:
    # payload: {"sign":"Овен", "period":"неделя"|"месяц"}
    prompt = (
        "Ты — астролог. Напиши позитивный, практичный гороскоп без фатализма.\n"
        "Структура: Общий фон, Работа/деньги, Отношения, Здоровье/ресурс, Совет.\n"
        f"Знак: {payload.get('sign','')}, период: {payload.get('period','')}\n"
    )
    r = openai.ChatCompletion.create(model="gpt-4o-mini", messages=[{"role":"user","content":prompt}], max_tokens=500)
    _log_usage(r)
    return r.choices[0].message["content"]

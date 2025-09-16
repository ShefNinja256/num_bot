import logging
from openai import OpenAI
from config import OPENAI_API_KEY

# Инициализация клиента
client = OpenAI(api_key=OPENAI_API_KEY)

# --- Общая функция для логов токенов ---
def _log_usage(r, label="GPT"):
    try:
        usage = r.usage
        logging.info(
            f"[{label}] Prompt: {usage.prompt_tokens} | "
            f"Completion: {usage.completion_tokens} | "
            f"Total: {usage.total_tokens}"
        )
    except Exception as e:
        logging.warning(f"[{label}] Не удалось вывести токены: {e}")

# --- Нумерология одного человека ---
def gpt_interpret(numbers: dict) -> str:
    prompt = (
        "Ты — профессиональный нумеролог с опытом более 20 лет. "
        "Сделай структурированную интерпретацию чисел: сильные стороны, слабые стороны и общий вывод.\n\n"
        f"Число судьбы: {numbers['судьбы']}\n"
        f"Число души: {numbers['души']}\n"
        f"Число личности: {numbers['личности']}\n"
        f"Число зрелости: {numbers['зрелости']}\n"
    )

    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=650
    )

    _log_usage(r, "Interpret")
    return r.choices[0].message.content

# --- Совместимость ---
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

    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )

    _log_usage(r, "Compat")
    return r.choices[0].message.content

# --- Натальная карта ---
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

    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=750
    )

    _log_usage(r, "Natal")
    return r.choices[0].message.content

# --- Гороскоп ---
def gpt_horoscope(payload: dict) -> str:
    # payload: {"sign":"Овен", "period":"неделя"|"месяц"}
    prompt = (
        "Ты — астролог. Напиши позитивный, практичный гороскоп без фатализма.\n"
        "Формат:\n"
        "✨ Общий фон\n"
        "💼 Работа и деньги\n"
        "❤️ Отношения\n"
        "🌱 Здоровье и ресурс\n"
        "🌟 Совет\n\n"
        f"Знак: {payload.get('sign','')}, период: {payload.get('period','')}\n"
    )

    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )

    _log_usage(r, "Horoscope")
    return r.choices[0].message.content

import logging
import requests
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

# --- Гороскоп с Aztro API ---
period_map = {
    "сегодня": "today",
    "завтра": "tomorrow"
    # "неделя" обработаем отдельно
}

def gpt_horoscope(payload: dict) -> str:
    sign_map = {
        "Овен": "aries", "Телец": "taurus", "Близнецы": "gemini", "Рак": "cancer",
        "Лев": "leo", "Дева": "virgo", "Весы": "libra", "Скорпион": "scorpio",
        "Стрелец": "sagittarius", "Козерог": "capricorn", "Водолей": "aquarius", "Рыбы": "pisces"
    }

    sign = sign_map.get(payload.get("sign"), "aries")
    period = payload.get("period", "сегодня")

    if period == "неделя":
        # ⚡ Трюк: берём "сегодня", а GPT просим расширить до недели
        resp = requests.post(f"https://aztro.sameerkumar.website/?sign={sign}&day=today")
        if resp.status_code != 200:
            return "⚠️ Ошибка: не удалось получить данные гороскопа."
        raw = resp.json()

        prompt = (
            f"Данные для гороскопа ({payload.get('sign')}):\n"
            f"Описание: {raw.get('description')}\n"
            f"Совместимость: {raw.get('compatibility')}\n"
            f"Настроение: {raw.get('mood')}\n"
            f"Цвет: {raw.get('color')}\n"
            f"Счастливое число: {raw.get('lucky_number')}\n"
            f"Счастливое время: {raw.get('lucky_time')}\n\n"
            "Сделай подробный гороскоп на 7 дней вперёд. "
            "Разбей по дням недели (Пн, Вт, Ср, ...), указывая общую атмосферу, "
            "работу/деньги, отношения, здоровье и совет."
        )

        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=900
        )
        _log_usage(r, "Horoscope-Week")
        return {
            "date": "неделю",
            "interpretation": r.choices[0].message.content
        }

    else:
        # день = сегодня/завтра
        day_key = period_map.get(period, "today")
        resp = requests.post(f"https://aztro.sameerkumar.website/?sign={sign}&day={day_key}")
        if resp.status_code != 200:
            return "⚠️ Ошибка: не удалось получить данные гороскопа."
        raw = resp.json()

        prompt = (
            f"Гороскоп для {payload.get('sign')} ({period}, {raw.get('current_date')}):\n\n"
            f"Описание: {raw.get('description')}\n"
            f"Совместимость: {raw.get('compatibility')}\n"
            f"Настроение: {raw.get('mood')}\n"
            f"Цвет: {raw.get('color')}\n"
            f"Счастливое число: {raw.get('lucky_number')}\n"
            f"Счастливое время: {raw.get('lucky_time')}\n\n"
            "Сделай красивый гороскоп в формате:\n"
            "✨ Общая атмосфера\n"
            "💼 Работа и деньги\n"
            "❤️ Отношения\n"
            "🌱 Здоровье и ресурс\n"
            "🌟 Совет\n\n"
            "Пиши живо и позитивно."
        )

        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600
        )
        _log_usage(r, "Horoscope")
        return {
            "date": raw.get("current_date"),
            "interpretation": r.choices[0].message.content
        }

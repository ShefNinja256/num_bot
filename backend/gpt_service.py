import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

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

from aiogram import types
from datetime import datetime
from numerology import calc_numbers, calc_compatibility
from gpt_service import gpt_interpret, gpt_compatibility


def validate_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return True
    except ValueError:
        return False


async def handle_date(message: types.Message):
    if not validate_date(message.text):
        await message.answer("Пожалуйста, введи дату в формате ДД.ММ.ГГГГ")
        return

    numbers = calc_numbers(message.text)
    interpretation = gpt_interpret(numbers)

    text = (
        f"📅 Дата: {message.text}\n"
        f"🔢 Число судьбы: {numbers['судьбы']}\n"
        f"💖 Число души: {numbers['души']}\n"
        f"😎 Число личности: {numbers['личности']}\n"
        f"🌟 Число зрелости: {numbers['зрелости']}\n\n"
        f"{interpretation}"
    )

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🔄 Ещё раз", callback_data="retry_single"))

    await message.answer(text, reply_markup=kb)


async def handle_compat(message: types.Message):
    try:
        date1, date2 = message.text.split()
        if not validate_date(date1) or not validate_date(date2):
            raise ValueError

        result = calc_compatibility(date1, date2)
        interpretation = gpt_compatibility(result)

        text = (
            f"👩 Женщина: {date1} → {result['person1']}\n"
            f"👨 Мужчина: {date2} → {result['person2']}\n\n"
            f"{interpretation}"
        )

        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("❤️ Проверить другую пару", callback_data="retry_compat"))

        await message.answer(text, reply_markup=kb)

    except Exception:
        await message.answer("Введи две даты через пробел, например:\n15.09.1992 20.07.1995")

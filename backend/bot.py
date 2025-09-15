import logging
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
import handlers

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


# --- Главное меню ---
def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🔮 Узнать своё число")
    kb.add("❤️ Проверить совместимость")
    return kb


@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.answer(
        "Привет! Я нумеролог-бот 🔮\n\n"
        "Выбери действие с помощью кнопок ниже 👇",
        reply_markup=main_menu()
    )


@dp.message_handler(lambda msg: msg.text == "🔮 Узнать своё число")
async def ask_date(message: types.Message):
    await message.answer("Введи дату рождения в формате ДД.ММ.ГГГГ")


@dp.message_handler(lambda msg: msg.text == "❤️ Проверить совместимость")
async def ask_dates(message: types.Message):
    await message.answer(
        "Введите две даты через пробел.\n"
        "Сначала дату рождения женщины 👩, потом мужчины 👨.\n\n"
        "Пример: 15.09.1992 20.07.1995"
    )


@dp.callback_query_handler(lambda c: c.data == "retry_single")
async def retry_single(call: types.CallbackQuery):
    await call.message.answer("Введи новую дату рождения в формате ДД.ММ.ГГГГ")
    await call.answer()  # убираем «часики»


@dp.callback_query_handler(lambda c: c.data == "retry_compat")
async def retry_compat(call: types.CallbackQuery):
    await call.message.answer(
        "Введите две новые даты через пробел.\n"
        "Сначала женщину 👩, потом мужчину 👨."
    )
    await call.answer()


@dp.message_handler()
async def router(message: types.Message):
    if " " in message.text.strip():
        await handlers.handle_compat(message)
    else:
        await handlers.handle_date(message)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

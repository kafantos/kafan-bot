print("RUNNING C:\\kafan_bot\\bot.py - VERSION TEST")

import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message

TOKEN = 8294719928:AAFu8J6iA6No5lBk8VNuGbuYRB3EczR33io

bot = Bot(token=TOKEN)
dp = Dispatcher()

menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📸 Отправить фото", callback_data="send_photo")],
    [InlineKeyboardButton(text="📂 Примеры работ", callback_data="examples")],
    [InlineKeyboardButton(text="💳 Тарифы", callback_data="pricing")],
    [InlineKeyboardButton(text="🆘 Поддержка", callback_data="support")],
])

@dp.message(CommandStart())
async def on_start(message: Message):
    await message.answer(
        "Привет! Я **kafan PRO**.\n\n"
        "Я сделаю для тебя фото на документы мечты 🫶\n"
        "Выбери действие ниже 👇",
        reply_markup=menu_kb,
        parse_mode="Markdown",
    )

@dp.callback_query(F.data == "send_photo")
async def cb_send_photo(call: CallbackQuery):
    await call.message.answer("Пришлите фото (как изображение, не как файл).")
    await call.answer()

@dp.callback_query(F.data == "examples")
async def cb_examples(call: CallbackQuery):
    await call.message.answer("Вот примеры наших работ:")
    for url in [
        "https://i.imgur.com/FKv58z.jpeg",
        "https://i.imgur.com/joWbVb4.jpeg",
    ]:
        await call.message.answer_photo(photo=url)
    await call.answer()

@dp.callback_query(F.data == "pricing")
async def cb_pricing(call: CallbackQuery):
    await call.message.answer("Тарифы скоро добавим. Пока тестовый режим ✅")
    await call.answer()

@dp.callback_query(F.data == "support")
async def cb_support(call: CallbackQuery):
    await call.message.answer("Поддержка: напишите сюда ваш вопрос.")
    await call.answer()

@dp.message(F.photo)
async def got_photo(message: Message):
    await message.answer("Фото получено! Скоро добавим обработку 😊")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


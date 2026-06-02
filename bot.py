import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8837878859:AAEy2MfNoCncHJbx4H9oZNb98NtGU4PSv2o"
logging.basicConfig(level=logging.INFO)

PRICE_SECTIONS = {
    "photo_print": {
        "name": "🖼 Фото печать",
        "items": [
            ("10х15 (до 7 шт — 25р/шт)", "20р"),
            ("15х21", "60р"),
            ("21х30 (А4)", "90р"),
            ("Полароид", "35р"),
            ("Самоклейка А4", "100р"),
        ],
    },
    "docs": {
        "name": "🪪 Фото на документы",
        "items": [
            ("1 комплект (1-6 шт)", "350р"),
            ("Доп. комплект", "200р"),
            ("Замена одежды на фото", "100р"),
            ("Электронная версия", "100р"),
        ],
    },
    "canvas": {
        "name": "🎨 Печать на холсте",
        "items": [
            ("20х30", "1500р"), ("30х40", "1800р"), ("35х45", "2100р"),
            ("40х50", "2750р"), ("40х60", "3150р"), ("50х70", "3800р"),
            ("60х80", "4050р"), ("60х90", "4700р"), ("70х90", "5350р"),
            ("70х100", "6400р"), ("80х110", "7450р"), ("90х130", "8800р"),
            ("100х150", "9300р"),
            ("Квадрат 30х30", "1650р"), ("Квадрат 40х40", "2150р"),
            ("Квадрат 50х50", "3550р"), ("Квадрат 60х60", "3900р"),
            ("Квадрат 70х70", "4050р"),
            ("Улучшение качества", "от 500р"),
            ("Собрать в коллаж", "от 400р"),
            ("Ретушь / Фотошоп", "от 300р"),
        ],
    },
    "souvenirs": {
        "name": "🎁 Фото сувениры",
        "items": [
            ("Футболка белая", "1550р"),
            ("Футболка чёрная", "1650р"),
            ("Доп. нанесение", "500р"),
            ("Кружка с фото белая", "500р"),
            ("Кружка хамелеон", "750р"),
            ("Макет для кружки", "от 150р"),
            ("Фото-магнит виниловый", "от 200р"),
            ("Фото-магнит акриловый", "от 150р"),
            ("Шоколадка именная 100г", "450р"),
            ("Авто-обложка из кожи", "1450р"),
            ("Брелок с госномером", "450р"),
        ],
    },
    "restoration": {
        "name": "🔧 Реставрация и прочее",
        "items": [
            ("Реставрация фото", "от 350р"),
            ("Услуги фотошопа", "от 100р"),
            ("Металлическая 15х21", "850р"),
            ("Металлическая 20х28", "950р"),
            ("Ламинирование", "100р"),
            ("Сканирование", "35р"),
            ("Ксерокопия", "10р"),
            ("Брошюровка", "от 200р"),
            ("Макет для визиток", "от 350р"),
            ("Макет для баннеров", "от 500р"),
            ("Презентация 10 слайдов", "от 500р"),
        ],
    },
    "paper": {
        "name": "🖨 Простая бумага",
        "items": [
            ("Ч/Б текст", "10р"),
            ("Ч/Б изображение", "20р"),
            ("Цветная печать", "25р"),
        ],
    },
}

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Цены и услуги", callback_data="prices")],
        [InlineKeyboardButton("📍 Адреса и время работы", callback_data="branches")],
        [InlineKeyboardButton("📞 Связаться / Оформить заказ", callback_data="contact")],
    ])

def prices_menu():
    buttons = [[InlineKeyboardButton(s["name"], callback_data=f"price_{k}")] for k, s in PRICE_SECTIONS.items()]
    buttons.append([InlineKeyboardButton("⬅️ Назад", callback_data="main")])
    return InlineKeyboardMarkup(buttons)

def back_to_prices():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ К категориям", callback_data="prices")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main")],
    ])

def back_to_main():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Главное меню", callback_data="main")]])

def contact_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📍 Репина 143 — WhatsApp", url="https://wa.me/79614994208")],
        [InlineKeyboardButton("📍 Репина 143 — Telegram", url="https://t.me/+79614994208")],
        [InlineKeyboardButton("📍 Репина 143 — MAX", url="https://max.ru/+79614994208")],
        [InlineKeyboardButton("📍 Ленина 308 — Telegram", url="https://t.me/+79331793739")],
        [InlineKeyboardButton("📍 Ленина 308 — MAX", url="https://max.ru/+79331793739")],
        [InlineKeyboardButton("📸 Instagram @kafan_foto", url="https://instagram.com/kafan_foto")],
        [InlineKeyboardButton("🌐 Сайт", url="https://kafan-foto.clients.site")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="main")],
    ])

WELCOME = "👋 Добро пожаловать в Kafan Foto!\n\n📸 Мы делаем:\n• Печать фото и фото на документы\n• Холсты, металлические фото\n• Принты на футболках и кружках\n• Реставрацию и обработку фото\n• Подарки с фото\n\nВыберите что вас интересует 👇"

BRANCHES = (
    "📍 Наши филиалы:\n\n"
    "1. ул. Репина, 143 (2 этаж)\n"
    "📞 +7 (961) 499-42-08\n"
    "🕐 Пн-Сб: 9:00 – 19:00\n"
    "🕐 Вс: 10:00 – 19:00\n\n"
    "2. ул. Ленина, 308с1\n"
    "📞 +7 (928) 011-37-39\n"
    "🕐 Пн-Пт: 9:00 – 19:00\n"
    "🕐 Сб: 12:00 – 18:00\n"
    "🕐 Вс: выходной\n\n"
    "Ждём вас! 😊"
)

CONTACT = (
    "📞 Связаться с нами:\n\n"
    "📍 Репина 143:\n"
    "+7 (961) 499-42-08 — WhatsApp, Telegram, MAX\n\n"
    "📍 Ленина 308:\n"
    "+7 (933) 179-37-39 — Telegram, MAX\n\n"
    "Выберите удобный способ 👇"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME, reply_markup=main_menu())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main":
        await query.edit_message_text(WELCOME, reply_markup=main_menu())
    elif data == "prices":
        await query.edit_message_text("💰 Цены и услуги\n\nВыберите категорию:", reply_markup=prices_menu())
    elif data.startswith("price_"):
        key = data.replace("price_", "")
        section = PRICE_SECTIONS.get(key)
        if section:
            lines = [section["name"] + "\n"]
            for name, price in section["items"]:
                lines.append(f"• {name} — {price}")
            lines.append("\n📞 Для заказа свяжитесь с нами или приходите в филиал!")
            await query.edit_message_text("\n".join(lines), reply_markup=back_to_prices())
    elif data == "branches":
        await query.edit_message_text(BRANCHES, reply_markup=back_to_main())
    elif data == "contact":
        await query.edit_message_text(CONTACT, reply_markup=contact_menu())

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if any(w in text for w in ["цен", "прайс", "стоит", "сколько"]):
        await update.message.reply_text("💰 Выберите категорию:", reply_markup=prices_menu())
    elif any(w in text for w in ["адрес", "где", "находит", "филиал"]):
        await update.message.reply_text(BRANCHES, reply_markup=back_to_main())
    elif any(w in text for w in ["заказ", "напиш", "связ", "контакт", "телефон"]):
        await update.message.reply_text(CONTACT, reply_markup=contact_menu())
    else:
        await update.message.reply_text(WELCOME, reply_markup=main_menu())

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()

import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    # Берем ссылку на твое приложение из переменных Render
    webapp_url = os.getenv("WEBAPP_URL", "https://tarot-bot-q2xr.onrender.com")
    
    # Нейтральная кнопка, чтобы Telegram не забанил бота
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🔮 Зал Оракула", 
            web_app=WebAppInfo(url=webapp_url)
        )]
    ])
    
    await message.answer(
        "👋 Добро пожаловать в Зал Оракула!\n\n"
        "Твой стартовый баланс: 100 ⭐\n"
        "Нажми кнопку ниже, чтобы заглянуть в будущее и испытать удачу.",
        reply_markup=kb
    )

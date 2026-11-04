import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    webapp_url = os.getenv("WEBAPP_URL", "https://tarot-bot-q2xr.onrender.com")
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🔮 Открыть Зал Оракула", 
            web_app=WebAppInfo(url=webapp_url)
        )]
    ])
    
    await message.answer(
        "👋 Добро пожаловать в Зал Оракула!\n\n"
        "Твой стартовый баланс: 100 ★\n"
        "Нажми кнопку ниже, чтобы начать.",
        reply_markup=kb
    )
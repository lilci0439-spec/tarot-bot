from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import os

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎰 Открыть Игры", web_app=WebAppInfo(url=os.getenv("WEBAPP_URL", "https://tarot-bot-q2xr.onrender.com")))]
    ])
    await message.answer("Добро пожаловать в Зал Оракула!\nТвой стартовый баланс: 100 ⭐", reply_markup=kb)

import os
import logging
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice, PreCheckoutQuery, WebAppInfo
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

# Токены
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Клиент OpenAI
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# --- FastAPI для Mini App ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Запускаем бота в фоне
    asyncio.create_task(dp.start_polling(bot))
    yield
    await bot.session.close()

app = FastAPI(lifespan=lifespan)

# Отдаем страницу игры (файл index.html)
@app.get("/", response_class=HTMLResponse)
async def read_index():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Файл index.html не найден"

# --- Логика бота ---
def get_start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Получить предсказание · 50 ⭐", callback_data="predict")],
        [InlineKeyboardButton(text="Открыть игры", web_app=WebAppInfo(url="ВСТАВЬ_СЮДА_ССЫЛКУ_RENDER"))]
    ])

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "🔮 Привет. Я — цифровой оракул.\n"
        "За 50 звёзд я загляну в твоё будущее и дам персональный прогноз.\n"
        "Нажми кнопку ниже, чтобы узнать свою судьбу, или открой игровой центр.",
        reply_markup=get_start_keyboard()
    )

# Обработка кнопки предсказания
@dp.callback_query(F.data == "predict")
async def send_invoice(callback: types.CallbackQuery):
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title="Персональное предсказание",
        description="Развлекательное предсказание, созданное с помощью ИИ.",
        payload="tarot_reading_50",
        currency="XTR",
        prices=[LabeledPrice(label="Прогноз", amount=50)],
        provider_token=""
    )
    await callback.answer()

@dp.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_q: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

@dp.message(F.successful_payment)
async def successful_payment_handler(message: types.Message):
    await message.answer("Оплата прошла. Смотрю в твоё будущее...")
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты — таролог. Пиши мистическим, но понятным языком. Прогноз должен быть на 3-5 предложений."},
                {"role": "user", "content": "Сделай мне расклад на ближайшую неделю."}
            ],
            max_tokens=200
        )
        prediction = response.choices[0].message.content
    except Exception as e:
        prediction = f"Звёзды сегодня молчат... (Ошибка: {e})"
    await message.answer(f"🔮 **Твой прогноз:**\n\n{prediction}", parse_mode="Markdown")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

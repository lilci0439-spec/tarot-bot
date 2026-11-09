from fastapi import APIRouter, Request, HTTPException
from app.database import async_session
from app.models import User
from sqlalchemy import select
import hmac, hashlib, json, os
from urllib.parse import unquote

router = APIRouter()
BOT_TOKEN = os.getenv("BOT_TOKEN")

def validate_telegram_data(init_data: str) -> dict:
    try:
        parsed_data = dict(x.split('=') for x in unquote(init_data).split('&'))
        hash_str = parsed_data.pop('hash')
        data_check_string = '\n'.join(f"{k}={v}" for k, v in sorted(parsed_data.items()))
        secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        if calculated_hash == hash_str: return json.loads(parsed_data['user'])
        return None
    except Exception: return None

@router.get("/api/balance")
async def get_balance(request: Request):
    init_data = request.headers.get("Authorization")
    if not init_data: raise HTTPException(status_code=401)
    
    tg_user = validate_telegram_data(init_data)
    if not tg_user: raise HTTPException(status_code=403)

    user_id = tg_user['id']
    
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            user = User(id=user_id, username=tg_user.get('username'), stars=0, coins=1000)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            
        return {"stars": user.stars, "coins": user.coins}

# Новый эндпоинт: сохранение баланса
@router.post("/api/update_balance")
async def update_balance(request: Request):
    init_data = request.headers.get("Authorization")
    data = await request.json()
    
    if not init_data: raise HTTPException(status_code=401)
    tg_user = validate_telegram_data(init_data)
    if not tg_user: raise HTTPException(status_code=403)

    user_id = tg_user['id']
    new_coins = data.get("coins", 0)
    
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user:
            user.coins = new_coins
            await session.commit()
            return {"status": "ok"}
    return {"status": "error"}
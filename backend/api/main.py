from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database import get_user, init_db, DB_PATH
import sqlite3

app = FastAPI(title="IGOS Trading Server", version="1.0")

@app.on_event("startup")
def startup_event():
    init_db()

class UserRegister(BaseModel):
    telegram_id: int

@app.get("/")
def read_root():
    return {"status": "online", "project": "IGOS Trading Bot API"}

@app.post("/api/v1/register")
def register_user(data: UserRegister):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT OR IGNORE INTO users (telegram_id, is_active, license_type, expires_at)
            VALUES (?, 1, 'FREE', '2026-12-31')
        ''', (data.telegram_id,))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()
    
    user = get_user(data.telegram_id)
    return {"message": "Успешно", "user": user}

@app.get("/api/v1/license/{telegram_id}")
def check_user_license(telegram_id: int):
    user = get_user(telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

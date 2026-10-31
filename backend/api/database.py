import sqlite3
import os

DB_PATH = os.path.join(os.path.expanduser('~'), 'igos', 'backend', 'api', 'igos_users.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Создаем таблицу пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            is_active BOOLEAN DEFAULT 1,
            license_type TEXT DEFAULT 'FREE',
            expires_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_user(telegram_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT telegram_id, is_active, license_type, expires_at FROM users WHERE telegram_id = ?', (telegram_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "telegram_id": row[0],
            "is_active": bool(row[1]),
            "license_type": row[2],
            "expires_at": row[3]
        }
    return None

if __name__ == '__main__':
    init_db()
    print("База данных IGOS успешно инициализирована!")

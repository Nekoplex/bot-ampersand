import aiosqlite

from config import DB_PATH

USERS_TABLE_SQL = """CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    drink INTEGER,
    last_request_date INTEGER
);"""


async def create_tables() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(USERS_TABLE_SQL)
        await db.commit()


async def get_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users WHERE id = ?", (user_id,)) as cur:
            result = await cur.fetchone()
    return result


async def create_user(user_id: int, drink, current_date: int) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO users (id, drink, last_request_date) VALUES (?, ?, ?)",
            (user_id, drink, current_date),
        )
        await db.commit()


async def update_drink_status(user_id: int, drink, current_date: int) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET drink = drink + ?, last_request_date = ? WHERE id = ?",
            (drink, current_date, user_id),
        )
        await db.commit()


async def top_drink_users():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users ORDER BY drink DESC") as cur:
            result = await cur.fetchall()
    return result

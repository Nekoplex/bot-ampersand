import aiosqlite

from config import DB_PATH

USERS_TABLE_SQL = """CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    sailed INTEGER,
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


async def create_user(user_id: int, sailed, current_date: int) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO users (id, sailed, last_request_date) VALUES (?, ?, ?)",
            (user_id, sailed, current_date),
        )
        await db.commit()


async def update_sailed_status(user_id: int, sailed, current_date: int) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET sailed = sailed + ?, last_request_date = ? WHERE id = ?",
            (sailed, current_date, user_id),
        )
        await db.commit()


async def top_sailed_users():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users ORDER BY sailed DESC") as cur:
            result = await cur.fetchall()
    return result

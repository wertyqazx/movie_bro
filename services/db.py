import aiosqlite
from pathlib import Path

_DB_PATH = Path("storage/movies.db")

async def init_db():
    async with aiosqlite.connect(_DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                user_id INTEGER,
                movie_id INTEGER,
                title TEXT,
                poster TEXT,
                PRIMARY KEY (user_id, movie_id)
            )
        """)
        await db.commit()

async def add_favorite(user_id: int, movie_id: int, title: str, poster: str | None):
    async with aiosqlite.connect(_DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO favorites VALUES (?, ?, ?, ?)",
            (user_id, movie_id, title, poster),
        )
        await db.commit()

async def list_favorites(user_id: int) -> list[tuple]:
    async with aiosqlite.connect(_DB_PATH) as db:
        async with db.execute(
            "SELECT movie_id, title, poster FROM favorites WHERE user_id = ?",
            (user_id,),
        ) as cur:
            return await cur.fetchall()

async def remove_favorite(user_id: int, movie_id: int):
    async with aiosqlite.connect(_DB_PATH) as db:
        await db.execute(
            "DELETE FROM favorites WHERE user_id = ? AND movie_id = ?",
            (user_id, movie_id),
        )
        await db.commit()

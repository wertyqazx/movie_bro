from math import ceil
from typing import List

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from services.tmdb import top_rated_movies, get_movie_details, poster_url, get_genres_map
from services.db import add_favorite
from utils.preferences import get_genres

router = Router()
PAGE_SIZE = 10
ABS_LIMIT = 250

@router.message(Command("top250"))
async def top250_cmd(msg: Message):
    await show_page(msg, 0, send_new=True)

@router.callback_query(lambda c: c.data.startswith("tpage:"))
async def navigate(call: CallbackQuery):
    offset = int(call.data.split(":")[1])
    await show_page(call.message, offset, edit=True)
    await call.answer()

@router.callback_query(lambda c: c.data.startswith("tsel:"))
async def select(call: CallbackQuery):
    movie_id = int(call.data.split(":")[1])
    await show_card(call.message, movie_id)
    await call.answer()

@router.callback_query(lambda c: c.data.startswith("tfav:"))
async def add_fav(call: CallbackQuery):
    movie_id = int(call.data.split(":")[1])
    details = await get_movie_details(movie_id)
    await add_favorite(
        user_id=call.from_user.id,
        movie_id=movie_id,
        title=details.get("title", "Без названия"),
        poster=details.get("poster_path") or "",
    )
    await call.answer("Добавлено в избранное ⭐", show_alert=True)

async def collect_top250() -> List[dict]:
    movies = []
    for p in range(1, 14):
        movies.extend(await top_rated_movies(page=p))
        if len(movies) >= ABS_LIMIT:
            break
    return movies[:ABS_LIMIT]

async def show_page(msg: Message, offset: int, *, send_new=False, edit=False):
    movies = await collect_top250()
    selected = get_genres(msg.chat.id)
    if selected:
        movies = [m for m in movies if selected.issubset(set(m.get("genre_ids", [])))]

    if not movies:
        await msg.answer("По выбранным жанрам в Top-250 ничего нет 🤷‍♂️")
        return

    chunk = movies[offset:offset + PAGE_SIZE]
    if not chunk:
        await msg.answer("Достигнут конец списка ✅")
        return

    rows = [
        [InlineKeyboardButton(
            text=f"★{m.get('vote_average', 0):.1f} {m['title']} ({m.get('release_date', '')[:4]})",
            callback_data=f"tsel:{m['id']}"
        )]
        for m in chunk
    ]

    nav = []
    if offset > 0:
        nav.append(InlineKeyboardButton(text="◀️", callback_data=f"tpage:{offset - PAGE_SIZE}"))
    if offset + PAGE_SIZE < len(movies):
        nav.append(InlineKeyboardButton(text="▶️", callback_data=f"tpage:{offset + PAGE_SIZE}"))
    if nav:
        rows.append(nav)

    genres_map = await get_genres_map()
    genre_names = [genres_map.get(g, "") for g in selected]
    genre_str = ", ".join(genre_names) if genre_names else "все жанры"
    text = f"TMDb TOP-250 ({genre_str}) — стр. {offset // PAGE_SIZE + 1} / {ceil(len(movies) / PAGE_SIZE)}"

    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    if send_new:
        await msg.answer(text, reply_markup=markup)
    elif edit:
        await msg.edit_text(text, reply_markup=markup)

async def show_card(msg: Message, movie_id: int):
    details = await get_movie_details(movie_id)
    genres = ", ".join(g["name"] for g in details.get("genres", [])) or "—"
    text = (
        f"<b>{details.get('title')}</b> ({details.get('release_date', '')[:4]})\n"
        f"⭐ {details.get('vote_average', 0):.1f} / 10\n"
        f"<i>{details.get('overview') or 'Без описания.'}</i>\n"
        f"<b>Жанры:</b> {genres}"
    )
    kb = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="⭐ В избранное", callback_data=f"tfav:{movie_id}")
        ]]
    )
    p = poster_url(details.get("poster_path"))
    if p:
        await msg.answer_photo(p, caption=text, reply_markup=kb)
    else:
        await msg.answer(text, reply_markup=kb)

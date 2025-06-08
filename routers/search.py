import urllib.parse

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from services.tmdb import search_movie, get_movie_details, poster_url, get_genres_map
from services.db import add_favorite
from states.search import SearchMovie
from utils.preferences import get_genres

router = Router()
PAGE_SIZE = 5

@router.message(Command("find"))
async def cmd_find(msg: Message, state: FSMContext):
    await msg.answer("Введите название фильма или сериала:")
    await state.set_state(SearchMovie.waiting_for_title)

@router.message(SearchMovie.waiting_for_title)
async def process_title(msg: Message, state: FSMContext):
    query = msg.text.strip()
    await show_results(msg, query, 0, send_new=True)
    await state.clear()

@router.callback_query(lambda c: c.data.startswith("nav:"))
async def navigate(call: CallbackQuery):
    _, offset_str, *query_parts = call.data.split(":")
    offset = int(offset_str)
    query = urllib.parse.unquote(":".join(query_parts))
    await show_results(call.message, query, offset, edit=True)
    await call.answer()

@router.callback_query(lambda c: c.data.startswith("sel:"))
async def select_movie(call: CallbackQuery):
    await show_movie_card(call.message, int(call.data.split(":")[1]))
    await call.answer()

@router.callback_query(lambda c: c.data.startswith("fav:"))
async def add_to_fav(call: CallbackQuery):
    movie_id = int(call.data.split(":")[1])
    details = await get_movie_details(movie_id)
    await add_favorite(
        user_id=call.from_user.id,
        movie_id=movie_id,
        title=details.get("title", "Без названия"),
        poster=details.get("poster_path") or "",
    )
    await call.answer("Добавлено в избранное ⭐", show_alert=True)

async def show_results(target: Message, query: str, offset: int, *, send_new=False, edit=False):
    page = offset // 20 + 1
    results = await search_movie(query, page=page)
    if not results:
        await target.answer("Ничего не найдено 🤷‍♂️")
        return

    selected = get_genres(target.chat.id)
    if selected:
        results = [r for r in results if selected.issubset(set(r.get("genre_ids", [])))]

    idx = offset % 20
    chunk = results[idx:idx + PAGE_SIZE]
    if not chunk:
        await target.answer("По выбранным жанрам ничего нет 🤷‍♂️")
        return

    rows = [
        [InlineKeyboardButton(
            text=f"★{r.get('vote_average', 0):.1f} {r['title']} ({r.get('release_date', '')[:4]})",
            callback_data=f"sel:{r['id']}"
        )]
        for r in chunk
    ]

    nav = []
    if offset > 0:
        nav.append(InlineKeyboardButton(
            text="◀️",
            callback_data=f"nav:{offset - PAGE_SIZE}:{urllib.parse.quote(query)}"
        ))
    if (idx + PAGE_SIZE) < len(results) or len(results) == 20:
        nav.append(InlineKeyboardButton(
            text="▶️",
            callback_data=f"nav:{offset + PAGE_SIZE}:{urllib.parse.quote(query)}"
        ))
    if nav:
        rows.append(nav)

    genres_map = await get_genres_map()
    genre_names = [genres_map.get(g, "") for g in selected]
    genre_str = ", ".join(genre_names) if genre_names else "нет"
    text = f"Результаты для <b>{query}</b> | фильтры: <i>{genre_str}</i>"

    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    if send_new:
        await target.answer(text, reply_markup=markup)
    elif edit:
        await target.edit_text(text, reply_markup=markup)

async def show_movie_card(msg: Message, movie_id: int):
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
            InlineKeyboardButton(text="⭐ В избранное", callback_data=f"fav:{movie_id}")
        ]]
    )
    p = poster_url(details.get("poster_path"))
    if p:
        await msg.answer_photo(p, caption=text, reply_markup=kb)
    else:
        await msg.answer(text, reply_markup=kb)

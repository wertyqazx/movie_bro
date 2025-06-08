import math

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from services.tmdb import get_genres_map
from utils.preferences import toggle_genre, clear_genres, get_genres

router = Router()
PAGE = 10

@router.message(Command("setgenre"))
async def set_genre_cmd(msg: Message):
    await show_genres(msg, 0, send_new=True)

@router.message(Command("cleargenre"))
async def clear_genre_cmd(msg: Message):
    clear_genres(msg.from_user.id)
    await msg.answer("Фильтры по жанрам сброшены ✅")

@router.callback_query(lambda c: c.data.startswith("gpage:"))
async def genre_page(call: CallbackQuery):
    page = int(call.data.split(":")[1])
    await show_genres(call.message, page, edit=True)
    await call.answer()

@router.callback_query(lambda c: c.data.startswith("genre:"))
async def genre_toggle(call: CallbackQuery):
    genre_id = int(call.data.split(":")[1])
    toggle_genre(call.from_user.id, genre_id)
    await show_genres(call.message, 0, edit=True)
    await call.answer()

async def show_genres(msg, page, send_new=False, edit=False):
    genres = await get_genres_map()
    user_genres = get_genres(msg.chat.id)

    items = list(genres.items())
    total_pages = math.ceil(len(items) / PAGE)
    items = items[page * PAGE:(page + 1) * PAGE]

    keyboard = []
    for gid, name in items:
        checked = "✅ " if gid in user_genres else ""
        keyboard.append([InlineKeyboardButton(text=checked + name, callback_data=f"genre:{gid}")])

    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="⬅️", callback_data=f"gpage:{page - 1}"))
    if (page + 1) * PAGE < len(genres):
        nav.append(InlineKeyboardButton(text="➡️", callback_data=f"gpage:{page + 1}"))
    if nav:
        keyboard.append(nav)

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = "Выберите жанры, по которым хотите получать рекомендации:"

    if send_new:
        await msg.answer(text, reply_markup=markup)
    elif edit:
        await msg.edit_text(text, reply_markup=markup)

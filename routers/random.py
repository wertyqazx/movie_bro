from aiogram import Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from services.tmdb import get_movie_details, poster_url, random_popular_movie
from services.db import add_favorite

router = Router()

@router.message(Command("random"))
async def cmd_random(message: Message):
    try:
        movie = await random_popular_movie()
        details = await get_movie_details(movie["id"])
    except Exception as e:
        await message.answer(f"Что-то пошло не так 🤷‍♂️\n<code>{e}</code>")
        return

    text = (
        f"<b>{details.get('title')}</b> ({details.get('release_date', '')[:4]})\n"
        f"⭐ {details.get('vote_average', 0):.1f} / 10\n"
        f"<i>{details.get('overview') or 'Без описания.'}</i>"
    )

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⭐ Добавить в избранное", callback_data=f"fav:{movie['id']}")]
        ]
    )

    url = poster_url(details.get("poster_path"))
    if url:
        await message.answer_photo(url, caption=text, reply_markup=kb)
    else:
        await message.answer(text, reply_markup=kb)

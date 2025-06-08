from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from services.db import list_favorites, remove_favorite
from services.tmdb import poster_url

router = Router()

@router.message(Command("favorites"))
async def show_favorites(message: Message):
    items = await list_favorites(message.from_user.id)
    if not items:
        await message.answer("У вас пока нет избранных фильмов.")
        return

    for movie_id, title, poster in items:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🗑 Удалить", callback_data=f"del:{movie_id}")]
            ]
        )
        url = poster_url(poster) if poster else None
        if url:
            await message.answer_photo(url, caption=title, reply_markup=kb)
        else:
            await message.answer(title, reply_markup=kb)

@router.callback_query(lambda c: c.data and c.data.startswith("del:"))
async def delete_favorite(call: CallbackQuery):
    movie_id = int(call.data.split(":")[1])
    await remove_favorite(call.from_user.id, movie_id)
    await call.message.delete()

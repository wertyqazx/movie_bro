from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 <b>MovieMate</b>\n"
        "Я помогу найти интересный фильм или сериал.\n"
        "Напиши /help, чтобы узнать команды."
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "<b>Команды:</b>\n"
        "/start — приветствие\n"
        "/help — справка\n"
        "/find — поиск фильма\n"
        "/random — случайный фильм\n"
        "/top250 — ТОП-250 TMDb\n"
        "/favorites — мои избранные\n"
        "/setgenre — выбрать жанры\n"
        "/cleargenre — сброс жанров\n\n"

        "<b>🎯 Как использовать фильтрацию по жанрам:</b>\n"
        "Команда /setgenre позволяет выбрать жанры, которые вас интересуют. После этого\n"
        "результаты команд /find, /random и /top250 будут фильтроваться по ним.\n"
        "Чтобы убрать фильтрацию, используйте /cleargenre.\n\n"

        "<b>🔍 Поиск фильмов:</b>\n"
        "Команда /find ищет фильмы по названию на русском и английском языках. "
        "Даже если вы не помните точное название, бот постарается найти наиболее подходящие варианты."
    )

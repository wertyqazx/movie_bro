# states/search.py
from aiogram.fsm.state import State, StatesGroup


class SearchMovie(StatesGroup):
    waiting_for_title = State()

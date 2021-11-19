from aiogram.dispatcher.filters.state import State, StatesGroup


class HabitState(StatesGroup):
    name = State()

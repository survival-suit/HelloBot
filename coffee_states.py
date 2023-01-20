from aiogram.dispatcher.filters.state import State, StatesGroup


class CoffeeStates(StatesGroup):
    coffee_start = State()

from aiogram.dispatcher.filters.state import StatesGroup, State

class MessageStatesGroup(StatesGroup):
    text = State()
    photo = State()
    wait = State()

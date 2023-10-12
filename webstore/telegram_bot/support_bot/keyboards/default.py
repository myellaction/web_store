from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_kb():
    markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='📝 Задать вопрос'), KeyboardButton(text='📓 Мои вопросы')],
        [KeyboardButton(text='📌 Справочная информация')]
    ], resize_keyboard=True)
    return markup

def get_cancel_kb():
    markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='❌ Отменить')]
    ], resize_keyboard=True)
    return markup


from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

cb_questions = CallbackData('show_question','pk')

def get_options():
    markup = InlineKeyboardMarkup(inline_keyboard = [
        [InlineKeyboardButton(text='🗒 Редактировать текст', callback_data='edit_text')],
         [InlineKeyboardButton(text='🏞 Добавить изображение', callback_data='add_photo')],
        [InlineKeyboardButton(text='✅ Отправить', callback_data='send')]
    ])
    return markup

def get_questions_ikb(questions):
    markup = InlineKeyboardMarkup()
    for q in questions:
        status = '⌛' if q.status.title == 'В работе' else '📩'
        markup.add(InlineKeyboardButton(text=f'№{q.pk} {q.date_created.strftime("%d.%m.%Y")} {status}',
                                        callback_data=cb_questions.new(q.pk)))
    return markup

def get_back():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('⬅️Назад', callback_data='get_back')]
    ])



from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram import types
from telegram_bot.support_bot.loader import dp, bot
from telegram_bot.support_bot.utils.db_api import commands
from telegram_bot.support_bot.utils.state import MessageStatesGroup
from telegram_bot.support_bot.keyboards import default, inline

information = '''👨🏻‍🔧 Бот службы поддержки
Может приннимать обращения и отправлять ответы на них.
Чтоб задать вопрос, выберите "📝 Задать вопрос". После рассмотрения вопроса вы получите сообщение.
В меню "📓 Мои вопросы" ви можете ознакомиться с заданными вопросами.'''

@dp.message_handler(Command('start'), state = '*')
async def cmd_start(message: types.Message):
    await message.delete()

    if not await commands.get_user(message.from_user.id):
        await commands.register_user(telegram_user_id=message.from_user.id,
                                     name=message.from_user.full_name,
                                     username=message.from_user.username)
    await message.answer(text='Здравствуйте. Чем могу помочь?',
                         reply_markup = default.get_main_kb())

@dp.message_handler(text = '📌 Справочная информация')
async def cmd_help(message: types.Message):
    await message.delete()
    await message.answer(text=information)

@dp.message_handler(text='📝 Задать вопрос')
async def make_question(message: types.Message):
    await message.delete()
    await MessageStatesGroup.text.set()
    await message.answer('Опишите ваш вопрос', reply_markup=default.get_cancel_kb())

@dp.message_handler(text='❌ Отменить', state='*')
async def cmd_cancel(message: types.Message, state:FSMContext):
    await message.delete()
    await message.answer('Шаблон вопроса удалено.', reply_markup=default.get_main_kb())
    await state.finish()

@dp.message_handler(state=MessageStatesGroup.text)
async def save_text(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        data['text'] = message.text
        photo = data.get('photo')
    text = f'<b>Ваш вопрос сформирован:</b>\n{message.text}'
    if not photo:
        await message.answer(text=text, reply_markup=inline.get_options())
    else:
        await message.answer_photo(photo = photo, caption = text, reply_markup=inline.get_options())
    await state.reset_state(with_data=False)

@dp.callback_query_handler(text='add_photo')
async def take_photo(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await MessageStatesGroup.photo.set()
    await callback.message.answer(text='Пришлите изображение')

@dp.message_handler(content_types=types.ContentType.PHOTO, state = MessageStatesGroup.photo)
async def save_photo(message: types.Message, state: FSMContext):
    await message.delete()
    photo = message.photo[-1].file_id
    async with state.proxy() as data:
        data['photo'] = photo
        text = data['text']
    await message.answer_photo(photo=photo, caption =f'<b>Ваш вопрос сформирован:</b>\n{text}',
                         reply_markup=inline.get_options())
    await state.reset_state(with_data=False)

@dp.callback_query_handler(text='edit_text')
async def edit_text(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text='Ожидаю отредактированный текст')
    await MessageStatesGroup.text.set()

@dp.callback_query_handler(text='send')
async def cmd_send_question(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    async with state.proxy() as data:
        photo = data.get('photo')
        text=data.get('text')
    url=None
    if photo:
        photo_file= await bot.get_file(file_id = photo)
        url = await photo_file.get_url()
    res = await commands.send_question(teleuser=callback.from_user.id, content=text, picture=url, picture_file_id=photo)
    if res:
        await callback.message.answer('📤 Ваш вопрос успешно отправлен. Благодарим!',
                                      reply_markup=default.get_main_kb())
    await state.finish()

@dp.message_handler(text='📓 Мои вопросы')
async def cmd_show_questions(message: types.Message):
    await message.delete()
    questions = await commands.get_questions(message.from_user.id)
    if not questions:
        await message.answer('Зарегистрированных вопросов нет.')
    else:
        markup=inline.get_questions_ikb(questions)
        await message.answer('Отправленные вопросы', reply_markup=markup)

@dp.callback_query_handler(inline.cb_questions.filter())
async def cmd_show_question(callback: types.CallbackQuery, callback_data:dict):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text=f'Вопрос №{callback_data.get("pk")}')
    q = await commands.get_question(callback_data.get('pk'))
    text= f'<b>Статус:</b> {q.status}\n' \
          f'<b>Дата формирования:</b> {q.date_created.strftime("%d.%m.%Y")}' \
          f'\n<b>Текст вопроса:</b>\n{q.content}'
    if q.answer_content:
        if q.picture:
            await callback.message.answer_photo(photo=q.picture_file_id, caption=text)

        else:
            await callback.message.answer(text=text)
    else:
        markup = inline.get_back()
        if q.picture:
            await callback.message.answer_photo(photo=q.picture_file_id, caption=text, reply_markup=markup)
        else:
            await callback.message.answer(text=text, reply_markup=markup)

    if q.answer_content:
        answer = f'<b>Ответ:</b>\n{q.answer_content}'
        markup = inline.get_back()
        if q.answer_picture:
            with open(q.answer_picture.path, 'rb') as photo:
                await callback.message.answer_photo(photo=photo, caption=answer,
                                                reply_markup=markup)
        else:
            await callback.message.answer(text=answer, reply_markup=markup)

@dp.callback_query_handler(text='get_back')
async def cmd_get_back(callback: types.CallbackQuery):
    await callback.answer()
    questions = await commands.get_questions(callback.from_user.id)
    if not questions:
        await callback.message.answer('Зарегистрированных вопросов нет.')
    else:
        markup = inline.get_questions_ikb(questions)
        await callback.message.answer('Отправленные вопросы', reply_markup=markup)











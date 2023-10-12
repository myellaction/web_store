from telegram_bot.support_bot.loader import bot
import asyncio
from django.core.mail import EmailMessage

def send_answer_user(obj):
    chat_id = obj.teleuser.telegram_user_id
    if obj.answer_picture:
        photo = open(obj.answer_picture.path, 'rb')
        func = bot.send_photo(chat_id=chat_id, photo=photo, caption=obj.answer_content)
    else:
        func = bot.send_message(chat_id=chat_id, text=obj.answer_content)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(func)

def send_message_admin(obj):
    body = f'''Пользователь {obj.teleuser.username} оставил вопрос.
Для ознакомления с ним можете перейти по ссылке
http://141.144.242.171/admin/telegram_bot/question/{obj.pk}/change/
'''
    em = EmailMessage(subject='Пришел новый вопрос', body=body, to=['alexsergx94@gmail.com'])
    em.send()

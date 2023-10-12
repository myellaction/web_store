from telegram_bot.models import TeleUser, Question
from asgiref.sync import sync_to_async
from datetime import datetime


@sync_to_async
def register_user(telegram_user_id, name, username):
    return TeleUser.objects.get_or_create(telegram_user_id=telegram_user_id,
                                name=name,
                                username=username)


@sync_to_async
def get_user(telegram_user_id):
    try:
        return TeleUser.objects.get(telegram_user_id=telegram_user_id)
    except:
        return False

@sync_to_async
def send_question(teleuser, content, picture=None, picture_file_id=None):
    user = TeleUser.objects.get(telegram_user_id=teleuser)
    q = Question(content=content, teleuser=user)
    if picture:
        q.picture = picture
        q.picture_file_id = picture_file_id
    q.save()
    return True

@sync_to_async
def get_questions(teleuser):
    user = TeleUser.objects.get(telegram_user_id=teleuser)
    res = Question.objects.filter(teleuser=user.pk)
    return res

@sync_to_async
def get_question(pk):
    q = Question.objects.get(pk=pk)
    return q



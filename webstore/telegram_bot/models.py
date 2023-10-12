from django.db import models
from .utilities import *

# Create your models here.

class TeleUser(models.Model):
    telegram_user_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=200, verbose_name="Имя")
    username = models.CharField(max_length=200, verbose_name='Юзернейм')
    date_register = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'


class QuestionStatus(models.Model):
    title = models.CharField(max_length=100, verbose_name='Статус')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статус вопроса'
        verbose_name_plural = 'Статусы вопросов'


class Question(models.Model):
    content = models.TextField(max_length=3000, verbose_name='Текст вопроса')
    picture = models.URLField(null=True, blank=True, verbose_name='Изображение')
    picture_file_id = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.ForeignKey(QuestionStatus, default=1, on_delete=models.PROTECT, verbose_name='Статус')
    teleuser = models.ForeignKey(TeleUser, on_delete=models.PROTECT, verbose_name='Пользователь')
    answer_content = models.TextField(verbose_name='Ответ')
    answer_picture = models.ImageField(upload_to = 'photos/answers/%Y/%m/%d', blank=True, null=True, verbose_name='Изображение к ответу')

    def save(self, *args, **kwargs):
        if self.answer_content:
            self.status = QuestionStatus.objects.get(pk=2)
        instance = super().save(*args, **kwargs)
        if self.answer_content:
            send_answer_user(self)
        else:
            send_message_admin(self)
        return instance



    def __str__(self):
        return f'Вопрос №{self.pk}'

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопрос'

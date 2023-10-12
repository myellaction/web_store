from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(QuestionStatus)
admin.site.register(Question)
admin.site.register(TeleUser)



from aiogram import executor
import django
import os

async def on_startup(_):
    print('Бот запущено!')

def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webstore.settings')
    os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE':'true'})
    django.setup()



if __name__ == '__main__':
    setup_django()
    from handlers import dp
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)








import os

from dotenv import load_dotenv

from bot.tg.client import TgClient

is_dotenv_load = load_dotenv()
if not is_dotenv_load:
    raise FileNotFoundError('Не удалось загрузить переменные окружения!')
else:
    print('Переменные окружения ЗАГРУЖЕНЫ')

SECRET = os.getenv('SECRET')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
REDIS_HOST = os.getenv('REDIS_HOST')
TELEGRAM_API = os.getenv('TELEGRAM_API')

if not (SECRET and DB_NAME and DB_USER and
        DB_PASSWORD and DB_HOST and DB_PORT and
        TELEGRAM_API and REDIS_HOST):
    raise FileNotFoundError('Не удалось загрузить какую-то переменную')

tg_client = TgClient(TELEGRAM_API)

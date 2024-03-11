# Название
Описание проекта

## Для запуска
Настроить файл с переменными среды .env, пример:
```editorconfig
SECRET=django-insecure-i-u2...
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5432
TELEGRAM_API=5280...
```

Создать контейнеры с базами данных:
```commandline
docker-compose up
```

После инициализации базы данных установить фикстуры с днями недели командой 
```commandline
./manage.py loaddata weekdays.json
```
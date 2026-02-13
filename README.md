# notebook-bot
Простой Telegram-бот для заметок, погоды, курсов криптовалют и хранения сообщений.

## Функции бота
- `/start` — приветствие
- `/weather` — погода в нескольких городах
- `/eth` — курс Ethereum
- `/myage` — заполнение анкеты (FSM)
- `/last` — последние 5 сообщений

## Технологии
- **aiogram 3.x** — асинхронный фреймворк для Telegram
- **FastAPI** — веб-сервер для приёма вебхуков
- **SQLite** — локальная БД
- **Poetry** — менеджер зависимостей
- **Docker + docker-compose** — контейнеризация
- **Tuna** — проброс локального сервера в интернет

## Переменные окружения
Создайте файл `.env` на основе `.env.example`:


Запуск сборки докера:
docker-compose up --build



## Настройка

1. Создайте `.env`:
  bash cp .env.example .env

2. Установите зависимости (опционально, если не используете Docker):
  bash poetry install

3. Создайте папку для данных:

## Запуск через Docker
   bash docker-compose up --build


После запуска:
- Бот начнёт работу.
- Tuna создаст публичный URL.
- Все данные БД будут сохраняться в `./data/db/tg_data.db`.



## Примечания
- Для работы с Tuna не обязателен токен — используется `--all`.
- Если вы видите ошибку подключения к Docker, убедитесь, что **Docker Desktop запущен**.
- Порт бота: `8080` (внутри контейнера).
- Для продакшена рассмотрите использование `Redis`, `PostgreSQL`, `HTTPS` и `nginx`.



## Дистрибьюция 

Чтобы перенести образы контейнеров, используемые в вашем docker-compose.yml, на другую машину, есть несколько способов. Ниже описаны основные подходы — с сохранением и загрузкой образов через файлы (без использования реестра) и с использованием Docker Registry.

✅ Способ 1: Экспорт и импорт образов в виде архивов (без реестра)
Подходит, если нет доступа к интернету или вы хотите полностью автономный перенос.

Шаг 1: На исходной машине — сохраните нужные образы
Найдите имена образов:
> docker images

В нашем случае используются:
ollama/ollama:latest
yuccastream/tuna

Ваш собственный образ telegram-bot (собирается через build: .)

Сохраните их в .tar-файлы:
> docker save -o ollama.tar ollama/ollama:latest
> docker save -o tuna.tar yuccastream/tuna
> docker save -o bot.tar telegram-bot  # или имя, которое указал build

Если имя образа бота не telegram-bot, проверьте:
> docker images | grep bot

Шаг 2: Перенесите файлы на другую машину
Например, через scp, флешку, облако и т.д.: 
> scp *.tar user@new-machine:/path/to/destination/

Шаг 3: На новой машине — загрузите образы
> docker load -i ollama.tar
> docker load -i tuna.tar
> docker load -i bot.tar

Шаг 4: Запустите docker-compose 
Убедитесь, что на новой машине установлены:

Docker
Docker Compose
.env файл
docker-compose.yml

Затем:
> docker-compose up -d

Образы уже будут доступны локально, поэтому Docker не будет пытаться их скачивать.

✅ Способ 2: Использование приватного/публичного Docker Registry
Более масштабируемый способ, особенно для командной разработки.
Шаг 1: Залогиньтесь в registry (например, Docker Hub)
> docker login

Шаг 2: Пометьте и запушьте образы
Для вашего бота:
> docker tag telegram-bot yourusername/telegram-bot:latest
> docker push yourusername/telegram-bot:latest

(Остальные образы ollama/ollama и yuccastream/tuna уже публичные — их можно не пушить.)
Шаг 3: На новой машине — просто запустите docker-compose up
Docker сам скачает образы из Docker Hub.
Если вы хотите использовать свой образ бота — укажите полное имя в docker-compose.yml:

services:
  bot:
    image: yourusername/telegram-bot:latest
    # build: .   # закомментируйте или удалите, если используете готовый образ
    ...

✅ Совет: Сохраните также данные (volumes)
Если важно перенести данные (например, базу SQLite и модели Ollama):
Для sqlite_data:
Скопируйте содержимое ${SQLITE_DATA_DIR} на новую машину в ту же папку.
Для ollama_models:
Это named volume. Чтобы его перенести:
# На исходной машине:
> docker run --rm -v ollama_models:/source -v $(pwd):/backup alpine tar czf /backup/ollama_models.tar.gz -C /source .

# Перенести файл ollama_models.tar.gz
# На новой машине:
> docker volume create ollama_models
> docker run --rm -v ollama_models:/dest -v $(pwd):/backup alpine tar xzf /backup/ollama_models.tar.gz -C /dest











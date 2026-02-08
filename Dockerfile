# Используем официальный образ Python с установленным Poetry
FROM python:3.10-slim

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR .

# Копируем только pyproject.toml и poetry.lock (если есть)
COPY pyproject.toml poetry.lock ./

# Копируем pyproject.toml и README.md
COPY pyproject.toml ./

# Устанавливаем зависимости через Poetry
RUN pip install --upgrade pip \
    && poetry config virtualenvs.create true \
    && poetry config virtualenvs.in-project true \
    && poetry install --only main --no-interaction --no-ansi --no-root

# Копируем остальной код проекта
COPY . .

# Экспортируем переменные окружения (необязательно, можно передавать через docker-compose)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Порты: 8080 для FastAPI
EXPOSE 8080

# Запуск бота
CMD ["poetry", "run", "python", "-m", "src.app.main"]
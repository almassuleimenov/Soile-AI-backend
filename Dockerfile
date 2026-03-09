# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /code

# Копируем файл с зависимостями Poetry
COPY pyproject.toml poetry.lock* /code/

# Устанавливаем poetry и зависимости
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-dev

# Копируем весь наш код в контейнер
COPY ./app /code/app

# Команда для запуска нашего FastAPI сервера
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
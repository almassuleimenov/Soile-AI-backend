FROM python:3.13-slim

WORKDIR /code

COPY pyproject.toml poetry.lock* /code/

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
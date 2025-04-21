FROM python:3.11.2
WORKDIR /app

# Подготовка Poetry
RUN pip install poetry


# Отключаем Poetry-venv, чтобы зависимости шли сразу в /usr/local
RUN poetry config virtualenvs.create false \
 && poetry config virtualenvs.in-project false

# Копируем манифесты зависимостей и устанавливаем их
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root --no-interaction
RUN poetry add gunicorn

# Копируем весь код приложения
COPY . .


EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

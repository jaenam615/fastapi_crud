FROM python:3.12

WORKDIR /app

COPY ./app /app/app

COPY ./pyproject.toml /app/pyproject.toml
COPY ./uv.lock /app/uv.lock

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir uv \
    && uv sync

EXPOSE 8000

CMD ["uv", "run", "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--workers", "2", "--bind", "0.0.0.0:8000"]

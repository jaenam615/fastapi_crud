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

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

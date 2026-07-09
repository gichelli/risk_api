FROM python:3.11-slim-bookworm

WORKDIR /app

COPY pyproject.toml .

COPY src/ ./src/

RUN pip install --upgrade pip && \
    pip install .

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "src.app:app"]
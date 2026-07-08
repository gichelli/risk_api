FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .

RUN pip install --upgrade pip \
    && pip install .

COPY src/ ./src/

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "src.app:app"]
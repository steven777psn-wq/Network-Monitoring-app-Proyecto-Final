FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/app/ ./app/

CMD ["gunicorn", "--workers", "1", "--bind", "0.0.0.0:8080", "app.main:app"]

FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV TELEGRAM_CHAT_ID=1429514055

CMD ["python", "app.py"]
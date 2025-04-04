FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY generate_fake_logs.py .

# Запускаем скрипт автоматически
CMD ["python", "generate_fake_logs.py"]
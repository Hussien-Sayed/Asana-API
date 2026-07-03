FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY config.py .
COPY asana_client.py .
COPY models.py .
COPY routes/ ./routes/
COPY services/ ./services/

ENV APP_HOST=0.0.0.0

EXPOSE 8000

CMD ["python", "main.py"]

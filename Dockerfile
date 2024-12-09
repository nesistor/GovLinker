FROM python:3.11-slim

WORKDIR /app

COPY . /app/

# Instalacja zależności
RUN pip install --no-cache-dir -r api/requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PORT=8000

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python seed_jmr_600.py

EXPOSE 8000

CMD ["sh", "-c", "uvicorn crm_portal_single_file:app --host 0.0.0.0 --port ${PORT:-8000}"]

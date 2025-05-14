FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY tsdb ./tsdb
COPY prometheus.yml .
COPY docker-compose.yml .
COPY README.md .
COPY grafana ./grafana

EXPOSE 8000 9090 3000
CMD ["uvicorn", "tsdb.api:app", "--host", "0.0.0.0", "--port", "8000"]

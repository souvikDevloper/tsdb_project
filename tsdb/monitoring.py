from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response
import psutil

REQUEST_COUNT = Counter(
    'tsdb_requests_total', 'Total HTTP requests',
    ['method','endpoint','status']
)
REQUEST_LATENCY = Histogram(
    'tsdb_request_latency_seconds','Request latency',
    ['method','endpoint']
)
INGESTION_COUNT = Counter(
    'tsdb_ingestion_total','Data points ingested'
)
MEMORY_USAGE = Gauge(
    'tsdb_memory_bytes','RSS memory bytes'
)

def record_metrics(method, endpoint, status, duration):
    REQUEST_COUNT.labels(method, endpoint, status).inc()
    REQUEST_LATENCY.labels(method, endpoint).observe(duration)
    MEMORY_USAGE.set(psutil.Process().memory_info().rss)

def metrics_endpoint():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

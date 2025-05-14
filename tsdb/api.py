import os
import time
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from .shard import ShardedTSDB
from .monitoring import record_metrics, metrics_endpoint, INGESTION_COUNT

app = FastAPI()

# Load from env or defaults
config = {
    'num_shards':       int(os.getenv('NUM_SHARDS',       4)),
    'chunk_size':       int(os.getenv('CHUNK_SIZE',       500)),
    'retention_seconds':int(os.getenv('RETENTION_SECONDS', 60)),
    'persistence':      True
}
db = ShardedTSDB(**config)

class WriteRequest(BaseModel):
    key: str
    timestamp: int
    value: float

class QueryResponse(BaseModel):
    result: list

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    record_metrics(request.method, request.url.path, response.status_code, time.time()-start)
    return response

@app.post("/write", status_code=204)
def write(req: WriteRequest):
    db.write(req.key, req.timestamp, req.value)
    INGESTION_COUNT.inc()

@app.get("/query/{key}", response_model=QueryResponse)
def query(key: str, start: int, end: int, agg: str=None, downsample: int=0):
    if start > end:
        raise HTTPException(400, "start must be <= end")
    result = db.query(key, start, end, agg, downsample or None)
    return QueryResponse(result=result)

@app.get("/metrics")
def metrics():
    return metrics_endpoint()

@app.get("/now")
def now():
    return {"now": int(time.time())}

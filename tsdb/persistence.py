import os
import json
from .chunk import Chunk
from typing import Any

class PersistenceHandler:
    def __init__(self, base_dir: str = "tsdb_data"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def flush(self, series: Any, chunk: Chunk):
        key = getattr(series, 'name', 'series')
        fname = f"{key}_{chunk.start_ts}.json"
        path = os.path.join(self.base_dir, fname)
        with open(path, 'w') as f:
            json.dump(chunk.data, f)

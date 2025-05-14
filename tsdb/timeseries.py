import threading
import time
from collections import deque, defaultdict
from typing import List, Tuple, Optional
from .chunk import Chunk
from .persistence import PersistenceHandler

class TimeSeries:
    def __init__(
        self,
        chunk_size: int,
        retention_seconds: Optional[int] = None,
        persistence: Optional[PersistenceHandler] = None
    ):
        self.chunk_size = chunk_size
        self.chunks: deque[Chunk] = deque()
        self.lock = threading.Lock()
        self.retention = retention_seconds
        self.persistence = persistence
        if retention_seconds:
            t = threading.Thread(target=self._evict_loop, daemon=True)
            t.start()

    def write(self, timestamp: int, value: float):
        with self.lock:
            if not self.chunks or self.chunks[-1].is_full():
                self.chunks.append(Chunk(self.chunk_size))
            self.chunks[-1].append(timestamp, value)

    def query(
        self,
        start: int,
        end: int,
        agg: Optional[str] = None,
        downsample_interval: Optional[int] = None
    ):
        points: List[Tuple[int, float]] = []
        with self.lock:
            for chunk in self.chunks:
                if chunk.end_ts < start or chunk.start_ts > end:
                    continue
                points.extend(chunk.slice_range(start, end))
        if downsample_interval:
            return self._downsample(points, downsample_interval, agg)
        if agg and points:
            return self._aggregate([v for _, v in points], agg)
        return points

    def _aggregate(self, values: List[float], agg: str):
        if agg == 'min':   return min(values)
        if agg == 'max':   return max(values)
        if agg == 'sum':   return sum(values)
        if agg == 'count': return len(values)
        if agg == 'avg':   return sum(values)/len(values)
        raise ValueError(f"Unknown agg: {agg}")

    def _downsample(self, points: List[Tuple[int, float]], interval: int, agg: str):
        buckets = defaultdict(list)
        base = points[0][0] if points else 0
        for ts, val in points:
            bucket = ((ts - base)//interval)*interval + base
            buckets[bucket].append(val)
        result = []
        for b in sorted(buckets):
            vals = buckets[b]
            if agg:
                result.append((b, self._aggregate(vals, agg)))
            else:
                result.append((b, vals))
        return result

    def _evict_loop(self):
        while True:
            cutoff = int(time.time()) - self.retention
            with self.lock:
                while self.chunks and self.chunks[0].end_ts < cutoff:
                    old = self.chunks.popleft()
                    if self.persistence:
                        self.persistence.flush(self, old)
            time.sleep(max(1, self.retention//2))

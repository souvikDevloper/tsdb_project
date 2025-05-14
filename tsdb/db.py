from collections import defaultdict
from typing import Optional
from .timeseries import TimeSeries
from .persistence import PersistenceHandler

class InMemoryTSDB:
    def __init__(
        self,
        chunk_size: int = 1000,
        retention_seconds: Optional[int] = None,
        persistence: bool = False
    ):
        self.chunk_size = chunk_size
        self.retention = retention_seconds
        self.persistence_handler = PersistenceHandler() if persistence else None
        self.series = defaultdict(self._make_series)

    def _make_series(self):
        ts = TimeSeries(
            chunk_size=self.chunk_size,
            retention_seconds=self.retention,
            persistence=self.persistence_handler
        )
        ts.name = None
        return ts

    def write(self, key: str, timestamp: int, value: float):
        ts = self.series[key]
        ts.name = key
        ts.write(timestamp, value)

    def query(
        self, key: str, start: int, end: int,
        agg: str=None, downsample: int=None
    ):
        ts = self.series.get(key)
        if not ts:
            return []
        return ts.query(start, end, agg, downsample)

import threading
from typing import List, Tuple

class Chunk:
    __slots__ = ('capacity', 'data', 'start_ts', 'end_ts', '_lock')

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.data: List[Tuple[int, float]] = []
        self.start_ts = None
        self.end_ts = None
        self._lock = threading.Lock()

    def append(self, timestamp: int, value: float):
        with self._lock:
            if self.start_ts is None:
                self.start_ts = timestamp
            self.end_ts = timestamp
            self.data.append((timestamp, value))

    def is_full(self) -> bool:
        return len(self.data) >= self.capacity

    def slice_range(self, start: int, end: int) -> List[Tuple[int, float]]:
        return [(ts, v) for ts, v in self.data if start <= ts <= end]

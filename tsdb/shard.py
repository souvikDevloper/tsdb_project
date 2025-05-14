from .db import InMemoryTSDB
from typing import Dict

class ShardedTSDB:
    def __init__(self, num_shards: int = 4, **kwargs):
        self.num_shards = num_shards
        self.shards: Dict[int, InMemoryTSDB] = {
            i: InMemoryTSDB(**kwargs) for i in range(num_shards)
        }

    def _get_shard(self, key: str):
        return self.shards[hash(key) % self.num_shards]

    def write(self, key: str, timestamp: int, value: float):
        shard = self._get_shard(key)
        shard.write(key, timestamp, value)

    def query(self, key: str, start: int, end: int, agg: str=None, downsample: int=None):
        shard = self._get_shard(key)
        return shard.query(key, start, end, agg, downsample)

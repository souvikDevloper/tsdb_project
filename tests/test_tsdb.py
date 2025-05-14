import time
import pytest
from tsdb.db import InMemoryTSDB

def test_write_and_query_raw():
    db = InMemoryTSDB(chunk_size=3)
    base = int(time.time())
    for i in range(5):
        db.write('m1', base+i, float(i))
    pts = db.query('m1', base, base+4)
    assert len(pts) == 5

def test_aggregations():
    db = InMemoryTSDB(chunk_size=3)
    base = int(time.time())
    for i in range(4):
        db.write('m2', base+i, float(i+1))
    assert db.query('m2', base, base+3, agg='sum') == pytest.approx(10)
    assert db.query('m2', base, base+3, agg='avg') == pytest.approx(2.5)

def test_downsampling():
    db = InMemoryTSDB(chunk_size=5)
    base = 1000
    for i in range(10):
        db.write('m3', base+i, float(i))
    ds = db.query('m3', base, base+9, agg='sum', downsample=5)
    assert ds == [(1000, sum(range(5))), (1005, sum(range(5,10)))]

def test_addition():
    assert 2 + 3 == 5

def test_subtraction():
    assert 5 - 3 == 2
"""
Basic reproducibility and clean-room tests.
"""
import random
import os
from src.config import SEED


def test_seed_determinism():
    random.seed(SEED)
    a = [random.random() for _ in range(10)]
    random.seed(SEED)
    b = [random.random() for _ in range(10)]
    assert a == b


def test_dockerfile_present():
    assert os.path.exists('docker/Dockerfile')

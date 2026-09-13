"""
ACO path router with resource & cost budgeting hooks.

This module implements a simple Ant Colony Optimization inspired router and per-path resource caps to prevent runaway scaling costs.
"""
import random
import threading
from typing import List

class ACOPathRouter:
    def __init__(self, num_paths: int = 8, base_pheromone: float = 1.0):
        self.num_paths = num_paths
        self.pheromones = [base_pheromone for _ in range(num_paths)]
        # resource caps per path (e.g., max_workers, max_gpu_seconds)
        self.resource_caps = [{'max_workers': 16, 'max_gpu_seconds': 0} for _ in range(num_paths)]
        self.lock = threading.Lock()

    def pick_path(self):
        with self.lock:
            total = sum(self.pheromones)
            r = random.random() * total
            cum = 0.0
            for i, p in enumerate(self.pheromones):
                cum += p
                if r <= cum:
                    return i
            return len(self.pheromones) - 1

    def reinforce(self, idx: int, reward: float = 1.0):
        with self.lock:
            self.pheromones[idx] += reward
            # slight evaporation
            self.pheromones = [p * 0.995 for p in self.pheromones]

    def set_resource_cap(self, idx: int, max_workers: int = None, max_gpu_seconds: int = None):
        with self.lock:
            cap = self.resource_caps[idx]
            if max_workers is not None:
                cap['max_workers'] = max_workers
            if max_gpu_seconds is not None:
                cap['max_gpu_seconds'] = max_gpu_seconds
            self.resource_caps[idx] = cap

    def get_resource_cap(self, idx: int):
        return self.resource_caps[idx]

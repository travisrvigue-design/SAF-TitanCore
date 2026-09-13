"""
Runtime orchestration for Lotusv1 agent mesh.
Provides a simple orchestrator that schedules tasks to worker threads/processes while enforcing reproducibility and human-in-the-loop gates.
"""
import threading
import queue
import time
import json
from src.config import SEED
from src.aco_router import ACOPathRouter
from src.gpg_audit import GPGAuditLog

import random
random.seed(SEED)

class Task:
    def __init__(self, id, metadata):
        self.id = id
        self.metadata = metadata

class Orchestrator:
    def __init__(self, worker_count=16):
        self.task_queue = queue.Queue()
        self.workers = []
        self.worker_count = worker_count
        self.audit = GPGAuditLog()
        self.router = ACOPathRouter()
        self.shutdown_flag = threading.Event()

    def submit(self, task: Task):
        self.audit.log_event('message', {'task_id': task.id, 'metadata': task.metadata})
        self.task_queue.put(task)

    def start(self):
        for i in range(self.worker_count):
            t = threading.Thread(target=self._worker_loop, name=f'worker-{i}', daemon=True)
            self.workers.append(t)
            t.start()

    def _worker_loop(self):
        while not self.shutdown_flag.is_set():
            try:
                task = self.task_queue.get(timeout=1)
            except Exception:
                continue
            # route path
            path = self.router.pick_path()
            # simulate processing
            time.sleep(0.01)
            # checkpoint for human gate
            if task.metadata.get('requires_human', False):
                # emit hold event and wait for release
                self.audit.log_event('hold', {'task_id': task.id})
                # blocking wait simulated (real system verifies signed token)
                while not task.metadata.get('released', False):
                    time.sleep(0.5)
            self.audit.log_event('transition', {'task_id': task.id, 'path': path})
            self.task_queue.task_done()

    def stop(self):
        self.shutdown_flag.set()
        for w in self.workers:
            w.join(timeout=1)

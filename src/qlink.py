"""
Q-LINK plateau mitigator: dynamic parameter adjustment to avoid barren plateaus.
This module implements conservative numeric safeguards and parameter perturbation strategies.
"""
import math
import random
from typing import Dict, Any

class QLINKMitigator:
    def __init__(self):
        # safe numeric thresholds
        self.max_update = 1e-2
        self.min_lr = 1e-8
        self.max_lr = 1e-1

    def adjust(self, params: Dict[str, Any]) -> Dict[str, Any]:
        # params expected to have 'lr' and 'grad_norm'
        lr = params.get('lr', 1e-3)
        grad_norm = params.get('grad_norm', 0.0)
        # if grad norms vanish (plateau), slightly increase lr within bounds and add noise
        if abs(grad_norm) < 1e-6:
            lr = min(self.max_lr, lr * 1.5 + random.uniform(-1e-6, 1e-6))
        # cap updates
        lr = max(self.min_lr, min(self.max_lr, lr))
        params['lr'] = lr
        params['adjustment'] = 'qlink_noise' if abs(grad_norm) < 1e-6 else 'none'
        return params

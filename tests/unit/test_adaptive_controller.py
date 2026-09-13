"""
Tests for adaptive controller logic.
"""
from src.adaptive_controller import AdaptiveController


def test_allocate_scaling():
    ac = AdaptiveController(base_workers=16)
    out = ac.allocate_for_task({'expected_load': 2.0})
    assert 'workers' in out and out['workers'] >= 1
    assert 'path' in out


def test_observe_plateau():
    ac = AdaptiveController(base_workers=16)
    res = ac.observe_and_learn({'plateau': True, 'params': {'lr': 0.1}})
    assert res['mitigated'] is True

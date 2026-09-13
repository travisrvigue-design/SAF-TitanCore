"""
Tests for KEGG adapter using mocking to avoid real network calls.
"""
import pytest
from unittest.mock import patch
from src.kegg_adapter import KEGGAdapter


@patch('src.kegg_adapter.requests.get')
def test_get_pathway_by_ko_mocked(mock_get, tmp_path):
    # Arrange: mock response
    class DummyResp:
        status_code = 200
        text = 'path:ko0001\n'
    mock_get.return_value = DummyResp()

    # Ensure fresh cache DB in tmp
    import os
    orig = ' .cache'
    # Use adapter normally; cache DB location is hardcoded to .cache for now
    adapter = KEGGAdapter(rate_limit_per_minute=100)
    res = adapter.get_pathway_by_ko('K00001')
    assert 'text' in res
    assert 'path' in res['text'] or 'path' in res['text']


@patch('src.kegg_adapter.requests.get')
def test_get_gene_info_mocked(mock_get):
    class DummyResp:
        status_code = 200
        text = 'GENE INFO TEXT'
    mock_get.return_value = DummyResp()
    adapter = KEGGAdapter(rate_limit_per_minute=100)
    res = adapter.get_gene_info('hsa:1234')
    assert res['text'] == 'GENE INFO TEXT'

"""
Tests for KEGG adapter using mocking to avoid real network calls.
"""
from unittest.mock import patch, MagicMock
from src.kegg_adapter import KEGGAdapter


@patch("src.kegg_adapter.requests.get")
def test_get_pathway_by_ko_mocked(mock_get, tmp_path):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.text = "path:ko00010\n"
    mock_resp.raise_for_status = MagicMock()
    mock_get.return_value = mock_resp

    # Force cache into tmp so we don't pollute the repo
    import os
    os.environ["KEGG_CACHE_DB"] = str(tmp_path / "kegg_cache.db")

    adapter = KEGGAdapter(rate_limit_per_minute=100)
    res = adapter.get_pathway_by_ko("K00001")

    assert "text" in res
    assert "path" in res["text"]


@patch("src.kegg_adapter.requests.get")
def test_get_gene_info_mocked(mock_get, tmp_path):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.text = "GENE INFO TEXT"
    mock_resp.raise_for_status = MagicMock()
    mock_get.return_value = mock_resp

    import os
    os.environ["KEGG_CACHE_DB"] = str(tmp_path / "kegg_cache.db")

    adapter = KEGGAdapter(rate_limit_per_minute=100)
    res = adapter.get_gene_info("hsa:1234")

    assert res["text"] == "GENE INFO TEXT"

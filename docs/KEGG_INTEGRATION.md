# KEGG integration docs

This document describes the KEGG integration approach used by SAF-TitanCore.

Design principles
- Use on-demand KEGG REST API queries with a local sqlite cache to avoid repeated network calls and to obey rate limits.
- Avoid bulk redistribution of KEGG data; the repository includes only adapters and mocked tests. For bulk ingestion, the owner must have a KEGG license and follow KEGG terms.
- Cache keys are crafted as 'ko:<id>' and 'gene:<id>' and stored in .cache/kegg_cache.db. Cache TTL and eviction policies should be implemented as needed.

Usage
- scripts/ingest_kegg_placeholder.py demonstrates usage of src/kegg_adapter.KEGGAdapter
- In production, run a dedicated cache service or graph DB to serve pathway lookups to agents to avoid per-request latency.

Legal note
- KEGG dataset licensing restricts bulk redistribution; do not commit bulk KEGG data into this public repository without explicit permission.

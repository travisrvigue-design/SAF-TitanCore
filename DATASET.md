# DATASET & Manifests

Deterministic ingestion requirements
- All raw files (FASTQ/BAM) MUST be assigned deterministic unit ids
- Each unit file must have a recorded SHA-256 digest in manifest.json
- Partitioner must be deterministic (same input => same partitions + hashes)

Manifest example (manifest.json)
{
  "dataset_id": "example-dataset-0001",
  "created_at": "2026-09-13T00:00:00Z",
  "units": [
    {"unit_id": "unit-0001", "path": "data/unit-0001.fastq.gz", "sha256": "..."}
  ]
}

See scripts/partitioner.py for a deterministic partitioner implementation and tests/ for verification tests.

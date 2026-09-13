# Lotusv1 Architecture

Lotusv1 is the primary Edgeless Hybrid Agent Mesh implementation targeting high-throughput genomic preprocessing and anomaly detection.

Key components:
- Ingestion proxies and deterministic partitioner (scripts/partitioner.py)
- Lotusv1 Q-LINK and ACO modules (design docs + placeholders)
- Worker node templates optimized for 24-CPU / 128GB environments
- Verification pipeline (statistics + cryptographic signing)

Design notes:
- All artifacts are hashed with SHA-256 and recorded in manifest.json files
- Sign artifacts with Sigstore (cosign) in CI and store verification metadata
- Human-in-loop gating via SOP-001 (see SOP-001.md)

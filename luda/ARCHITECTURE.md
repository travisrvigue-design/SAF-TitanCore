# Luda Architecture

Luda variant is a high-throughput batch-first implementation optimized for large-scale retrospective analyses.

Differences vs Lotusv1:
- Larger partition units and aggressive parallelism
- Batch-oriented checkpointing and checkpoint aggregation
- Bulk verification jobs for statistical regression across long time windows

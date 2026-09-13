# Ludus Architecture

Ludus variant prioritizes low-latency, near-real-time inference on edge streaming data. It shares core infrastructure with Lotusv1 but has lower-batch, lower-latency scheduling and different agent tuning.

Differences vs Lotusv1:
- Scheduling tuned for sub-second decision windows
- Smaller partition sizes and prioritized worker queues
- Enhanced heartbeat SLOs and local cache layer to minimize I/O latency

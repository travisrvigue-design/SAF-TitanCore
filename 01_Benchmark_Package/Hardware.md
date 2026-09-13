Hardware: Describe hardware baselines used for benchmarks and tests.

- Local test bench (single-node reference):
  - CPU: 2x 12-core Intel Xeon (24 cores total) or AMD EPYC equivalent
  - Memory: 128 GB
  - Disk: NVMe SSD 1TB
  - Network: 1 Gbps dedicated

- Cloud instances (cost-optimized examples):
  - AWS c6i.4xlarge (16 vCPU) - cost-optimized for CPU workloads
  - AWS g5.xlarge (1 GPU) - for optional tensor workloads (use sparingly)

All machine-level details must be recorded in each run's results metadata (see Results/benchmark_results.csv).

Workload: Defines representative workloads used for benchmarking the Lotusv1 engine and agent mesh.

- Small synthetic FASTQ workloads: 100-10k reads for CI and early validation.
- Medium workload: 10k-1M reads for hosted benchmarking.
- Production workload: 1M+ reads on self-hosted runners with 24 CPUs/128GB.

Workload generation scripts: scripts/generate_fastq.py (synthetic workload generator). All workload parameters (reads, seed) must be recorded.

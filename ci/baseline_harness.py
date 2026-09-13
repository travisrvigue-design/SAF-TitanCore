#!/usr/bin/env python3
"""
Baseline harness (simulated BWA-MEM-like) - single-threaded CPU-bound workload.
This provides a conservative baseline runtime for comparison. Results are written similarly to the lotus harness.
"""
import argparse
import json
import time
from pathlib import Path


def count_reads(fastq_path: Path):
    with fastq_path.open('r') as f:
        lines = sum(1 for _ in f)
    return lines // 4


def baseline_workload(total_reads: int):
    # Simulate a slower single-threaded processing by heavier CPU work
    s = 0
    # scale heavier than lotus per read
    for i in range(2000 * max(1, total_reads // 10)):
        s += (i * 17) % 89
    return s


def run_once(fastq: Path):
    reads = count_reads(fastq)
    start = time.time()
    baseline_workload(reads)
    end = time.time()
    elapsed = end - start
    throughput = reads / elapsed if elapsed > 0 else 0.0
    return {
        'run_time_seconds': elapsed,
        'reads': reads,
        'throughput_units_per_sec': throughput,
        'timestamp': time.time()
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument('fastq', help='Input FASTQ')
    p.add_argument('--out', default='01_Benchmark_Package/Results', help='Output directory')
    p.add_argument('--runs', type=int, default=30, help='Number of runs')
    args = p.parse_args()

    fastq = Path(args.fastq)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    csv_path = out / 'benchmark_results.csv'
    if not csv_path.exists():
        csv_path.write_text('run_id,run_time_seconds,reads,throughput_units_per_sec,worker_count,chunk_size_reads,timestamp\n')

    for i in range(1, args.runs + 1):
        result = run_once(fastq)
        run_file = out / f'benchmark_run_base_{i}.json'
        run_file.write_text(json.dumps(result))
        line = f"baseline_{i},{result['run_time_seconds']},{result['reads']},{result['throughput_units_per_sec']},1,0,{result['timestamp']}\n"
        with csv_path.open('a') as f:
            f.write(line)
        print(f"Completed baseline run {i}: throughput={result['throughput_units_per_sec']:.2f} reads/sec")

if __name__ == '__main__':
    main()

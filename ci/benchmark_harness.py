#!/usr/bin/env python3
"""
Lotusv1 benchmark harness (simulated processing).
Processes a FASTQ file by partitioning reads and processing chunks concurrently to simulate agent worker parallelism.
Outputs per-run JSON to OUTDIR/benchmark_run_<i>.json and appends to OUTDIR/benchmark_results.csv
"""
import argparse
import json
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor


def count_reads(fastq_path: Path):
    # FASTQ has 4 lines per read
    with fastq_path.open('r') as f:
        lines = sum(1 for _ in f)
    return lines // 4


def process_chunk_workload(chunk_reads: int):
    # Simulate compute work proportional to chunk_reads
    # Use a small CPU-bound loop to simulate processing without sleeping
    s = 0
    for i in range(1000 * max(1, chunk_reads // 10)):
        s += (i * 31) % 97
    return s


def run_once(fastq: Path, outdir: Path, worker_count: int, chunk_size_reads: int):
    reads = count_reads(fastq)
    chunks = []
    # determine number of chunks
    num_chunks = max(1, reads // chunk_size_reads)
    # distribute reads approximately equally
    base = reads // num_chunks
    rem = reads % num_chunks
    for i in range(num_chunks):
        size = base + (1 if i < rem else 0)
        chunks.append(size)

    start = time.time()
    # process chunks in threadpool
    with ThreadPoolExecutor(max_workers=worker_count) as ex:
        futures = [ex.submit(process_chunk_workload, c) for c in chunks]
        # wait
        for f in futures:
            f.result()
    end = time.time()
    elapsed = end - start
    throughput = reads / elapsed if elapsed > 0 else 0.0
    return {
        'run_time_seconds': elapsed,
        'reads': reads,
        'throughput_units_per_sec': throughput,
        'worker_count': worker_count,
        'chunk_size_reads': chunk_size_reads,
        'timestamp': time.time()
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument('fastq', help='Input FASTQ')
    p.add_argument('--out', default='01_Benchmark_Package/Results', help='Output directory')
    p.add_argument('--runs', type=int, default=30, help='Number of independent runs')
    p.add_argument('--workers', type=int, default=8, help='Worker threads')
    p.add_argument('--chunk', type=int, default=200, help='Reads per chunk')
    args = p.parse_args()

    fastq = Path(args.fastq)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    csv_path = out / 'benchmark_results.csv'
    # if CSV missing, write header
    if not csv_path.exists():
        csv_path.write_text('run_id,run_time_seconds,reads,throughput_units_per_sec,worker_count,chunk_size_reads,timestamp\n')

    for i in range(1, args.runs + 1):
        result = run_once(fastq, out, args.workers, args.chunk)
        run_file = out / f'benchmark_run_lotus_{i}.json'
        run_file.write_text(json.dumps(result))
        line = f"lotus_{i},{result['run_time_seconds']},{result['reads']},{result['throughput_units_per_sec']},{result['worker_count']},{result['chunk_size_reads']},{result['timestamp']}\n"
        with csv_path.open('a') as f:
            f.write(line)
        print(f"Completed lotus run {i}: throughput={result['throughput_units_per_sec']:.2f} reads/sec")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Deterministic FASTQ generator for CI and benchmarking.
Usage: python scripts/generate_fastq.py output.fastq --reads 100 --seed 42 --length 100
"""
import argparse
import random
from pathlib import Path

NUCLS = ['A', 'C', 'G', 'T']


def random_seq(length, rng):
    return ''.join(rng.choice(NUCLS) for _ in range(length))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('output', help='Output FASTQ file')
    p.add_argument('--reads', type=int, default=100, help='Number of reads to generate')
    p.add_argument('--seed', type=int, default=42, help='Random seed for reproducibility')
    p.add_argument('--length', type=int, default=100, help='Read length (bases)')
    args = p.parse_args()

    rng = random.Random(args.seed)
    outp = Path(args.output)
    outp.parent.mkdir(parents=True, exist_ok=True)

    with outp.open('w') as f:
        for i in range(args.reads):
            header = f"@read_{i}"
            seq = random_seq(args.length, rng)
            qual = 'I' * args.length
            f.write(f"{header}\n{seq}\n+\n{qual}\n")

if __name__ == '__main__':
    main()

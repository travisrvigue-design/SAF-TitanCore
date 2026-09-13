#!/usr/bin/env python3
"""Generate small synthetic FASTQ test vectors for deterministic testing."""
import argparse
from random import Random

BASES = ["A","C","G","T"]


def random_read(rng, length=100):
    return ''.join(rng.choice(BASES) for _ in range(length))


def generate_fastq(output, reads=100, seed=42):
    rng = Random(seed)
    with open(output, 'w') as f:
        for i in range(reads):
            f.write(f"@read{i}\n")
            f.write(random_read(rng) + "\n")
            f.write("+\n")
            f.write("~" * 100 + "\n")
    print("wrote", output)


if __name__ == '__main__':
    import sys
    p = argparse.ArgumentParser()
    p.add_argument('out', help='Output FASTQ file')
    p.add_argument('--reads', type=int, default=100)
    p.add_argument('--seed', type=int, default=42)
    args = p.parse_args()
    generate_fastq(args.out, args.reads, args.seed)

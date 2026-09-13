#!/usr/bin/env python3
"""
Simple FASTQ partitioner. Splits an input FASTQ into multiple unit files with a deterministic order.
Usage: python scripts/partitioner.py input.fastq --out outdir --reads-per-file 10 --seed 42
"""
import argparse
from pathlib import Path


def iter_fastq(path):
    with open(path, 'r') as f:
        while True:
            header = f.readline()
            if not header:
                break
            seq = f.readline()
            plus = f.readline()
            qual = f.readline()
            if not qual:
                break
            yield header, seq, plus, qual


def main():
    p = argparse.ArgumentParser()
    p.add_argument('input', help='Input FASTQ file')
    p.add_argument('--out', required=True, help='Output directory for units')
    p.add_argument('--reads-per-file', type=int, default=10)
    p.add_argument('--seed', type=int, default=42, help='Deterministic ordering seed (not used currently)')
    args = p.parse_args()

    inp = Path(args.input)
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    unit_idx = 0
    read_count = 0
    out_f = None
    for h, s, p_line, q in iter_fastq(str(inp)):
        if read_count % args.reads_per_file == 0:
            if out_f:
                out_f.close()
            out_path = outdir / f'unit_{unit_idx}.fastq'
            out_f = open(out_path, 'w')
            unit_idx += 1
        out_f.write(h)
        out_f.write(s)
        out_f.write(p_line)
        out_f.write(q)
        read_count += 1
    if out_f:
        out_f.close()

    # Write a simple manifest of created units
    manifest = outdir / 'units_manifest.txt'
    with manifest.open('w') as mf:
        for f in sorted(outdir.glob('unit_*.fastq')):
            mf.write(f.name + '\n')

if __name__ == '__main__':
    main()

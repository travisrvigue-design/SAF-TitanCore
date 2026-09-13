#!/usr/bin/env python3
"""Deterministic partitioner for FASTQ-like text files.
Produces unit files and a manifest with SHA-256 digests.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path

CHUNK_LINES = 4000  # small example; tune per variant


def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def partition_fastq(input_path, out_dir, chunk_lines=CHUNK_LINES):
    in_path = Path(input_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {"dataset_id": in_path.stem, "units": [], "created_at": None}
    unit_idx = 0
    with in_path.open("r") as f:
        buffer = []
        for i, line in enumerate(f, start=1):
            buffer.append(line)
            if i % chunk_lines == 0:
                unit_idx += 1
                unit_name = f"{in_path.stem}-unit-{unit_idx:04d}.fastq"
                unit_path = out_dir / unit_name
                with unit_path.open("w") as u:
                    u.writelines(buffer)
                digest = sha256_of_file(unit_path)
                manifest["units"].append({"unit_id": unit_name, "path": str(unit_path), "sha256": digest})
                buffer = []
        if buffer:
            unit_idx += 1
            unit_name = f"{in_path.stem}-unit-{unit_idx:04d}.fastq"
            unit_path = out_dir / unit_name
            with unit_path.open("w") as u:
                u.writelines(buffer)
            digest = sha256_of_file(unit_path)
            manifest["units"].append({"unit_id": unit_name, "path": str(unit_path), "sha256": digest})
    return manifest


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("input", help="Input FASTQ-like text file")
    p.add_argument("--out", default="./units", help="Output directory for units")
    args = p.parse_args()
    manifest = partition_fastq(args.input, args.out)
    manifest["created_at"] = __import__("datetime").datetime.utcnow().isoformat() + "Z"
    with open(os.path.join(args.out, "manifest.json"), "w") as mf:
        json.dump(manifest, mf, indent=2)
    print("Wrote", os.path.join(args.out, "manifest.json"))

#!/usr/bin/env bash
set -euo pipefail

echo "Running CI smoke script"
python -V
python scripts/generate_fastq.py tests/resources/small.fastq --reads 20 --seed 7
python scripts/partitioner.py tests/resources/small.fastq --out tests/resources/units
pytest -q --junitxml=reports/junit.xml


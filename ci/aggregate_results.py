#!/usr/bin/env python3
"""
Aggregator helper: converts per-run JSONs into a single CSV for archival.
"""
import json
from pathlib import Path
import csv

out = Path('01_Benchmark_Package/Results')
jsons = sorted(out.glob('benchmark_run_*.json'))
rows = []
for j in jsons:
    d = json.loads(j.read_text())
    rows.append(d)

csvp = out / 'aggregated_runs.csv'
with csvp.open('w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['run_time_seconds','reads','throughput_units_per_sec','worker_count','chunk_size_reads','timestamp'])
    for r in rows:
        writer.writerow([r.get('run_time_seconds'), r.get('reads'), r.get('throughput_units_per_sec'), r.get('worker_count', ''), r.get('chunk_size_reads',''), r.get('timestamp')])
print('Wrote', csvp)

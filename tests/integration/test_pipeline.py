"""
Integration test: generate FASTQ -> partition -> check outputs.
"""
import subprocess
from pathlib import Path


def test_generate_and_partition(tmp_path):
    out_fastq = tmp_path / "small.fastq"
    out_units = tmp_path / "units"
    out_units.mkdir()

    # Generate
    result = subprocess.run(
        ["python", "scripts/generate_fastq.py", str(out_fastq), "--reads", "10", "--seed", "123"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert out_fastq.exists()
    assert out_fastq.stat().st_size > 0

    # Partition
    result = subprocess.run(
        ["python", "scripts/partitioner.py", str(out_fastq), "--out", str(out_units), "--reads-per-file", "5"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr

    units = list(out_units.glob("unit_*.fastq"))
    assert len(units) >= 1

    manifest = out_units / "units_manifest.txt"
    assert manifest.exists()
    assert "unit_" in manifest.read_text()

"""
Unit tests for the FASTQ partitioner script.
"""
import subprocess
from pathlib import Path


def test_partitioner_creates_units(tmp_path):
    # Create a tiny FASTQ
    input_file = tmp_path / "test.fastq"
    input_file.write_text("@r1\nACGT\n+\n~~~~\n@r2\nTGCA\n+\n~~~~\n")

    out = tmp_path / "units"
    out.mkdir()

    result = subprocess.run(
        ["python", "scripts/partitioner.py", str(input_file), "--out", str(out), "--reads-per-file", "1"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr

    # Should have created unit files + manifest
    units = list(out.glob("unit_*.fastq"))
    assert len(units) >= 1

    manifest = out / "units_manifest.txt"
    assert manifest.exists()
    content = manifest.read_text().strip()
    assert "unit_" in content


def test_partitioner_deterministic(tmp_path):
    input_file = tmp_path / "test.fastq"
    input_file.write_text("@r1\nA\n+\n~\n@r2\nC\n+\n~\n@r3\nG\n+\n~\n")

    out1 = tmp_path / "units1"
    out2 = tmp_path / "units2"
    out1.mkdir()
    out2.mkdir()

    subprocess.run(
        ["python", "scripts/partitioner.py", str(input_file), "--out", str(out1), "--reads-per-file", "1"],
        check=True,
    )
    subprocess.run(
        ["python", "scripts/partitioner.py", str(input_file), "--out", str(out2), "--reads-per-file", "1"],
        check=True,
    )

    files1 = sorted(p.name for p in out1.glob("unit_*.fastq"))
    files2 = sorted(p.name for p in out2.glob("unit_*.fastq"))
    assert files1 == files2

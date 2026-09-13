import subprocess
import json


def test_manifest_and_hash(tmp_path):
    # Generate a small fastq
    out_fastq = tmp_path / "small.fastq"
    subprocess.run(["python", "scripts/generate_fastq.py", str(out_fastq), "--reads", "10", "--seed", "123"], check=True)
    out_units = tmp_path / "units"
    out_units.mkdir()
    subprocess.run(["python", "scripts/partitioner.py", str(out_fastq), "--out", str(out_units)], check=True)
    manifest = json.loads((out_units / "manifest.json").read_text())
    assert len(manifest['units']) >= 1

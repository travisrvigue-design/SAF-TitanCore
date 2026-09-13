"""
Utility: manifest hashing for datasets and artifacts.
"""
import hashlib
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def write_manifest(directory: Path, out_path: Path):
    files = sorted([p for p in directory.rglob('*') if p.is_file()])
    manifest = []
    for f in files:
        manifest.append({'path': str(f.relative_to(directory)), 'sha256': sha256_file(f)})
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text('\n'.join([f"{m['sha256']}  {m['path']}" for m in manifest]))

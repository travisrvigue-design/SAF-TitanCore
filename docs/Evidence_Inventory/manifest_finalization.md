# Manifest Verification & Finalization Instructions

This file describes the exact commands to compute and commit the final repository manifest (REP-001) and verify the Inventory Log (VVP-001). Follow these steps in your clean-room environment or CI runner.

1) Create a clean Python environment
- python3 -m venv .venv && source .venv/bin/activate
- pip install --upgrade pip
- pip install -r requirements.txt

2) Compute the manifest (writes 01_Benchmark_Package/Results/repo_manifest.txt)
- python -c "from pathlib import Path; from src.utils.hash_manifest import write_manifest; write_manifest(Path('.'), Path('01_Benchmark_Package/Results/repo_manifest.txt'))"

3) Validate the manifest has no 'TBD' placeholders
- grep -n "TBD" 01_Benchmark_Package/Results/repo_manifest.txt || echo "All hashes present"

4) Commit the final manifest and Inventory_Log.md
- git add 01_Benchmark_Package/Results/repo_manifest.txt docs/Evidence_Inventory/Inventory_Log.md
- git commit -m "REP-001: Finalized repo_manifest with computed SHA-256s (VVP-001)" && git push origin main

5) Optional GPG signing (SEC-001)
- Sign the manifest outside the repo and upload the signature file (do NOT commit private keys):
  - gpg --armor --output repo_manifest.txt.asc --detach-sign 01_Benchmark_Package/Results/repo_manifest.txt
  - git add repo_manifest.txt.asc && git commit -m "SEC-001: repo_manifest signature" && git push origin main

Notes on automation
- You can automate steps 2-4 in CI (recommended) with a controlled runner that has access to the artifacts.
- For highest integrity, perform the hash computation in an immutable clean-room container (docker build --no-cache) and verify the container digest as part of REP-001.

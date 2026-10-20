# GitHub Copilot Prompt Pack for SAF-TitanCore

## 1. Diagnose the blocker
@workspace The GitHub Actions runs for this repo currently fail with conclusion: startup_failure and path: BuildFailed. No jobs are created. Review the workflow files, repo settings, and branch configuration to identify the most likely causes. Tell me the exact checks to do in the GitHub UI and the precise YAML fixes that would resolve it.

## 2. Review all workflows
@workspace Review .github/workflows/*.yml and tell me whether anything is still wrong for ubuntu-latest runners, free GitHub accounts, the current default branch, or repository/action permissions. Highlight any invalid YAML, missing actions, unsupported syntax, or branch/path issues.

## 3. Verify the repo is ready
@workspace Looking at the current main branch, are the tests, workflow files, scripts, and project structure in a state that should pass once GitHub Actions is allowed to run? Identify any blockers, config mismatches, or missing required files.

## 4. Local verification commands
@workspace Give me the exact local commands to run the same checks the CI workflow would run, using only my local shell. Include test suite commands, any PoC harness commands, and a short explanation of what each command validates.

## 5. Root-cause focus
@workspace Check for repo-specific issues that commonly trigger startup_failure or BuildFailed in GitHub Actions: invalid YAML, bad branch filters, missing workflow files, unsupported runner image, missing permissions, or syntax errors in the workflow file. Show the minimum fix.

## 6. Specific file fix (example)
@workspace In src/kegg_adapter.py, make sure network errors never crash CI, keep the existing cache behavior, and preserve compatibility with the current unit tests. Provide the minimal safe patch and explain why it fixes the failure.

## 7. Test vs implementation check
@workspace Explain how tests/unit/test_partitioner.py works, compare it to scripts/partitioner.py, and tell me whether they match the expected behavior for the current PoC or benchmark.

## 8. Single workflow review
/explain Is this workflow correctly configured for a free GitHub account using ubuntu-latest? Identify anything that would cause startup_failure, BuildFailed, or jobs to never launch.

## Local CI verification checklist

```bash
# 1. Clone / enter the repo
cd SAF-TitanCore

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the test suite (same as CI)
pytest -q

# 5. Smoke the main scripts
python scripts/generate_fastq.py /tmp/small.fastq --reads 50 --seed 123
python scripts/partitioner.py /tmp/small.fastq --out /tmp/units

# 6. (Optional) Run a short PoC harness
python ci/baseline_harness.py /tmp/small.fastq --out /tmp/results --runs 3
python ci/benchmark_harness.py /tmp/small.fastq --out /tmp/results --runs 3 --workers 4 --chunk 100
```

## GitHub UI checklist for the startup_failure issue

1. Repo → Settings → Actions → General
   - Actions enabled?
   - “Allow all actions and reusable workflows” selected?
2. Confirm default branch is main
3. Confirm workflow files exist under `.github/workflows/`
4. Account → Settings → Billing
   - Check remaining Actions minutes / spending limits
5. After fixing settings, re-run a workflow or push a tiny commit

## Quick summary
Likely causes of the exact failure:
- Workflow YAML is invalid or malformed
- GitHub Actions is disabled at repo or org level
- Workflow is configured for the wrong branch
- The repo is blocked by organization policy or billing restrictions
- A required action path or script path is missing, so GitHub fails before jobs start
- The workflow references an unavailable runner or unsupported setup

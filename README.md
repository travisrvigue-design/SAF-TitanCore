.github/workflows/policy-check.yml
name: Policy Check

on:
  push:
    branches:
      - "**"
  pull_request:
    branches:
      - "**"
  workflow_dispatch:

jobs:
  workflow-policy:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Enforce fail-closed workflow policy
        run: |
          python scripts/ci/workflow_policy_check.py

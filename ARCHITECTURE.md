# System Architecture — SAF TitanCore (Monorepo)

This repository captures the system architecture and deliverables for three SAF variants: Lotusv1, Ludus, and Luda.

Goals
- Deterministic ingest and SHA-256 manifests
- Verifiable, signed artifacts (Sigstore / cosign recommended)
- Structured logging and immutable audit trail
- Reproducible tests and benchmarks
- Human-in-loop gating enforced by CI

Mermaid overview (rendered in compatible viewers):

```mermaid
flowchart TD
  A[Tier 1: Ingestion & Edge Mesh] --> B[Tier 2: Hybrid Agent Engine (Lotusv1 / Ludus / Luda)]
  B --> C[Tier 3: Verification & Governance]
  C --> D[Tier 4: Secure Data Storage Layer]
  subgraph Ingest
    A1[FASTQ/BAM feeds] --> A2[Partitioner & SHA-256 manifests]
  end
  subgraph Agents
    B1[ACO Path Routers]
    B2[Q-LINK Plateau Mitigation]
    B3[Parallel Worker Nodes]
  end
  B --> B1 & B2 & B3
  C --> C1[Statistical Eval (MSE, t-test, Cohen's d)]
  C --> C2[GPG / Sigstore signatures]
  C --> C3[Human SOP-001 Gate]
  D --> D1[Immutable Log Sinks]
  D --> D2[Versioned Manifests (SHA-256)]
```

See per-variant ARCHITECTURE.md files for details.

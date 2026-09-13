# Key management and signing guide

Recommended: use Sigstore / cosign with OIDC (GitHub Actions) to sign containers and artifacts without storing long-lived keys.

Alternative: GPG keys stored in a dedicated KMS/HSM and accessed via CI with short-lived credentials. Never store private keys in the repo.

See .github/workflows/sign.yml for signing workflow template.

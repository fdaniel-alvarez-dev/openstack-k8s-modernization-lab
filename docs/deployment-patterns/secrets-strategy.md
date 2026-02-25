# Deployment Pattern: Secrets Strategy

## Goals
- Reduce secret sprawl and uncontrolled access.

## Pattern
- Prefer external secrets backends in real deployments (vault-like patterns).
- Rotate credentials on schedule and after incidents.
- Avoid committing secrets; enforce scanning in CI.


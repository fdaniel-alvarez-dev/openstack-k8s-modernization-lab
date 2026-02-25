# Deployment Pattern: GitOps-Friendly Repository Layout

## Goals
- Make change review the primary control plane.

## Pattern
- Separate `apps/` from `platform/`.
- Define environments as overlays (`dev`, `stage`, `prod`).
- Require PR-based approvals for platform changes.


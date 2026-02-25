# Runbook: Upgrades (OpenStack + Kubernetes)

## Goals
- Predictable upgrades with clear rollback and validation.

## Pre-flight
- Confirm HA status and backups (DB, control-plane configuration).
- Review dependency matrix (API compatibility, CNI/CSI versions).
- Freeze high-risk changes during maintenance windows.

## Execution (high level)
- OpenStack: follow controller upgrade workflow; validate DB/message bus health; verify service endpoints.
- Kubernetes: follow release cadence; validate baseline policies and RBAC; run conformance smoke checks.

## Validation
- API readiness, control-plane health, and representative workload checks.
- SLO burn-rate remains within limits post-change.


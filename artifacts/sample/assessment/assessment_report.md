# Modernization Assessment: legacy-prod-east

## Executive overview
Legacy infrastructure showed reliability and provisioning constraints driven by operational variance and manual touchpoints.

## Assessment scores (0–100)
- Reliability risk (higher is worse): **85.6**
- Operational maturity: **33.9**
- Automation maturity: **25.2**
- Standardization: **25.0**

## Key findings
- Provisioning workflow P50 is ~110.0 minutes with 11 manual touchpoints.
- Control plane HA is not enabled; reliability risk increases during upgrades and failures.
- Config drift rate is 17.5%, indicating inconsistent operations.
- Automation maturity is low; inconsistent provisioning and manual changes drive variance.
- East-west visibility is low; change impact is harder to predict and validate.

## Prioritized recommendations
### R-001 — Harden OpenStack control plane (HA, clustered DB and message bus)
- Priority: 1
- Effort: M | Impact: H | Risk reduction: H
- Tags: openstack, reliability, control-plane
- Rationale: Reduce single points of failure and improve recovery behavior by standardizing HA patterns across controller services.

### A-010 — Shift to automation-first provisioning (Terraform patterns + Ansible enforcement)
- Priority: 2
- Effort: M | Impact: H | Risk reduction: H
- Tags: terraform, ansible, devops, automation
- Rationale: Lower error rate and cycle time by making provisioning deterministic, reviewable, and easier to validate.

### K-020 — Standardize Kubernetes baseline (namespaces, RBAC, policies, and release cadence)
- Priority: 3
- Effort: M | Impact: H | Risk reduction: M
- Tags: kubernetes, standardization
- Rationale: Reduce operational variance and improve day-2 reliability with consistent cluster standards and upgrade practices.

### O-030 — Operationalize SLOs, runbooks, and change management gates
- Priority: 4
- Effort: S | Impact: H | Risk reduction: H
- Tags: operations, sre, governance
- Rationale: Sustain reliability gains by turning standards into daily practice (incident response, upgrades, backups, and capacity reviews).

### N-040 — Improve east-west visibility and change safety (baseline telemetry + review workflow)
- Priority: 5
- Effort: S | Impact: M | Risk reduction: M
- Tags: network, observability
- Rationale: Lower change failure rate by tightening feedback loops and visibility for internal traffic and service dependencies.

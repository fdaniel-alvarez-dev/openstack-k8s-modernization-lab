# Runbook: Incident Response (sev1–sev3)

## Purpose
Reduce MTTR and prevent recurrence with consistent triage, escalation, and post-incident learning.

## Triggers
- SLO burn-rate alert, service unavailability, or customer-impacting latency.

## Steps
1. Confirm severity (sev1/sev2/sev3) and assign incident commander.
2. Stabilize: stop the bleeding (rollback change, isolate blast radius, fail over if needed).
3. Collect evidence: timelines, logs, metrics, and key events (controller, network, storage).
4. Communicate: status updates at a fixed cadence; identify internal/external stakeholders.
5. Recover: validate service health, error rates, and SLO compliance.
6. Post-incident review: root cause, contributing factors, corrective actions with owners and due dates.

## Definition of done
- Services stable, customer-impact resolved, and action items created with measurable follow-up.


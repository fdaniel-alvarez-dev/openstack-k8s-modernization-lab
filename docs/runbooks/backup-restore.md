# Runbook: Backup and Restore Validation

## Purpose
Ensure backups are restorable and aligned to RTO/RPO.

## Routine checks
- Daily: backup job success rate, storage capacity headroom.
- Weekly: sample restore test (small but representative dataset).
- Monthly: full restore rehearsal (document duration and gaps).

## Restore steps (outline)
1. Identify restore point and required scope (DB, configs, workload state).
2. Restore to isolated environment if possible.
3. Validate integrity and service health.
4. Document actual RTO/RPO and any deviations.


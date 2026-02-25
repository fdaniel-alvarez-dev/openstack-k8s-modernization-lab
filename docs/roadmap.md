# Modernization Roadmap (Phased)

This roadmap is intentionally outcomes-driven and measurable. It aligns reliability (99.9% uptime) and speed (~40% faster provisioning) to concrete platform and operations changes.

## 0–30 days (Stabilize + baseline)
- Establish baseline KPIs: uptime trend, incident taxonomy, provisioning workflow P50/P95, change failure rate.
- Define target SLOs/SLIs and an escalation policy aligned to severity (sev1–sev3).
- Freeze uncontrolled changes: introduce a minimal change gate for OpenStack controller and network changes.
- Validate backups/restores and document RTO/RPO expectations.

## 30–90 days (Standardize + automate)
- Standardize OpenStack controller HA patterns (clustered DB + message bus, repeatable maintenance workflow).
- Define and publish Kubernetes baseline (namespaces/RBAC/policies + release cadence).
- Implement automation-first provisioning patterns:
  - Terraform plans as the change contract (reviewable diffs)
  - Ansible enforcement for configuration conventions and drift reduction
- Introduce a lightweight runbook library and start “incident learning” updates after sev1/sev2 events.

## 90–180 days (Scale + sustain)
- Mature upgrades: prefer blue/green patterns where feasible; automate pre-flight and post-check validation.
- Expand observability coverage: east-west visibility, dependency mapping, and SLO burn-rate alerting.
- Institutionalize quarterly capacity + cost review: tie demand forecasts to platform scaling decisions.
- Enforce policy-as-code where appropriate (RBAC maturity, change controls, baseline drift detection).


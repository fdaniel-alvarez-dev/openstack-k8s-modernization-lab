# Ops Standard: Naming Conventions

## Goals
- Reduce ambiguity and improve operability across OpenStack and Kubernetes.

## Conventions
- Tenants/projects: `tenant-<org>-<env>`
- Networks: `net-<tenant>-<zone>`
- Kubernetes namespaces: `<team>-<env>` plus `platform-system` reserved for platform tooling
- Tags/labels: `owner`, `env`, `service`, `criticality`


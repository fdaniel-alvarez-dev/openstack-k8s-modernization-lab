# ADR-0002: Enforce a Kubernetes Baseline (RBAC, Namespaces, Policies)

## Context
Inconsistent cluster configuration creates drift and complicates troubleshooting.

## Decision
Define a baseline for namespaces, RBAC, and policy controls and treat it as versioned infrastructure.

## Trade-offs
- Pros: consistent operations, safer multi-tenancy, reduced variance.
- Cons: teams must align to standards and adopt a change workflow.

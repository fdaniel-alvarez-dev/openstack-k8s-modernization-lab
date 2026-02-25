# ADR-0001: Standardize OpenStack Control Plane HA

## Context
Legacy operations experienced reliability incidents during controller maintenance and upgrades.

## Decision
Adopt a consistent HA pattern for controller services with clustered database and message bus.

## Trade-offs
- Pros: reduced SPOFs, improved recovery, more predictable upgrades.
- Cons: added operational complexity and careful capacity planning required.

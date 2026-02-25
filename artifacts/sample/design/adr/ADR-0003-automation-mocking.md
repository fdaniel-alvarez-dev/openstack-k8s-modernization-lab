# ADR-0003: Local-First Automation Simulation with Mock Runners

## Context
This lab must run without cloud credentials and without requiring a live OpenStack/Kubernetes platform.

## Decision
Ship real Terraform/Ansible artifacts, but execute via mock runners by default. If binaries are available, attempt real execution and fall back to mocks on failure.

## Trade-offs
- Pros: reproducible demo, testable behaviors, portfolio-friendly evidence.
- Cons: does not prove provider-specific edge cases without real infrastructure.

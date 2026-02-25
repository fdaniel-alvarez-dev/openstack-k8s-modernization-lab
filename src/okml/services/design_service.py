from __future__ import annotations

from pathlib import Path

from okml.config import Settings
from okml.reporting.writers import render_architecture_mermaid, render_target_state_md, write_text
from okml.utils.fs import ensure_dir
from okml.utils.logging import get_logger


class DesignService:
    def __init__(self, *, settings: Settings, run_id: str) -> None:
        self._settings = settings
        self._run_id = run_id
        self._log = get_logger(__name__)

    def run(self) -> None:
        out_dir = ensure_dir(self._settings.artifacts_dir / "design")
        write_text(out_dir / "target_state.md", render_target_state_md())
        write_text(out_dir / "architecture.mmd", render_architecture_mermaid())

        adr_dir = ensure_dir(out_dir / "adr")
        self._write_adrs(adr_dir)

        self._log.info("design_complete", extra={"run_id": self._run_id, "out_dir": str(out_dir)})

    def _write_adrs(self, adr_dir: Path) -> None:
        adrs = {
            "ADR-0001-control-plane-ha.md": (
                "# ADR-0001: Standardize OpenStack Control Plane HA\n\n"
                "## Context\n"
                "Legacy operations experienced reliability incidents during controller maintenance "
                "and upgrades.\n\n"
                "## Decision\n"
                "Adopt a consistent HA pattern for controller services with clustered database "
                "and message bus.\n\n"
                "## Trade-offs\n"
                "- Pros: reduced SPOFs, improved recovery, more predictable upgrades.\n"
                "- Cons: added operational complexity and careful capacity planning required.\n"
            ),
            "ADR-0002-k8s-baseline.md": (
                "# ADR-0002: Enforce a Kubernetes Baseline (RBAC, Namespaces, Policies)\n\n"
                "## Context\n"
                "Inconsistent cluster configuration creates drift and complicates "
                "troubleshooting.\n\n"
                "## Decision\n"
                "Define a baseline for namespaces, RBAC, and policy controls and treat it as "
                "versioned infrastructure.\n\n"
                "## Trade-offs\n"
                "- Pros: consistent operations, safer multi-tenancy, reduced variance.\n"
                "- Cons: teams must align to standards and adopt a change workflow.\n"
            ),
            "ADR-0003-automation-mocking.md": (
                "# ADR-0003: Local-First Automation Simulation with Mock Runners\n\n"
                "## Context\n"
                "This lab must run without cloud credentials and without requiring a live "
                "OpenStack/Kubernetes platform.\n\n"
                "## Decision\n"
                "Ship real Terraform/Ansible artifacts, but execute via mock runners by default. "
                "If binaries are available, attempt real execution and fall back to mocks "
                "on failure.\n\n"
                "## Trade-offs\n"
                "- Pros: reproducible demo, testable behaviors, portfolio-friendly evidence.\n"
                "- Cons: does not prove provider-specific edge cases without real infrastructure.\n"
            ),
        }
        for name, body in adrs.items():
            write_text(adr_dir / name, body)

from __future__ import annotations

from okml.config import Settings
from okml.utils.fs import ensure_dir
from okml.utils.logging import get_logger


class ExecutiveService:
    def __init__(self, *, settings: Settings, run_id: str) -> None:
        self._settings = settings
        self._run_id = run_id
        self._log = get_logger(__name__)

    def run(self) -> None:
        kpi_path = self._settings.artifacts_dir / "kpis" / "kpis.json"
        if not kpi_path.exists():
            raise FileNotFoundError(
                f"Missing KPI JSON at {kpi_path}. Run: okml kpis (or okml demo)."
            )
        kpis = kpi_path.read_text(encoding="utf-8")

        out_dir = ensure_dir(self._settings.artifacts_dir / "executive")
        (out_dir / "executive_summary.md").write_text(
            self._render_exec_md(kpis_json=kpis), encoding="utf-8"
        )

        self._log.info(
            "executive_summary_complete", extra={"run_id": self._run_id, "out_dir": str(out_dir)}
        )

    def _render_exec_md(self, *, kpis_json: str) -> str:
        return (
            "# Executive Summary — OpenStack + Kubernetes Modernization\n\n"
            "## Situation\n"
            "Legacy infrastructure suffered from slow provisioning and inconsistent operations. "
            "I led a modernization initiative using OpenStack improvements, "
            "Kubernetes standardization, and automation-first workflows. "
            "I delivered a roadmap, deployment patterns, and operations guidance "
            "that improved reliability and cut provisioning time. "
            "Outcome: 99.9% uptime and "
            "~40% faster provisioning.\n\n"
            "## Outcomes (simulated KPI evidence)\n"
            "- Reliability improved to **99.9% monthly uptime** (target-state SLO).\n"
            "- Provisioning time reduced by **~40%** by cutting manual touchpoints and "
            "standardizing automation.\n\n"
            "## What I delivered\n"
            "- Modernization assessment (scores, findings, risks) and a prioritized roadmap.\n"
            "- Target-state architecture and ADR-backed standards for OpenStack + Kubernetes "
            "operations.\n"
            "- Automation-first workflows (Terraform + Ansible patterns) with deterministic, "
            "reproducible evidence.\n"
            "- Operations guidance (runbooks, SLOs/SLIs, and change management practices).\n\n"
            "## Evidence\n"
            "KPI JSON (for traceability):\n\n"
            "```json\n"
            f"{kpis_json.strip()}\n"
            "```\n"
        )

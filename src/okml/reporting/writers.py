from __future__ import annotations

import base64
import csv
import json
import os
import tempfile
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "okml-mplconfig"))

import matplotlib.pyplot as plt

from okml.domain.models import AssessmentReport, RoadmapItem
from okml.utils.fs import ensure_dir


def write_json(path: Path, payload: object) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    ensure_dir(path.parent)
    path.write_text(text, encoding="utf-8")


def write_risk_register_csv(path: Path, recommendations: list[RoadmapItem]) -> None:
    ensure_dir(path.parent)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["risk_id", "risk", "mitigation", "priority"])
        for i, rec in enumerate(recommendations, start=1):
            w.writerow([f"RISK-{i:03d}", rec.title, rec.rationale, rec.priority])


def render_assessment_md(report: AssessmentReport) -> str:
    env = report.env
    s = report.scores
    lines = [
        f"# Modernization Assessment: {env.name}",
        "",
        "## Executive overview",
        "Legacy infrastructure showed reliability and provisioning constraints driven by "
        "operational variance and manual touchpoints.",
        "",
        "## Assessment scores (0–100)",
        f"- Reliability risk (higher is worse): **{s.reliability_risk}**",
        f"- Operational maturity: **{s.operational_maturity}**",
        f"- Automation maturity: **{s.automation_maturity}**",
        f"- Standardization: **{s.standardization}**",
        "",
        "## Key findings",
    ]
    lines += [f"- {f}" for f in report.findings]
    lines += ["", "## Prioritized recommendations"]
    for r in report.recommendations:
        lines += [
            f"### {r.id} — {r.title}",
            f"- Priority: {r.priority}",
            f"- Effort: {r.effort} | Impact: {r.impact} | Risk reduction: {r.risk_reduction}",
            f"- Tags: {', '.join(r.tags)}",
            f"- Rationale: {r.rationale}",
            "",
        ]
    return "\n".join(lines).rstrip() + "\n"


def plot_uptime_trend_png(path: Path, *, before_uptime: float, after_uptime: float) -> None:
    ensure_dir(path.parent)
    months = ["M-2", "M-1", "M0", "M+1", "M+2", "M+3"]
    series = [
        before_uptime - 0.25,
        before_uptime - 0.12,
        before_uptime,
        min(after_uptime, before_uptime + 0.35),
        min(after_uptime, before_uptime + 0.5),
        after_uptime,
    ]
    plt.figure(figsize=(8, 3))
    plt.plot(months, series, marker="o")
    plt.ylim(97.0, 100.0)
    plt.title("Monthly Uptime Trend (Simulated)")
    plt.ylabel("Uptime (%)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def plot_provisioning_time_png(path: Path, *, before_p50: float, after_p50: float) -> None:
    ensure_dir(path.parent)
    labels = ["Before", "After"]
    vals = [before_p50, after_p50]
    plt.figure(figsize=(5, 3))
    plt.bar(labels, vals, color=["#C43C35", "#2E8B57"])
    plt.title("Provisioning Time P50 (Simulated)")
    plt.ylabel("Minutes")
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def render_kpis_md(kpis: dict[str, dict[str, float]]) -> str:
    b = kpis["before"]
    a = kpis["after"]
    improvement = 1.0 - (a["provisioning_time_minutes_p50"] / b["provisioning_time_minutes_p50"])
    return (
        "# KPI Evidence Pack\n\n"
        "## Reliability\n"
        f"- Before: **{b['uptime_monthly_percent']}%** monthly uptime\n"
        f"- After: **{a['uptime_monthly_percent']}%** monthly uptime\n\n"
        "## Provisioning speed\n"
        f"- Before P50: **{b['provisioning_time_minutes_p50']} min**\n"
        f"- After P50: **{a['provisioning_time_minutes_p50']} min**\n"
        f"- Improvement: **{round(improvement * 100, 1)}%**\n"
    )


def render_dashboard_html(
    *,
    path: Path,
    kpis: dict[str, dict[str, float]],
    uptime_png: Path,
    provisioning_png: Path,
) -> None:
    def as_data_uri(p: Path) -> str:
        data = p.read_bytes()
        b64 = base64.b64encode(data).decode("ascii")
        return f"data:image/png;base64,{b64}"

    ensure_dir(path.parent)
    uptime_uri = as_data_uri(uptime_png)
    prov_uri = as_data_uri(provisioning_png)
    html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>OKML KPI Dashboard</title>
    <style>
      body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; margin: 2rem; }}
      .grid {{ display: grid; grid-template-columns: 1fr; gap: 1.5rem; max-width: 980px; }}
      .card {{ border: 1px solid #e5e7eb; border-radius: 12px; padding: 1rem 1.25rem; }}
      h1 {{ margin: 0 0 0.5rem 0; }}
      .kpi {{ display: flex; gap: 1.25rem; flex-wrap: wrap; }}
      .kpi div {{
        background: #f9fafb;
        border: 1px solid #eef2f7;
        padding: 0.75rem 1rem;
        border-radius: 10px;
      }}
      img {{ width: 100%; height: auto; border-radius: 8px; border: 1px solid #f0f0f0; }}
      code {{ background: #f3f4f6; padding: 0.1rem 0.3rem; border-radius: 6px; }}
    </style>
  </head>
  <body>
    <div class="grid">
      <div class="card">
        <h1>OpenStack + Kubernetes Modernization | KPI Evidence</h1>
        <p>
          This dashboard is generated locally by <code>okml kpis</code> with deterministic inputs.
        </p>
        <div class="kpi">
          <div><strong>Before uptime</strong><br />{kpis["before"]["uptime_monthly_percent"]}%</div>
          <div><strong>After uptime</strong><br />{kpis["after"]["uptime_monthly_percent"]}%</div>
          <div>
            <strong>Before provisioning P50</strong><br />
            {kpis["before"]["provisioning_time_minutes_p50"]} min
          </div>
          <div>
            <strong>After provisioning P50</strong><br />
            {kpis["after"]["provisioning_time_minutes_p50"]} min
          </div>
        </div>
      </div>
      <div class="card">
        <h2>Uptime trend</h2>
        <img src="{uptime_uri}" alt="Uptime trend" />
      </div>
      <div class="card">
        <h2>Provisioning time</h2>
        <img src="{prov_uri}" alt="Provisioning time" />
      </div>
    </div>
  </body>
</html>
"""
    path.write_text(html, encoding="utf-8")


def render_target_state_md() -> str:
    return (
        "# Target-State Platform Design\n\n"
        "## Objectives\n"
        "- Improve reliability to 99.9% monthly uptime via standardized HA patterns "
        "and operational controls.\n"
        "- Reduce provisioning cycle time by ~40% via automation-first workflows "
        "and reduction of manual touchpoints.\n\n"
        "## Reference architecture (conceptual)\n"
        "- OpenStack provides VM + network primitives with hardened control-plane patterns.\n"
        "- Kubernetes provides standardized application runtime with consistent "
        "namespaces/RBAC/policies.\n"
        "- Terraform models provisioning units and produces a change plan "
        "(mocked locally for this lab).\n"
        "- Ansible enforces configuration conventions and renders example artifacts "
        "(mocked locally when needed).\n\n"
        "## Standardization highlights\n"
        "- Naming conventions across tenants/projects/namespaces.\n"
        "- Upgrade strategy aligned to blue/green patterns where feasible.\n"
        "- SLO/SLI + runbooks as first-class operational artifacts.\n"
    )


def render_architecture_mermaid() -> str:
    return (
        "flowchart TB\n"
        "  subgraph Legacy[Legacy OpenStack Environment]\n"
        "    CP[Control Plane]\\nHA gaps + upgrade risk\n"
        "    NW[Network]\\nchange failure + low visibility\n"
        "    ST[Storage]\\nbackup variability\n"
        "    WF[Provisioning Workflow]\\nmanual touchpoints\n"
        "  end\n"
        "  subgraph Modern[Modernized Target State]\n"
        "    OCP[OpenStack Hardened]\\nHA + clustered services\n"
        "    K8S[Kubernetes Standard Baseline]\\nRBAC + policies + cadence\n"
        "    AUT[Automation-First]\\nTerraform plan + Ansible enforcement\n"
        "    OPS[Operations]\\nSLOs + runbooks + change gates\n"
        "  end\n"
        "  Legacy -->|assessment| AUT\n"
        "  AUT --> Modern\n"
    )

from __future__ import annotations

from okml.config import Settings
from okml.domain.kpis import generate_kpis
from okml.domain.models import AssessmentReport
from okml.reporting.writers import (
    plot_provisioning_time_png,
    plot_uptime_trend_png,
    render_dashboard_html,
    render_kpis_md,
    write_json,
    write_text,
)
from okml.utils.fs import ensure_dir
from okml.utils.logging import get_logger


class KPIService:
    def __init__(self, *, settings: Settings, run_id: str) -> None:
        self._settings = settings
        self._run_id = run_id
        self._log = get_logger(__name__)

    def run(self) -> dict[str, dict[str, float]]:
        assessment_path = self._settings.artifacts_dir / "assessment" / "assessment_report.json"
        if not assessment_path.exists():
            raise FileNotFoundError(
                f"Missing assessment report JSON at {assessment_path}. "
                "Run: okml assess (or okml demo)."
            )

        report = AssessmentReport.model_validate_json(assessment_path.read_text(encoding="utf-8"))
        kpis = generate_kpis(
            scores=report.scores, recommendations=report.recommendations, seed=self._settings.seed
        )

        out_dir = ensure_dir(self._settings.artifacts_dir / "kpis")
        write_json(out_dir / "kpis.json", kpis)
        write_text(out_dir / "kpis.md", render_kpis_md(kpis))

        uptime_png = out_dir / "uptime_trend.png"
        prov_png = out_dir / "provisioning_time.png"
        plot_uptime_trend_png(
            uptime_png,
            before_uptime=kpis["before"]["uptime_monthly_percent"],
            after_uptime=kpis["after"]["uptime_monthly_percent"],
        )
        plot_provisioning_time_png(
            prov_png,
            before_p50=kpis["before"]["provisioning_time_minutes_p50"],
            after_p50=kpis["after"]["provisioning_time_minutes_p50"],
        )
        render_dashboard_html(
            path=out_dir / "dashboard.html",
            kpis=kpis,
            uptime_png=uptime_png,
            provisioning_png=prov_png,
        )

        self._log.info("kpis_complete", extra={"run_id": self._run_id, "out_dir": str(out_dir)})
        return kpis

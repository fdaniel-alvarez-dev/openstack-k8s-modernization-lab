from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer

from okml.config import load_settings
from okml.services.assessment_service import AssessmentService
from okml.services.automation_service import AutomationService
from okml.services.design_service import DesignService
from okml.services.executive_service import ExecutiveService
from okml.services.kpi_service import KPIService
from okml.utils.logging import configure_logging, get_logger
from okml.utils.run_id import new_run_id

app = typer.Typer(no_args_is_help=True, add_completion=False)


ArtifactsDirOpt = Annotated[
    Path | None,
    typer.Option(
        "--artifacts-dir",
        help="Where to write artifacts (default: ./artifacts).",
        dir_okay=True,
        file_okay=False,
    ),
]
SeedOpt = Annotated[
    int | None, typer.Option("--seed", help="Deterministic seed for KPI simulation.")
]
LogFormatOpt = Annotated[
    str | None, typer.Option("--log-format", help="Log format: pretty|json (default: pretty).")
]


@app.command()
def assess(
    input_path: Annotated[
        Path, typer.Option("--input", exists=True, dir_okay=False, help="Legacy env YAML/JSON.")
    ],
    artifacts_dir: ArtifactsDirOpt = None,
    seed: SeedOpt = None,
    log_format: LogFormatOpt = None,
) -> None:
    settings = load_settings(artifacts_dir=artifacts_dir, log_format=log_format, seed=seed)
    run_id = new_run_id()
    configure_logging(settings.log_format, run_id=run_id)
    AssessmentService(settings=settings, run_id=run_id).run(input_path=input_path)


@app.command()
def design(
    artifacts_dir: ArtifactsDirOpt = None,
    seed: SeedOpt = None,
    log_format: LogFormatOpt = None,
) -> None:
    settings = load_settings(artifacts_dir=artifacts_dir, log_format=log_format, seed=seed)
    run_id = new_run_id()
    configure_logging(settings.log_format, run_id=run_id)
    DesignService(settings=settings, run_id=run_id).run()


@app.command()
def automate(
    artifacts_dir: ArtifactsDirOpt = None,
    seed: SeedOpt = None,
    log_format: LogFormatOpt = None,
) -> None:
    settings = load_settings(artifacts_dir=artifacts_dir, log_format=log_format, seed=seed)
    run_id = new_run_id()
    configure_logging(settings.log_format, run_id=run_id)
    AutomationService(settings=settings, run_id=run_id).run()


@app.command()
def kpis(
    artifacts_dir: ArtifactsDirOpt = None,
    seed: SeedOpt = None,
    log_format: LogFormatOpt = None,
) -> None:
    settings = load_settings(artifacts_dir=artifacts_dir, log_format=log_format, seed=seed)
    run_id = new_run_id()
    configure_logging(settings.log_format, run_id=run_id)
    KPIService(settings=settings, run_id=run_id).run()


@app.command("executive-summary")
def executive_summary(
    artifacts_dir: ArtifactsDirOpt = None,
    seed: SeedOpt = None,
    log_format: LogFormatOpt = None,
) -> None:
    settings = load_settings(artifacts_dir=artifacts_dir, log_format=log_format, seed=seed)
    run_id = new_run_id()
    configure_logging(settings.log_format, run_id=run_id)
    ExecutiveService(settings=settings, run_id=run_id).run()


@app.command()
def demo(
    artifacts_dir: ArtifactsDirOpt = None,
    seed: SeedOpt = None,
    log_format: LogFormatOpt = None,
) -> None:
    settings = load_settings(artifacts_dir=artifacts_dir, log_format=log_format, seed=seed)
    run_id = new_run_id()
    configure_logging(settings.log_format, run_id=run_id)
    log = get_logger(__name__)

    input_path = Path("sample_data/legacy_env.yaml")
    AssessmentService(settings=settings, run_id=run_id).run(input_path=input_path)
    DesignService(settings=settings, run_id=run_id).run()
    AutomationService(settings=settings, run_id=run_id).run()
    KPIService(settings=settings, run_id=run_id).run()
    ExecutiveService(settings=settings, run_id=run_id).run()

    meta_path = settings.artifacts_dir / "run_metadata.json"
    meta = {"run_id": run_id, "artifacts_dir": str(settings.artifacts_dir)}
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    log.info(
        "demo_complete", extra={"artifacts_dir": str(settings.artifacts_dir), "run_id": run_id}
    )
    typer.echo(f"Artifacts written to: {settings.artifacts_dir}")

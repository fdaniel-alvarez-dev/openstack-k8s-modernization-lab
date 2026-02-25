from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="OKML_", env_file=None)

    artifacts_dir: Path = Path("artifacts")
    log_format: str = "pretty"  # "pretty" | "json"
    seed: int = 2026


def load_settings(
    artifacts_dir: Path | None = None,
    log_format: str | None = None,
    seed: int | None = None,
) -> Settings:
    settings = Settings()
    if artifacts_dir is not None:
        settings.artifacts_dir = artifacts_dir
    if log_format is not None:
        settings.log_format = log_format
    if seed is not None:
        settings.seed = seed
    return settings

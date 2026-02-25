from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CmdResult:
    cmd: list[str]
    returncode: int
    stdout: str
    stderr: str


def run_cmd(
    cmd: list[str],
    *,
    cwd: Path | None = None,
    timeout_s: int = 300,
    check: bool = False,
) -> CmdResult:
    proc = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        timeout=timeout_s,
    )
    result = CmdResult(cmd=cmd, returncode=proc.returncode, stdout=proc.stdout, stderr=proc.stderr)
    if check and result.returncode != 0:
        joined = " ".join(cmd)
        raise RuntimeError(
            f"Command failed rc={result.returncode}: {joined}\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )
    return result

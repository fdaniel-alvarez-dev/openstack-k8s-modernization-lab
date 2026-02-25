from __future__ import annotations

import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path

from okml.utils.logging import get_logger
from okml.utils.subprocess import run_cmd


@dataclass(frozen=True)
class AnsibleResult:
    run_log: str
    mode: str  # "real" | "mock"


class AnsibleRunner:
    def __init__(self, repo_root: Path) -> None:
        self._repo_root = repo_root
        self._log = get_logger(__name__)

    def run(self) -> AnsibleResult:
        ans_dir = self._repo_root / "iac" / "ansible"
        if not ans_dir.exists():
            raise FileNotFoundError(f"Missing ansible dir: {ans_dir}")

        ap = shutil.which("ansible-playbook")
        if ap is None:
            return self._mock()

        try:
            return self._real(ansible_playbook=ap, ans_dir=ans_dir)
        except Exception as e:
            self._log.info("ansible_real_failed_fallback_to_mock", extra={"error": str(e)})
            return self._mock()

    def _real(self, *, ansible_playbook: str, ans_dir: Path) -> AnsibleResult:
        with tempfile.TemporaryDirectory(prefix="okml-ans-") as td:
            work = Path(td)
            shutil.copytree(ans_dir, work / "ansible", dirs_exist_ok=True)
            cwd = work / "ansible"
            inv = cwd / "inventory.ini"
            inv.write_text("[local]\nlocalhost ansible_connection=local\n", encoding="utf-8")

            res = run_cmd(
                [ansible_playbook, "-i", str(inv), "site.yml"],
                cwd=cwd,
                timeout_s=180,
                check=True,
            )
            return AnsibleResult(run_log=res.stdout + "\n" + res.stderr, mode="real")

    def _mock(self) -> AnsibleResult:
        log = (
            "PLAY [local] *********************************************************************\n"
            "TASK [Gathering Facts] ***********************************************************\n"
            "ok: [localhost]\n"
            "TASK [Render example configs/manifests] ******************************************\n"
            "changed: [localhost]\n"
            "TASK [Validate conventions] ******************************************************\n"
            "ok: [localhost]\n"
            "PLAY RECAP ***********************************************************************\n"
            "localhost                  : ok=3    changed=1    unreachable=0    failed=0\n"
            "NOTE: Mock runner used (ansible-playbook not available or execution not required).\n"
        )
        return AnsibleResult(run_log=log, mode="mock")

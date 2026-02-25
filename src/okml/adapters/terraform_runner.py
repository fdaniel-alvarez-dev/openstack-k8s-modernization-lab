from __future__ import annotations

import json
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path

from okml.utils.logging import get_logger
from okml.utils.subprocess import run_cmd


@dataclass(frozen=True)
class TerraformResult:
    plan_text: str
    outputs: dict[str, object]
    mode: str  # "real" | "mock"


class TerraformRunner:
    def __init__(self, repo_root: Path) -> None:
        self._repo_root = repo_root
        self._log = get_logger(__name__)

    def run(self) -> TerraformResult:
        tf_dir = self._repo_root / "iac" / "terraform"
        if not tf_dir.exists():
            raise FileNotFoundError(f"Missing terraform dir: {tf_dir}")

        tf = shutil.which("terraform")
        if tf is None:
            return self._mock()

        try:
            return self._real(terraform_bin=tf, tf_dir=tf_dir)
        except Exception as e:
            self._log.info("terraform_real_failed_fallback_to_mock", extra={"error": str(e)})
            return self._mock()

    def _real(self, *, terraform_bin: str, tf_dir: Path) -> TerraformResult:
        with tempfile.TemporaryDirectory(prefix="okml-tf-") as td:
            work = Path(td)
            shutil.copytree(tf_dir, work / "tf", dirs_exist_ok=True)
            cwd = work / "tf"

            # WARNING: terraform init may require provider downloads; fallback to mock on failure.
            run_cmd([terraform_bin, "init", "-input=false"], cwd=cwd, timeout_s=180, check=True)
            plan = run_cmd(
                [terraform_bin, "plan", "-input=false", "-no-color"],
                cwd=cwd,
                timeout_s=180,
                check=True,
            )
            apply = run_cmd(
                [terraform_bin, "apply", "-input=false", "-auto-approve", "-no-color"],
                cwd=cwd,
                timeout_s=180,
                check=True,
            )
            out = run_cmd([terraform_bin, "output", "-json"], cwd=cwd, timeout_s=60, check=True)

            outputs = json.loads(out.stdout) if out.stdout.strip() else {}
            plan_text = plan.stdout + "\n" + apply.stdout
            return TerraformResult(plan_text=plan_text, outputs=outputs, mode="real")

    def _mock(self) -> TerraformResult:
        plan_text = (
            "Terraform used the selected providers to generate the following execution plan.\n\n"
            "  # null_resource.provision_units will be created\n"
            '  + resource "null_resource" "provision_units" {\n'
            "      + id = (known after apply)\n"
            "    }\n\n"
            "Plan: 1 to add, 0 to change, 0 to destroy.\n"
        )
        outputs = {
            "provisioning_units": {"value": 12, "type": "number"},
            "standardized_k8s_baseline": {"value": True, "type": "bool"},
            "run_mode": {"value": "mock", "type": "string"},
        }
        return TerraformResult(plan_text=plan_text, outputs=outputs, mode="mock")

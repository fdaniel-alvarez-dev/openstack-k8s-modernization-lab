from __future__ import annotations

import json
from pathlib import Path

from okml.adapters.ansible_runner import AnsibleRunner
from okml.adapters.terraform_runner import TerraformRunner
from okml.config import Settings
from okml.reporting.writers import write_json, write_text
from okml.utils.fs import ensure_dir
from okml.utils.logging import get_logger


class AutomationService:
    def __init__(self, *, settings: Settings, run_id: str) -> None:
        self._settings = settings
        self._run_id = run_id
        self._log = get_logger(__name__)

    def run(self) -> None:
        repo_root = Path.cwd()
        tf = TerraformRunner(repo_root=repo_root).run()
        ans = AnsibleRunner(repo_root=repo_root).run()

        out_dir = ensure_dir(self._settings.artifacts_dir / "automation")
        write_text(out_dir / "terraform_plan.txt", tf.plan_text + f"\nMode: {tf.mode}\n")
        write_json(out_dir / "terraform_outputs.json", tf.outputs)
        write_text(out_dir / "ansible_run.log", ans.run_log + f"\nMode: {ans.mode}\n")

        gen_dir = ensure_dir(out_dir / "generated_configs")
        (gen_dir / "k8s_baseline.yaml").write_text(_k8s_baseline_manifest(), encoding="utf-8")
        (gen_dir / "openstack_controller_standard.md").write_text(
            _openstack_controller_standard(), encoding="utf-8"
        )

        meta = {"terraform_mode": tf.mode, "ansible_mode": ans.mode, "run_id": self._run_id}
        (out_dir / "automation_metadata.json").write_text(
            json.dumps(meta, indent=2), encoding="utf-8"
        )

        self._log.info(
            "automation_complete",
            extra={
                "run_id": self._run_id,
                "out_dir": str(out_dir),
                "terraform_mode": tf.mode,
                "ansible_mode": ans.mode,
            },
        )


def _k8s_baseline_manifest() -> str:
    return (
        "apiVersion: v1\n"
        "kind: Namespace\n"
        "metadata:\n"
        "  name: platform-system\n"
        "  labels:\n"
        '    okml.io/baseline: "true"\n'
        "---\n"
        "apiVersion: rbac.authorization.k8s.io/v1\n"
        "kind: ClusterRole\n"
        "metadata:\n"
        "  name: okml-readonly\n"
        "rules:\n"
        '  - apiGroups: ["*"]\n'
        '    resources: ["*"]\n'
        '    verbs: ["get", "list", "watch"]\n'
    )


def _openstack_controller_standard() -> str:
    return (
        "# OpenStack Controller Standard (Reference)\n\n"
        "- Use clustered DB and message bus.\n"
        "- Enforce maintenance windows with change gates.\n"
        "- Prefer blue/green upgrade paths when feasible.\n"
        "- Capture SLOs and incident learnings into runbooks.\n"
    )

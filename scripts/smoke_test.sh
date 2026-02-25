#!/usr/bin/env bash
set -euo pipefail

if [[ ! -d ".venv" ]]; then
  echo "Missing .venv. Run: make setup" >&2
  exit 2
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ART_DIR="${ROOT}/artifacts/smoke"

rm -rf "${ART_DIR}"
mkdir -p "${ART_DIR}"

"${ROOT}/.venv/bin/python" -m okml demo --artifacts-dir "${ART_DIR}" --seed 2026 --log-format json >/dev/null

req_files=(
  "${ART_DIR}/assessment/assessment_report.md"
  "${ART_DIR}/assessment/assessment_report.json"
  "${ART_DIR}/assessment/risk_register.csv"
  "${ART_DIR}/design/target_state.md"
  "${ART_DIR}/design/architecture.mmd"
  "${ART_DIR}/automation/terraform_plan.txt"
  "${ART_DIR}/automation/terraform_outputs.json"
  "${ART_DIR}/automation/ansible_run.log"
  "${ART_DIR}/kpis/kpis.json"
  "${ART_DIR}/kpis/kpis.md"
  "${ART_DIR}/kpis/uptime_trend.png"
  "${ART_DIR}/kpis/provisioning_time.png"
  "${ART_DIR}/kpis/dashboard.html"
  "${ART_DIR}/executive/executive_summary.md"
)

for f in "${req_files[@]}"; do
  if [[ ! -f "${f}" ]]; then
    echo "Missing expected artifact: ${f}" >&2
    exit 3
  fi
done

"${ROOT}/.venv/bin/python" - <<'PY'
import json
from pathlib import Path

root = Path("artifacts/smoke")
kpis = json.loads((root / "kpis" / "kpis.json").read_text(encoding="utf-8"))
assert kpis["after"]["uptime_monthly_percent"] >= 99.9
assert kpis["after"]["provisioning_time_minutes_p50"] < kpis["before"]["provisioning_time_minutes_p50"]
PY

echo "Smoke test: OK"


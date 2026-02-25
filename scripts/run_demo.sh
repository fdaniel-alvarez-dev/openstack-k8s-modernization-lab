#!/usr/bin/env bash
set -euo pipefail

make setup
make demo

echo ""
echo "Demo complete. Open artifacts/kpis/dashboard.html"


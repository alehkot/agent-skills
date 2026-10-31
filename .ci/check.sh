#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export CI=true NO_COLOR=1
mkdir -p .ci-output
trap 'printf "CI check failed at line %s\n" "$LINENO" >&2' ERR
python3 -B .ci/test_report.py

python3 scripts/validate_public.py
python3 scripts/test_validate_public.py

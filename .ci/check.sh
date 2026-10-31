#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
trap 'printf "CI check failed at line %s\n" "$LINENO" >&2' ERR

python3 scripts/validate_public.py
python3 scripts/test_validate_public.py

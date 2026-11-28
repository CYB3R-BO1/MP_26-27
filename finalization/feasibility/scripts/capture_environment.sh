#!/usr/bin/env bash
set -euo pipefail

ENV_PREFIX="${ENV_PREFIX:-/home/cherr/mp26_27_env_py311}"
WORKSPACE="${WORKSPACE:-/mnt/c/Users/cherr/Documents/PROJECTS/MP_26-27}"
BASE="$WORKSPACE/finalization/feasibility"
OUT="$BASE/environment"

mkdir -p "$OUT"
"$ENV_PREFIX/bin/python" --version > "$OUT/linux-python-version.txt" 2>&1
"$ENV_PREFIX/bin/python" -m pip freeze --all > "$OUT/linux-pip-freeze.txt"
"$ENV_PREFIX/bin/python" -m pip check > "$OUT/linux-pip-check.txt" 2>&1
"$ENV_PREFIX/bin/mafft" --version > "$OUT/mafft-version.txt" 2>&1
"$BASE/environment/maude-3.5.1/maude" --version > "$OUT/maude-version.txt" 2>&1 || true
PATH="$BASE/environment/maude-3.5.1:/usr/bin:/bin" \
  "$BASE/environment/tamarin-1.12.0/tamarin-prover" --version > "$OUT/tamarin-version.txt" 2>&1
"$BASE/environment/stack-3.11.1/stack" --version > "$OUT/stack-version.txt" 2>&1
PATH="$BASE/environment/maude-3.5:/usr/bin:/bin" \
  "$BASE/environment/tamarin-api-bin/tamarin-prover-json" --version > "$OUT/tamarin-api-version.txt" 2>&1

for repo in TamRL Tamarin-ML-API MARISSA; do
  git -C "$BASE/artifacts/$repo" rev-parse HEAD > "$OUT/${repo}-commit.txt"
done

{
  uname -a
  printf '\n'
  cat /etc/os-release
  printf '\nWSL memory and swap:\n'
  free -b
  printf '\nLogical CPUs:\n'
  getconf _NPROCESSORS_ONLN
} > "$OUT/wsl-system.txt"

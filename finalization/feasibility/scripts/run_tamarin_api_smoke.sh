#!/usr/bin/env bash
set -euo pipefail

ENV_PREFIX="${ENV_PREFIX:-/home/cherr/mp26_27_env_py311}"
WORKSPACE="${WORKSPACE:-/mnt/c/Users/cherr/Documents/PROJECTS/MP_26-27}"
BASE="$WORKSPACE/finalization/feasibility"
API="$BASE/environment/tamarin-api-bin/tamarin-prover-json"
MAUDE_DIR="$BASE/environment/maude-3.5"
SCRIPTS="$BASE/artifacts/Tamarin-ML-API/scripts"
RUNNER="$BASE/scripts/measure_command.py"
RUN_DIR="${RUN_DIR:-$BASE/results/proof-budget/api_smoke_retry}"
PORT=3001

export PATH="$BASE/environment/tamarin-api-bin:$MAUDE_DIR:$ENV_PREFIX/bin:/usr/bin:/bin"

if [ -e "$RUN_DIR" ]; then
  echo "refusing to overwrite: $RUN_DIR" >&2
  exit 3
fi

"$ENV_PREFIX/bin/python" "$RUNNER" \
  --output-dir "$RUN_DIR" \
  --timeout-seconds 180 \
  --cwd "$SCRIPTS" \
  -- \
  bash -c '
    set -euo pipefail
    server_pid=""
    cleanup() {
      if [ -n "$server_pid" ]; then
        kill "$server_pid" 2>/dev/null || true
        wait "$server_pid" 2>/dev/null || true
      fi
    }
    trap cleanup EXIT
    tamarin-prover-json interactive --port=3001 Tutorial.spthy &
    server_pid=$!
    sleep 5
    kill -0 "$server_pid"
    python examples.py
  '

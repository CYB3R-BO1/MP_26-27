#!/usr/bin/env bash
set -u

ENV_PREFIX="${ENV_PREFIX:-/home/cherr/mp26_27_env_py311}"
WORKSPACE="${WORKSPACE:-/mnt/c/Users/cherr/Documents/PROJECTS/MP_26-27}"
BASE="$WORKSPACE/finalization/feasibility"
TAMARIN="$BASE/environment/tamarin-1.12.0/tamarin-prover"
MAUDE_DIR="$BASE/environment/maude-3.5.1"
EVAL="$BASE/artifacts/TamRL/eval/5G_handover_xn"
RUNNER="$BASE/scripts/measure_command.py"
RESULTS="${RESULTS:-$BASE/results/proof-budget}"
TIMEOUT_SECONDS="${TIMEOUT_SECONDS:-20}"
LEMMA="secret_k_gnb_star"

export PATH="$MAUDE_DIR:/usr/bin:/bin"

run_one() {
  heuristic="$1"
  label="$2"
  case "$heuristic" in
    s) model="$EVAL/base_s/5G_handover_xn.spthy" ;;
    c) model="$EVAL/base_c/5G_handover_xn.spthy" ;;
    *) echo "unsupported heuristic: $heuristic" >&2; return 2 ;;
  esac
  run_dir="$RESULTS/timeout_restart_${label}"
  if [ -e "$run_dir" ]; then
    echo "refusing to overwrite: $run_dir" >&2
    return 3
  fi

  "$ENV_PREFIX/bin/python" "$RUNNER" \
    --output-dir "$run_dir" \
    --timeout-seconds "$TIMEOUT_SECONDS" \
    --cwd "$EVAL" \
    -- \
    "$TAMARIN" "$model" "--prove=$LEMMA" +RTS -N2 -M2048m -RTS
}

# Expected exit 124 is evidence that the external timeout was enforced.
run_one s s_first
first_exit=$?
run_one c c_first
second_exit=$?
# Same input, fresh process and fresh output directory: Tamarin CLI has no
# checkpoint argument here, so this is a restart, not a continuation.
run_one s s_restart
restart_exit=$?

printf 's_first_exit=%s\nc_first_exit=%s\ns_restart_exit=%s\n' \
  "$first_exit" "$second_exit" "$restart_exit"

if [ "$first_exit" -eq 124 ] && [ "$second_exit" -eq 124 ] && [ "$restart_exit" -eq 124 ]; then
  exit 0
fi
exit 1

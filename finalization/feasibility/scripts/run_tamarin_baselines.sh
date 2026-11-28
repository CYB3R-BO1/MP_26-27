#!/usr/bin/env bash
set -u

ENV_PREFIX="${ENV_PREFIX:-/home/cherr/mp26_27_env_py311}"
WORKSPACE="${WORKSPACE:-/mnt/c/Users/cherr/Documents/PROJECTS/MP_26-27}"
BASE="$WORKSPACE/finalization/feasibility"
TAMARIN="$BASE/environment/tamarin-1.12.0/tamarin-prover"
MAUDE_DIR="$BASE/environment/maude-3.5.1"
EVAL="$BASE/artifacts/TamRL/eval"
RUNNER="$BASE/scripts/measure_command.py"
RESULTS="${RESULTS:-$BASE/results/proof-budget}"
TIMEOUT_SECONDS="${TIMEOUT_SECONDS:-180}"

export PATH="$MAUDE_DIR:/usr/bin:/bin"

run_one() {
  protocol="$1"
  heuristic="$2"
  lemma="$3"
  case "$protocol:$heuristic" in
    tutorial:s) model="$EVAL/Tutorial/original/Tutorial.spthy" ;;
    tutorial:c) model="$EVAL/Tutorial/base_c/Tutorial.spthy" ;;
    yubikey_hsm:s) model="$EVAL/yubikey_hsm/original/yubikey_hsm.spthy" ;;
    yubikey_hsm:c) model="$EVAL/yubikey_hsm/base_c/yubikey_hsm.spthy" ;;
    *) echo "unsupported protocol/heuristic: $protocol/$heuristic" >&2; return 2 ;;
  esac
  run_dir="$RESULTS/${protocol}_${heuristic}_${lemma}"
  if [ -e "$run_dir" ]; then
    echo "refusing to overwrite: $run_dir" >&2
    return 3
  fi

  "$ENV_PREFIX/bin/python" "$RUNNER" \
    --output-dir "$run_dir" \
    --timeout-seconds "$TIMEOUT_SECONDS" \
    --cwd "$EVAL" \
    -- \
    "$TAMARIN" "$model" "--prove=$lemma" +RTS -N2 -M2048m -RTS
}

failures=0
tutorial_lemmas=(
  Client_session_key_secrecy
  Client_auth
  Client_auth_injective
  Client_session_key_honest_setup
)
yubikey_hsm_lemmas=(
  adv_can_guess_counter
  otp_decode_does_not_help_adv_use_induction
  neither_k_nor_k2_are_ever_leaked_inv
  one_count_foreach_login
)

for heuristic in s c; do
  for lemma in "${tutorial_lemmas[@]}"; do
    run_one tutorial "$heuristic" "$lemma" || failures=$((failures + 1))
  done
  for lemma in "${yubikey_hsm_lemmas[@]}"; do
    run_one yubikey_hsm "$heuristic" "$lemma" || failures=$((failures + 1))
  done
done

echo "baseline_failures=$failures"
exit "$failures"

#!/usr/bin/env bash
set -u

ENV_PREFIX="${ENV_PREFIX:-/home/cherr/mp26_27_env_py311}"
WORKSPACE="${WORKSPACE:-/mnt/c/Users/cherr/Documents/PROJECTS/MP_26-27}"
BASE="$WORKSPACE/finalization/feasibility"
ARTIFACT="$BASE/artifacts/MARISSA"
RUNNER="$BASE/scripts/measure_command.py"
RESULTS="${RESULTS:-$BASE/results/proto-sure}"
TIMEOUT_SECONDS="${TIMEOUT_SECONDS:-300}"

export PATH="$ENV_PREFIX/bin:/usr/bin:/bin"
export LD_LIBRARY_PATH="$ENV_PREFIX/lib"
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-4}"
export OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-4}"
export MKL_NUM_THREADS="${MKL_NUM_THREADS:-4}"

run_one() {
  protocol="$1"
  size="$2"
  repetition="$3"
  input="$ARTIFACT/dataset/${protocol}_${size}.pcap"
  run_dir="$RESULTS/${protocol}_${size}_r${repetition}"
  output_dir="$run_dir/output"

  if [ ! -f "$input" ]; then
    echo "missing input: $input" >&2
    return 2
  fi
  if [ -e "$run_dir" ]; then
    echo "refusing to overwrite: $run_dir" >&2
    return 3
  fi

  "$ENV_PREFIX/bin/python" "$RUNNER" \
    --output-dir "$run_dir" \
    --timeout-seconds "$TIMEOUT_SECONDS" \
    --cwd "$ARTIFACT" \
    -- \
    "$ENV_PREFIX/bin/marissa" \
      --input "$input" \
      --output "$output_dir" \
      --remove-headers \
      --distance-algorithm ssdeep \
      --cluster-algorithm optics \
      --align-algorithm mafft
}

failures=0
for protocol in dns modbus; do
  for size in 100 500 1000; do
    run_one "$protocol" "$size" 1 || failures=$((failures + 1))
  done
done

# Repeated small runs expose fixed startup cost and run-to-run variability.
run_one dns 100 2 || failures=$((failures + 1))
run_one dns 100 3 || failures=$((failures + 1))

echo "matrix_failures=$failures"
exit "$failures"

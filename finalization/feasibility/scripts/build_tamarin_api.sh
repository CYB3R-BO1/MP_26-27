#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${WORKSPACE:-/mnt/c/Users/cherr/Documents/PROJECTS/MP_26-27}"
BASE="$WORKSPACE/finalization/feasibility"
SOURCE="$BASE/artifacts/Tamarin-ML-API"
STACK_BIN="${STACK_BIN:-$BASE/environment/stack-3.11.1/stack}"
BUILD_ROOT="${BUILD_ROOT:-/home/cherr/mp26_27_tamarin_api_build_reproduction}"
OUTPUT_BIN="${OUTPUT_BIN:-$BASE/environment/tamarin-api-bin-reproduction}"
SNAPSHOT="${SNAPSHOT:-/home/cherr/lts-22.39.yaml}"

if [ -e "$BUILD_ROOT" ] || [ -e "$OUTPUT_BIN" ]; then
  echo "refusing to overwrite BUILD_ROOT or OUTPUT_BIN" >&2
  exit 3
fi

curl --fail --location \
  'https://raw.githubusercontent.com/commercialhaskell/stackage-snapshots/master/lts/22/39.yaml' \
  --output "$SNAPSHOT"
cp -a "$SOURCE" "$BUILD_ROOT"
sed -i "s#^resolver: lts-22.39#resolver: $SNAPSHOT#" "$BUILD_ROOT/stack.yaml"
mkdir -p "$OUTPUT_BIN"

cd "$BUILD_ROOT"
"$STACK_BIN" --jobs 2 install --local-bin-path "$OUTPUT_BIN"

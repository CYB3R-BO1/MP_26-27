# Reproduction guide

This directory is self-contained for the recorded experiments on the inspected machine. Scripts refuse to overwrite existing run directories. Use a new `RESULTS` or `RUN_DIR` path for repetitions.

## Layout

| Path | Purpose |
| --- | --- |
| `proof-budget/` | project-specific report |
| `proto-sure/` | project-specific report |
| `scripts/` | runners, monitors, extractors, and summarizers |
| `results/` | immutable per-run logs plus structured summaries |
| `environment/` | tool binaries, version captures, package manifest, hardware inventory |
| `artifacts/` | pinned public source checkouts and checksum-verified published results |

The public source revisions are:

```text
TamRL             f82e5914e23e3f1d3623d4aeaa0fb503f3ce410b
Tamarin-ML-API    b3a20fc880404ef110a5ea083730843a2e0f6ba2
MARISSA           adcd5bc3b94b6aff817da9dc613caa3a62a147d6
```

Version files and the complete Linux package freeze are in [`environment/`](environment/). The structured index of all 33 measured local runs is [`experiment_status.json`](results/experiment_status.json): 28 command successes, three expected timeouts, and two preserved diagnosed failures.

## Environment used

Two fresh environments were created:

```powershell
conda create --prefix finalization/feasibility/.conda/feasibility-py311 python=3.11.18 pip=26.2.2 -y
```

```bash
/home/cherr/mp26_27_miniforge/bin/conda create \
  --prefix /home/cherr/mp26_27_env_py311 \
  --channel conda-forge python=3.11.18 mafft=7.526 pip -y
```

The Linux environment then received the versions in [`linux-pip-freeze.txt`](environment/linux-pip-freeze.txt). MARISSA was installed editable at its pinned local commit. ssdeep/libfuzzy 2.14.1 was built into the environment prefix before installing `ssdeep==3.4`; the Poetry-lock-compatible Python pins were used, notably Click 8.1.7 and Typer 0.9.4. `pip check` is captured in [`linux-pip-check.txt`](environment/linux-pip-check.txt).

Standard Tamarin 1.12.0 and Maude 3.5.1 are under `environment/`. The modified API is Tamarin 1.11.0 and requires Maude 3.5, also retained. Rebuild it with [`build_tamarin_api.sh`](scripts/build_tamarin_api.sh); the script uses Stack 3.11.1, two build jobs, an ext4 build directory, and refuses to overwrite an existing build/output.

## Common variables

The shell runners default to this machine's paths. On another WSL installation set:

```bash
export WORKSPACE=/mnt/c/path/to/MP_26-27
export ENV_PREFIX=/path/to/fresh/linux/python/environment
```

All commands below are executed inside Ubuntu WSL from the repository root unless marked PowerShell.

## PROOF-BUDGET commands

Run the 16 standard baseline jobs into a new directory:

```bash
RESULTS="$WORKSPACE/finalization/feasibility/results/reproduction-proof-baselines" \
TIMEOUT_SECONDS=180 \
bash "$WORKSPACE/finalization/feasibility/scripts/run_tamarin_baselines.sh"
```

Summarize them:

```bash
python "$WORKSPACE/finalization/feasibility/scripts/summarize_tamarin.py" \
  "$WORKSPACE/finalization/feasibility/results/reproduction-proof-baselines" \
  "$WORKSPACE/finalization/feasibility/results/reproduction-proof-baselines.csv"
```

Run the deliberate timeout/restart check:

```bash
RESULTS="$WORKSPACE/finalization/feasibility/results/reproduction-timeout-restart" \
TIMEOUT_SECONDS=20 \
bash "$WORKSPACE/finalization/feasibility/scripts/run_tamarin_timeout_restart.sh"
```

Run the JSON-API BFS smoke test:

```bash
RUN_DIR="$WORKSPACE/finalization/feasibility/results/reproduction-api-smoke" \
bash "$WORKSPACE/finalization/feasibility/scripts/run_tamarin_api_smoke.sh"
```

Extract conservative reuse-dependency candidates:

```powershell
finalization\feasibility\.conda\feasibility-py311\python.exe `
  finalization\feasibility\scripts\extract_lemma_dependencies.py `
  --output finalization\feasibility\results\reproduction-dependencies.json `
  finalization\feasibility\artifacts\TamRL\eval\Tutorial\original\Tutorial.spthy `
  finalization\feasibility\artifacts\TamRL\eval\yubikey_hsm\original\yubikey_hsm.spthy `
  finalization\feasibility\artifacts\TamRL\eval\5G_handover_xn\base_s\5G_handover_xn.spthy
```

The published TamRL archive analysis is reproduced with:

```powershell
finalization\feasibility\.conda\feasibility-py311\python.exe `
  finalization\feasibility\scripts\analyze_tamrl_published.py `
  --results-root finalization\feasibility\artifacts\TamRL-precomputed\extracted\results `
  --archive finalization\feasibility\artifacts\TamRL-precomputed\results.zip `
  --output finalization\feasibility\results\proof-budget\published_artifact_summary.reproduced.json
```

This analysis labels the data as published, not local reproduction.

## PROTO-SURE commands

Run the eight-job baseline matrix into a new directory:

```bash
RESULTS="$WORKSPACE/finalization/feasibility/results/reproduction-proto-matrix" \
TIMEOUT_SECONDS=300 OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4 \
bash "$WORKSPACE/finalization/feasibility/scripts/run_marissa_matrix.sh"
```

Summarize it:

```bash
python "$WORKSPACE/finalization/feasibility/scripts/summarize_marissa.py" \
  "$WORKSPACE/finalization/feasibility/results/reproduction-proto-matrix" \
  "$WORKSPACE/finalization/feasibility/results/reproduction-proto-matrix.csv"
```

Compute capture overlap, independent constraints, and fixed-header metrics:

```bash
python "$WORKSPACE/finalization/feasibility/scripts/analyze_captures_and_structures.py" \
  --artifact "$WORKSPACE/finalization/feasibility/artifacts/MARISSA" \
  --results "$WORKSPACE/finalization/feasibility/results/reproduction-proto-matrix" \
  --output "$WORKSPACE/finalization/feasibility/results/reproduction-capture-structure.json"
```

## Hardware and environment capture

From PowerShell:

```powershell
& finalization\feasibility\scripts\hardware_inventory.ps1
```

From WSL:

```bash
bash "$WORKSPACE/finalization/feasibility/scripts/capture_environment.sh"
```

The latter intentionally refreshes manifest text files under `environment/`; it does not alter source artifacts.

## Measurement semantics

[`measure_command.py`](scripts/measure_command.py) starts the target in a new process group, samples the complete process tree, sends `SIGTERM` at the configured wall-time limit, escalates to `SIGKILL` after ten seconds if necessary, and writes:

- `stdout.log` and `stderr.log`;
- `measurement.json` containing exact command, working directory, timestamps, timeout, exit status, peak RSS/VMS/process count, sampled CPU, and host details;
- the tool's normal output directory, if any.

Peak RSS is the primary memory metric. GHC reserves very large virtual address spaces, making VMS misleading. The first MARISSA matrix was run before cumulative CPU accounting was fixed, so use its wall time and RSS only. The later `cpu_probe_dns_100` run contains valid cumulative CPU data. Very short/spawn-heavy commands can still produce unreliable instantaneous peak CPU samples; average observed CPU is safer.

## Integrity and scope

- Original `paper-discovery/` and `shortlisting/` files were not edited.
- Existing run directories are never overwritten by the runners.
- No full TamRL training was performed.
- No project was selected and no GitHub push was made.
- Dataset licensing/provenance and full schema annotations remain research gates, not silently assumed facts.

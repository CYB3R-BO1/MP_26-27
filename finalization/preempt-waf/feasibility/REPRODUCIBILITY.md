# Reproducibility guide

Run from the repository root in PowerShell unless a command explicitly uses WSL. Raw data are excluded from Git; rerunning retrieval requires network access and acceptance of each dataset license. No command contacts or tests an external web application.

## 1. Python environment

The recorded run used the host Python 3.13.5 environment. For an isolated rerun:

```powershell
python -m venv finalization/preempt-waf/feasibility/environment/.venv
finalization/preempt-waf/feasibility/environment/.venv/Scripts/python -m pip install -r finalization/preempt-waf/feasibility/environment/requirements-feasibility.txt
```

The `.venv` path is Git-excluded. Exact host and container versions are in `environment/SYSTEM_PROFILE.md`.

## 2. Metadata and remote ZIP inspection

Metadata retrieval uses the public Zenodo API and writes the complete response:

```powershell
python finalization/preempt-waf/feasibility/scripts/fetch_zenodo_metadata.py 19483937 --output finalization/preempt-waf/feasibility/results/zenodo_19483937_metadata.json
python finalization/preempt-waf/feasibility/scripts/fetch_zenodo_metadata.py 8263181 --output finalization/preempt-waf/feasibility/results/zenodo_8263181_metadata.json
python finalization/preempt-waf/feasibility/scripts/fetch_zenodo_metadata.py 18861762 --output finalization/preempt-waf/feasibility/results/zenodo_18861762_metadata.json
python finalization/preempt-waf/feasibility/scripts/fetch_zenodo_metadata.py 16978408 --output finalization/preempt-waf/feasibility/results/zenodo_16978408_metadata.json
python finalization/preempt-waf/feasibility/scripts/fetch_zenodo_metadata.py 20001206 --output finalization/preempt-waf/feasibility/results/zenodo_20001206_metadata.json
```

The manifest reader fetches only the ZIP end/central directory using HTTP range requests. Example for the smallest AIT no-PCAP archive:

```powershell
python finalization/preempt-waf/feasibility/scripts/remote_zip_manifest.py "https://zenodo.org/api/records/19483937/files/russellmitchell_no-pcaps.zip/content" --output finalization/preempt-waf/feasibility/results/russellmitchell_no-pcaps_remote_manifest.json
```

Selected extraction fetches only compressed members, verifies ZIP CRC32, rejects unsafe paths, and records a receipt. Example:

```powershell
python finalization/preempt-waf/feasibility/scripts/remote_zip_extract.py finalization/preempt-waf/feasibility/results/russellmitchell_no-pcaps_remote_manifest.json --match "gather/intranet_server/logs/apache2/.*access\.log|labels/.*apache|attacker/traffic\.json" --destination finalization/preempt-waf/feasibility/datasets/ait-lds-v2.1-russellmitchell-selected --receipt finalization/preempt-waf/feasibility/results/ait_selected_extract_receipt.json
```

The exact external URLs, archive checksums, member lists and CRC receipts used in the investigation are retained in `results/*metadata.json`, `results/*manifest.json`, and `results/*receipt*.json`. This avoids downloading the 137 GB compressed AIT collection.

## 3. Dataset profiling

After the selected members are present:

```powershell
python finalization/preempt-waf/feasibility/scripts/profile_datasets.py --datasets finalization/preempt-waf/feasibility/datasets --output finalization/preempt-waf/feasibility/results/dataset_profile.json
python finalization/preempt-waf/feasibility/scripts/profile_jsonl_trace.py finalization/preempt-waf/feasibility/datasets/ait-lds-v2.1-russellmitchell-selected/attacker/traffic.json --output finalization/preempt-waf/feasibility/results/ait_attacker_trace_profile.json
```

The first command took 184.5 seconds locally. Paths can vary if a Zenodo archive changes structure; consult the saved manifest rather than guessing.

## 4. Prediction baselines

The full reported experiment:

```powershell
python finalization/preempt-waf/feasibility/scripts/run_ait_baselines.py --datasets finalization/preempt-waf/feasibility/datasets --output finalization/preempt-waf/feasibility/results/ait_baselines_full.json --prefix 20 --bin-seconds 5 --request-stride 10 --bootstrap-repetitions 200 --seed 20261128
```

Prefix sensitivity at the 60-second horizon:

```powershell
python finalization/preempt-waf/feasibility/scripts/run_ait_baselines.py --datasets finalization/preempt-waf/feasibility/datasets --output finalization/preempt-waf/feasibility/results/ait_prefix5_time60.json --prefix 5 --only-time --bootstrap-repetitions 200 --seed 20261128
python finalization/preempt-waf/feasibility/scripts/run_ait_baselines.py --datasets finalization/preempt-waf/feasibility/datasets --output finalization/preempt-waf/feasibility/results/ait_prefix100_time60.json --prefix 100 --only-time --bootstrap-repetitions 200 --seed 20261128
```

The script is deterministic for the supplied seed except for platform/library floating-point details. It creates campaign splits before fitting transforms/models, uses a distinct validation campaign for thresholds, and records software/runtime/RSS in the JSON. The full run took 1,356.9 seconds and 1,346,936,832 peak RSS bytes.

## 5. Local defense smoke test

Preferred setup with Compose is `environment/local-testbed.compose.yml`; both images are digest-pinned. With this WSL installation, the tested equivalent used explicit container names:

```powershell
wsl -d Ubuntu -- bash -lc "docker network inspect preempt-waf-testbed >/dev/null 2>&1 || docker network create --internal preempt-waf-testbed; docker create --name preempt-juice --network preempt-waf-testbed bkimminich/juice-shop@sha256:adaf6a6ca50f772dff7d2fe56972c659e81a61e0dbbe607c2b39fefd436e6153 >/dev/null; docker create --name preempt-waf --network preempt-waf-testbed -e BACKEND=http://preempt-juice:3000 -e PORT=8080 -e MODSEC_RULE_ENGINE=On -e BLOCKING_PARANOIA=1 -e DETECTION_PARANOIA=1 -e ANOMALY_INBOUND=5 -e ANOMALY_OUTBOUND=4 -e MODSEC_AUDIT_ENGINE=RelevantOnly owasp/modsecurity-crs@sha256:cd1aa84167b5ba42539001c6fedf174484499ad1c37161df9eed1453e64d65e2 >/dev/null"
wsl -d Ubuntu -- bash -lc "bash /mnt/c/Users/cherr/Documents/PROJECTS/MP_26-27/finalization/preempt-waf/feasibility/scripts/test_local_defense.sh"
```

If the containers already exist, omit the `docker create` line. The script starts and stops them, sends only a benign request plus one harmless SQLi-shaped request to a missing path, and never targets an external host. Its measurements are transcribed in `results/defense_smoke_test.json`; raw WAF logs are intentionally excluded.

## 6. Integrity checks

```powershell
python -m compileall -q finalization/preempt-waf/feasibility/scripts
Get-FileHash -Algorithm SHA256 finalization/preempt-waf/feasibility/results/*.json
git status --short
```

Do not commit `datasets/`, `logs/`, environments, packet captures, credentials, or secrets. This investigation made no commit or push.

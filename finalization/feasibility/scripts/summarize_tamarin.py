#!/usr/bin/env python3
"""Summarize preserved Tamarin measurements and proof status lines."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


STATUS_LINE = re.compile(
    r"^\s*(?P<lemma>[A-Za-z0-9_]+)\s+\([^)]*\):\s+"
    r"(?P<status>verified|falsified)\s+\((?P<steps>\d+) steps\)\s*$"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("results_dir", type=Path)
    parser.add_argument("output_csv", type=Path)
    args = parser.parse_args()
    rows = []
    for measurement_path in sorted(args.results_dir.glob("*/measurement.json")):
        run_dir = measurement_path.parent
        measurement = json.loads(measurement_path.read_text(encoding="utf-8"))
        command = measurement["command"]
        prove_arg = next((item for item in command if item.startswith("--prove=")), "")
        lemma = prove_arg.partition("=")[2]
        model = next((item for item in command if item.endswith(".spthy")), "")
        protocol = "yubikey_hsm" if "yubikey_hsm" in model.lower() else "tutorial"
        heuristic = "c" if "/base_c/" in model.replace("\\", "/") else "s"
        proof_status = ""
        proof_steps = ""
        stdout = (run_dir / "stdout.log").read_text(encoding="utf-8", errors="replace")
        for line in stdout.splitlines():
            match = STATUS_LINE.match(line)
            if match and match.group("lemma") == lemma:
                proof_status = match.group("status")
                proof_steps = match.group("steps")
        rows.append(
            {
                "run": run_dir.name,
                "protocol": protocol,
                "heuristic": heuristic,
                "lemma": lemma,
                "run_status": measurement["status"],
                "exit_code": measurement["exit_code"],
                "proof_status": proof_status,
                "proof_steps": proof_steps,
                "elapsed_seconds": f'{measurement["elapsed_seconds"]:.6f}',
                "peak_rss_mib": f'{measurement["peak_rss_bytes"] / 2**20:.3f}',
                "peak_sampled_cpu_percent": f'{measurement["peak_sampled_cpu_percent"]:.3f}',
                "observed_cpu_seconds": f'{measurement["observed_cpu_seconds"]:.6f}',
                "average_cpu_percent": f'{measurement["average_cpu_percent_from_observed_time"]:.3f}',
                "timeout_seconds": measurement["timeout_seconds"],
                "model": model,
            }
        )

    if not rows:
        raise SystemExit("no measurement.json files found")
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Aggregate preserved MARISSA run measurements and output metadata."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


RUN_NAME = re.compile(r"^(?P<protocol>.+)_(?P<size>\d+)_r(?P<repetition>\d+)$")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("results_dir", type=Path)
    parser.add_argument("output_csv", type=Path)
    args = parser.parse_args()

    rows = []
    for measurement_path in sorted(args.results_dir.glob("*/measurement.json")):
        run_dir = measurement_path.parent
        match = RUN_NAME.match(run_dir.name)
        measurement = json.loads(measurement_path.read_text(encoding="utf-8"))
        metadata_path = run_dir / "output" / "output.meta.json"
        metadata = (
            json.loads(metadata_path.read_text(encoding="utf-8"))
            if metadata_path.exists()
            else {}
        )
        rows.append(
            {
                "run": run_dir.name,
                "protocol": match.group("protocol") if match else "",
                "sample_size_label": match.group("size") if match else "",
                "repetition": match.group("repetition") if match else "",
                "status": measurement["status"],
                "exit_code": measurement["exit_code"],
                "elapsed_seconds": f'{measurement["elapsed_seconds"]:.6f}',
                "peak_rss_mib": f'{measurement["peak_rss_bytes"] / 2**20:.3f}',
                "peak_vms_mib": f'{measurement["peak_vms_bytes"] / 2**20:.3f}',
                "peak_sampled_cpu_percent": f'{measurement["peak_sampled_cpu_percent"]:.3f}',
                "average_cpu_percent": f'{measurement["average_cpu_percent_from_observed_time"]:.3f}',
                "packet_count": metadata.get("packet_count", ""),
                "clusters": metadata.get("clusters", ""),
                "tool_reported_running_time": metadata.get("running_time", ""),
                "common_prefix_hex_chars": len(metadata.get("common_prefix") or ""),
                "distance_algorithm": metadata.get("distance_algorithm", ""),
                "cluster_algorithm": metadata.get("cluster_algorithm", ""),
                "align_algorithm": metadata.get("align_algorithm", ""),
            }
        )

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit("no measurement.json files found")
    with args.output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()

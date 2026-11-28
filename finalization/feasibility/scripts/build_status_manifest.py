#!/usr/bin/env python3
"""Index every measured run without modifying the preserved run directories."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("results", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    runs = []
    for path in sorted(args.results.rglob("measurement.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        runs.append(
            {
                "run": str(path.parent.relative_to(args.results)),
                "status": record["status"],
                "timed_out": record["timed_out"],
                "exit_code": record["exit_code"],
                "elapsed_seconds": record["elapsed_seconds"],
                "peak_rss_bytes": record["peak_rss_bytes"],
                "observed_cpu_seconds": record.get("observed_cpu_seconds"),
                "average_cpu_percent": record.get(
                    "average_cpu_percent_from_observed_time"
                ),
                "command": record["command"],
                "measurement": str(path.relative_to(args.results)),
            }
        )
    counts = Counter(item["status"] for item in runs)
    output = {
        "schema_version": 1,
        "measured_run_count": len(runs),
        "status_counts": dict(sorted(counts.items())),
        "runs": runs,
        "notes": [
            "Timeout is an expected experimental outcome for timeout_restart runs.",
            "The initial MARISSA matrix predates the cumulative CPU accounting fix; use its runtime and RSS, not average CPU.",
            "Published TamRL results are summarized separately and are not counted as local measured runs.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output["status_counts"], indent=2))


if __name__ == "__main__":
    main()

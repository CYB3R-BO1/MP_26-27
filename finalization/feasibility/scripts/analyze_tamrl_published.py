#!/usr/bin/env python3
"""Summarize the downloaded TamRL results without treating them as local runs."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def summarize_rl(group: Path) -> dict:
    raw = json.loads((group / "raw.json").read_text(encoding="utf-8"))
    runs = []
    all_first_times = []
    for run_id, run in raw.items():
        lemmas = []
        protocols = []
        for protocol, values in run.items():
            if protocol == "_meta":
                continue
            protocols.append(protocol)
            lemmas.extend(values.values())
        completed = [x for x in lemmas if int(x.get("completes", 0)) > 0]
        times = [float(x["first_completion_time"]) for x in completed]
        all_first_times.extend(times)
        config = run.get("_meta", {}).get("config", {})
        runs.append(
            {
                "run_id": run_id,
                "protocols": protocols,
                "lemma_entries": len(lemmas),
                "completed_lemma_entries": len(completed),
                "max_first_completion_seconds": max(times) if times else None,
                "num_envs": config.get("env/num_envs"),
                "cache_max_memory_mb": config.get("env/cache_max_memory_mb"),
                "search_budget": config.get("search/budget"),
            }
        )
    return {
        "run_count": len(runs),
        "lemma_entries": sum(x["lemma_entries"] for x in runs),
        "completed_lemma_entries": sum(x["completed_lemma_entries"] for x in runs),
        "max_reported_first_completion_seconds": max(all_first_times) if all_first_times else None,
        "num_envs_values": sorted({x["num_envs"] for x in runs if x["num_envs"] is not None}),
        "cache_max_memory_mb_values": sorted(
            {x["cache_max_memory_mb"] for x in runs if x["cache_max_memory_mb"] is not None}
        ),
        "search_budget_values": sorted(
            {x["search_budget"] for x in runs if x["search_budget"] is not None}
        ),
        "runs": runs,
    }


def summarize_tamarin(root: Path) -> dict:
    outcomes: Counter[str] = Counter()
    seconds = 0.0
    rows = 0
    files = list(root.rglob("*.csv"))
    protocols = set()
    variants = Counter()
    for path in files:
        relative = path.relative_to(root)
        if len(relative.parts) >= 2:
            protocols.add(relative.parts[0])
            variants[relative.parts[1]] += 1
        with path.open(newline="", encoding="utf-8-sig") as handle:
            for row in csv.reader(handle):
                if len(row) < 3:
                    continue
                outcome = row[1].strip()
                try:
                    elapsed = float(row[2])
                except ValueError:
                    continue
                rows += 1
                outcomes[outcome] += 1
                seconds += elapsed
    return {
        "protocol_count": len(protocols),
        "protocols": sorted(protocols),
        "csv_count": len(files),
        "csv_count_by_variant": dict(sorted(variants.items())),
        "lemma_rows": rows,
        "outcomes": dict(sorted(outcomes.items())),
        "sum_recorded_lemma_seconds": seconds,
        "sum_recorded_lemma_hours": seconds / 3600,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-root", required=True, type=Path)
    parser.add_argument("--archive", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    files = [p for p in args.results_root.rglob("*") if p.is_file()]
    proof_files = [p for p in files if "proof_trees" in p.parts]
    summary = {
        "provenance": "PUBLISHED_TAMRL_ARTIFACT_NOT_LOCALLY_REPRODUCED",
        "archive_bytes": args.archive.stat().st_size,
        "extracted_file_count": len(files),
        "extracted_bytes": sum(p.stat().st_size for p in files),
        "proof_tree_file_count": len(proof_files),
        "proof_tree_bytes": sum(p.stat().st_size for p in proof_files),
        "best": summarize_rl(args.results_root / "best"),
        "others": summarize_rl(args.results_root / "others"),
        "tamarin": summarize_tamarin(args.results_root / "tamarin"),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

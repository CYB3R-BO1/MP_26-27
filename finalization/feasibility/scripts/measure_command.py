#!/usr/bin/env python3
"""Run one bounded command and record process-tree resource usage.

This wrapper deliberately keeps stdout, stderr, and structured measurements in a
new per-run directory.  It refuses to overwrite an existing run.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import psutil


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--timeout-seconds", required=True, type=float)
    parser.add_argument("--poll-seconds", type=float, default=0.10)
    parser.add_argument("--cwd", type=Path)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.command and args.command[0] == "--":
        args.command = args.command[1:]
    if not args.command:
        parser.error("a command is required after --")
    return args


def process_tree(root: psutil.Process) -> list[psutil.Process]:
    try:
        return [root, *root.children(recursive=True)]
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return []


def main() -> int:
    args = parse_args()
    if args.output_dir.exists():
        raise SystemExit(f"refusing to overwrite existing run: {args.output_dir}")
    args.output_dir.mkdir(parents=True)

    stdout_path = args.output_dir / "stdout.log"
    stderr_path = args.output_dir / "stderr.log"
    result_path = args.output_dir / "measurement.json"
    cwd = args.cwd.resolve() if args.cwd else Path.cwd().resolve()
    started_at = datetime.now(timezone.utc)
    started = time.perf_counter()
    timed_out = False
    peak_rss = 0
    peak_vms = 0
    peak_processes = 0
    peak_sampled_cpu_percent = 0.0
    samples = 0
    observed: dict[tuple[int, float], psutil.Process] = {}
    latest_cpu_seconds: dict[tuple[int, float], float] = {}

    with stdout_path.open("wb") as stdout_file, stderr_path.open("wb") as stderr_file:
        proc = subprocess.Popen(
            args.command,
            cwd=cwd,
            stdout=stdout_file,
            stderr=stderr_file,
            start_new_session=True,
        )
        root = psutil.Process(proc.pid)
        while proc.poll() is None:
            now = time.perf_counter()
            if now - started > args.timeout_seconds:
                timed_out = True
                try:
                    os.killpg(proc.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    try:
                        os.killpg(proc.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                break

            procs = process_tree(root)
            rss = 0
            vms = 0
            cpu = 0.0
            for child in procs:
                try:
                    key = (child.pid, child.create_time())
                    if key not in observed:
                        child.cpu_percent(None)
                        observed[key] = child
                    mem = child.memory_info()
                    cpu_times = child.cpu_times()
                    latest_cpu_seconds[key] = cpu_times.user + cpu_times.system
                    rss += mem.rss
                    vms += mem.vms
                    cpu += child.cpu_percent(None)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            peak_rss = max(peak_rss, rss)
            peak_vms = max(peak_vms, vms)
            peak_processes = max(peak_processes, len(procs))
            peak_sampled_cpu_percent = max(peak_sampled_cpu_percent, cpu)
            samples += 1
            time.sleep(args.poll_seconds)

        exit_code = proc.wait()

    elapsed = time.perf_counter() - started
    for key, child in observed.items():
        try:
            times = child.cpu_times()
            latest_cpu_seconds[key] = times.user + times.system
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    child_cpu_seconds = sum(latest_cpu_seconds.values())

    status = "timeout" if timed_out else ("success" if exit_code == 0 else "failed")
    record = {
        "schema_version": 1,
        "status": status,
        "timed_out": timed_out,
        "exit_code": exit_code,
        "command": args.command,
        "cwd": str(cwd),
        "started_at_utc": started_at.isoformat(),
        "ended_at_utc": datetime.now(timezone.utc).isoformat(),
        "timeout_seconds": args.timeout_seconds,
        "poll_seconds": args.poll_seconds,
        "elapsed_seconds": elapsed,
        "peak_rss_bytes": peak_rss,
        "peak_vms_bytes": peak_vms,
        "peak_process_count": peak_processes,
        "peak_sampled_cpu_percent": peak_sampled_cpu_percent,
        "observed_cpu_seconds": child_cpu_seconds,
        "average_cpu_percent_from_observed_time": (
            100.0 * child_cpu_seconds / elapsed if elapsed else 0.0
        ),
        "samples": samples,
        "host": {
            "platform": platform.platform(),
            "python": sys.version,
            "logical_cpus": psutil.cpu_count(logical=True),
            "physical_cpus": psutil.cpu_count(logical=False),
            "total_ram_bytes": psutil.virtual_memory().total,
        },
    }
    result_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))
    return 124 if timed_out else exit_code


if __name__ == "__main__":
    raise SystemExit(main())

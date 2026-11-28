#!/usr/bin/env python3
"""Profile the locally inspected PREEMPT-WAF dataset subsets.

The script is descriptive only: it does not infer missing timestamps, sessions,
or outcomes. Raw IP addresses and payloads are not copied into the result.
"""

from __future__ import annotations

import argparse
import collections
import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path


APACHE = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[(?P<time>[^]]+)\] "(?P<method>\S+) (?P<target>.*?) '
    r'HTTP/(?P<http>[^\"]+)" (?P<status>\d{3}) (?P<bytes>\S+) "(?P<referer>[^"]*)" "(?P<ua>[^"]*)"'
)


def parse_apache(line: str) -> dict[str, object] | None:
    match = APACHE.match(line.rstrip("\n"))
    if not match:
        return None
    values = match.groupdict()
    return {
        **values,
        "timestamp": datetime.strptime(values["time"], "%d/%b/%Y:%H:%M:%S %z").timestamp(),
        "status": int(values["status"]),
        "bytes": None if values["bytes"] == "-" else int(values["bytes"]),
    }


def profile_webspotter(root: Path) -> dict[str, object]:
    result: dict[str, object] = {}
    for path in sorted(root.glob("datasets/**/*.jsonl")):
        counts: collections.Counter[int] = collections.Counter()
        methods: collections.Counter[str] = collections.Counter()
        keys: set[str] = set()
        locations = 0
        records = 0
        for line in path.open(encoding="utf-8"):
            row = json.loads(line)
            records += 1
            keys.update(row)
            counts[int(row["label"])] += 1
            methods[str(row.get("method"))] += 1
            locations += row.get("location") is not None
        result[str(path.relative_to(root))] = {
            "records": records,
            "labels": dict(sorted(counts.items())),
            "methods": dict(methods),
            "keys": sorted(keys),
            "location_labeled_records": locations,
            "has_timestamp": "timestamp" in keys,
            "has_session_identifier": bool({"session", "session_id", "cookie"} & keys),
        }
    return result


def read_phase_labels(path: Path) -> dict[str, dict[str, tuple[float, float]]]:
    phases: dict[str, dict[str, tuple[float, float]]] = collections.defaultdict(dict)
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            phases[row["scenario"]][row["attack"]] = (float(row["start"]), float(row["end"]))
    return phases


def profile_ait(root: Path, label_path: Path) -> dict[str, object]:
    phases = read_phase_labels(label_path)
    result: dict[str, object] = {}
    for campaign_dir in sorted(root.glob("ait-lds-v2.1-*-selected")):
        campaign = campaign_dir.name.removeprefix("ait-lds-v2.1-").removesuffix("-selected")
        access_files = sorted(campaign_dir.glob("gather/intranet_server/logs/apache2/*access.log*"))
        total = parsed = 0
        minimum = maximum = None
        ips: set[str] = set()
        uas: set[str] = set()
        methods: collections.Counter[str] = collections.Counter()
        statuses: collections.Counter[int] = collections.Counter()
        phase_counts: collections.Counter[str] = collections.Counter()
        before_first_exploit = 0
        precursor_requests = 0
        exploit_start = phases.get(campaign, {}).get("webshell", (None, None))[0]
        reconnaissance_start = phases.get(campaign, {}).get("network_scans", (None, None))[0]
        for path in access_files:
            with path.open(encoding="utf-8", errors="replace") as handle:
                for line in handle:
                    total += 1
                    event = parse_apache(line)
                    if event is None:
                        continue
                    parsed += 1
                    timestamp = float(event["timestamp"])
                    minimum = timestamp if minimum is None else min(minimum, timestamp)
                    maximum = timestamp if maximum is None else max(maximum, timestamp)
                    ips.add(str(event["ip"]))
                    uas.add(str(event["ua"]))
                    methods[str(event["method"])] += 1
                    statuses[int(event["status"])] += 1
                    if exploit_start is not None and timestamp < exploit_start:
                        before_first_exploit += 1
                    if (
                        reconnaissance_start is not None
                        and exploit_start is not None
                        and reconnaissance_start <= timestamp < exploit_start
                    ):
                        precursor_requests += 1
                    for phase, (start, end) in phases.get(campaign, {}).items():
                        if start <= timestamp < end:
                            phase_counts[phase] += 1
                            break
        label_files = sorted(campaign_dir.glob("labels/intranet_server/logs/apache2/*access.log*"))
        line_labels: collections.Counter[str] = collections.Counter()
        label_rows = 0
        for path in label_files:
            with path.open(encoding="utf-8") as handle:
                for line in handle:
                    row = json.loads(line)
                    label_rows += 1
                    line_labels.update(row.get("labels", []))
        result[campaign] = {
            "access_files": len(access_files),
            "raw_lines": total,
            "parsed_requests": parsed,
            "unparsed_lines": total - parsed,
            "start_utc": datetime.fromtimestamp(minimum, timezone.utc).isoformat() if minimum else None,
            "end_utc": datetime.fromtimestamp(maximum, timezone.utc).isoformat() if maximum else None,
            "unique_ip_values": len(ips),
            "unique_user_agents": len(uas),
            "methods": dict(methods),
            "statuses": {str(k): v for k, v in sorted(statuses.items())},
            "first_exploit_attempt_definition": "AIT-ADS webshell phase start",
            "first_exploit_attempt_utc": (
                datetime.fromtimestamp(exploit_start, timezone.utc).isoformat()
                if exploit_start is not None
                else None
            ),
            "requests_before_first_exploit": before_first_exploit,
            "requests_between_recon_start_and_first_exploit": precursor_requests,
            "requests_by_attack_phase": dict(phase_counts),
            "apache_line_label_rows": label_rows,
            "apache_line_labels": dict(line_labels),
        }
    return result


def profile_cam(root: Path) -> dict[str, object]:
    access_path = next(root.glob("**/videoserver/logs/access.log.1"))
    attack_path = next(root.glob("**/attacker/logs/attackmate.json"))
    requests = 0
    minimum = maximum = None
    methods: collections.Counter[str] = collections.Counter()
    statuses: collections.Counter[int] = collections.Counter()
    for line in access_path.open(encoding="utf-8", errors="replace"):
        event = parse_apache(line)
        if event is None:
            continue
        requests += 1
        timestamp = float(event["timestamp"])
        minimum = timestamp if minimum is None else min(minimum, timestamp)
        maximum = timestamp if maximum is None else max(maximum, timestamp)
        methods[str(event["method"])] += 1
        statuses[int(event["status"])] += 1
    steps = []
    with attack_path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            row = json.loads(line)
            metadata = row.get("parameters", {}).get("metadata") or {}
            tactics = str(metadata.get("tactics", ""))
            techniques = str(metadata.get("techniques", ""))
            if metadata or row.get("type") in {"metasploit", "msf-session"}:
                steps.append(
                    {
                        "line": line_number,
                        "start_datetime": row.get("start-datetime"),
                        "type": row.get("type"),
                        "tactics": tactics,
                        "techniques": techniques,
                        "technique_name": metadata.get("technique_name"),
                    }
                )
    return {
        "apache_requests": requests,
        "apache_start_utc": datetime.fromtimestamp(minimum, timezone.utc).isoformat() if minimum else None,
        "apache_end_utc": datetime.fromtimestamp(maximum, timezone.utc).isoformat() if maximum else None,
        "methods": dict(methods),
        "statuses": {str(k): v for k, v in sorted(statuses.items())},
        "attackmate_labeled_or_session_steps": len(steps),
        "attackmate_steps": steps,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--datasets", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    webspotter_root = next(args.datasets.glob("webspotter-v1.0-selected/*"))
    result = {
        "webspotter": profile_webspotter(webspotter_root),
        "ait_lds_v2_1": profile_ait(args.datasets, args.datasets / "ait-alert-labels.csv"),
        "cam_lds_scenario_1": profile_cam(args.datasets / "cam-lds-scenario1-selected"),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "webspotter_files": len(result["webspotter"]),
        "ait_campaigns": len(result["ait_lds_v2_1"]),
        "cam_requests": result["cam_lds_scenario_1"]["apache_requests"],
    }, indent=2))


if __name__ == "__main__":
    main()


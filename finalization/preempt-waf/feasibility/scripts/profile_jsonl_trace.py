#!/usr/bin/env python3
"""Stream-profile a large JSON-lines network trace without copying payloads."""

from __future__ import annotations

import argparse
import collections
import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    protocols: collections.Counter[str] = collections.Counter()
    layer_keys: collections.Counter[str] = collections.Counter()
    http_field_keys: collections.Counter[str] = collections.Counter()
    records = errors = http_records = 0
    minimum = maximum = None
    with args.input.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                errors += 1
                continue
            records += 1
            protocols[str(row.get("protocol"))] += 1
            try:
                timestamp = float(row["timestamp"]) / 1000.0
                minimum = timestamp if minimum is None else min(minimum, timestamp)
                maximum = timestamp if maximum is None else max(maximum, timestamp)
            except (KeyError, TypeError, ValueError):
                pass
            layers = row.get("layers") or {}
            layer_keys.update(layers.keys())
            http = layers.get("http")
            if http is not None:
                http_records += 1
                if isinstance(http, dict):
                    http_field_keys.update(http.keys())
    result = {
        "source": str(args.input),
        "records": records,
        "json_errors": errors,
        "protocol_counts": dict(protocols.most_common()),
        "layer_presence_counts": dict(layer_keys.most_common()),
        "http_records": http_records,
        "http_field_presence_counts": dict(http_field_keys.most_common()),
        "start_utc": datetime.fromtimestamp(minimum, timezone.utc).isoformat() if minimum else None,
        "end_utc": datetime.fromtimestamp(maximum, timezone.utc).isoformat() if maximum else None,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()


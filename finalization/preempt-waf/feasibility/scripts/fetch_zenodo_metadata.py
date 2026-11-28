#!/usr/bin/env python3
"""Fetch a Zenodo record's public metadata and file manifest as JSON."""

from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("record_id")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    url = f"https://zenodo.org/api/records/{args.record_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "PREEMPT-WAF-feasibility/1.0"})
    with urllib.request.urlopen(req, timeout=120) as response:
        payload = json.load(response)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()


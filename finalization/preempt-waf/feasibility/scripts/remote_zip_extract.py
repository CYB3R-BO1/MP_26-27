#!/usr/bin/env python3
"""Extract selected members from a remote ZIP using a saved manifest.

Only each selected member's local header and compressed byte range are fetched.
The output path is constrained beneath the requested destination, and CRC/size
are verified before a temporary file is renamed into place.
"""

from __future__ import annotations

import argparse
import binascii
import json
import re
import struct
import urllib.request
import zlib
from pathlib import Path, PurePosixPath


LOCAL = b"PK\x03\x04"


def fetch(url: str, start: int, end: int) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "PREEMPT-WAF-feasibility/1.0",
            "Range": f"bytes={start}-{end}",
        },
    )
    with urllib.request.urlopen(request, timeout=300) as response:
        if response.status != 206:
            raise RuntimeError(f"Server ignored byte range (HTTP {response.status})")
        return response.read()


def safe_output(root: Path, member_name: str) -> Path:
    parts = PurePosixPath(member_name).parts
    if not parts or any(part in {"", ".", ".."} for part in parts):
        raise RuntimeError(f"Unsafe ZIP member path: {member_name!r}")
    destination = (root / Path(*parts)).resolve()
    resolved_root = root.resolve()
    if resolved_root not in destination.parents and destination != resolved_root:
        raise RuntimeError(f"ZIP member escapes destination: {member_name!r}")
    return destination


def extract_member(url: str, member: dict[str, object], destination_root: Path) -> dict[str, object]:
    offset = int(member["local_header_offset"])
    header = fetch(url, offset, offset + 65_535)
    if header[:4] != LOCAL:
        raise RuntimeError(f"Invalid local header for {member['name']}")
    values = struct.unpack_from("<4s5H3L2H", header, 0)
    _, _needed, flags, method, _time, _date, _crc, _compressed, _uncompressed, name_len, extra_len = values
    if flags & 0x1:
        raise RuntimeError(f"Encrypted ZIP member unsupported: {member['name']}")
    data_start = offset + 30 + name_len + extra_len
    compressed_size = int(member["compressed_bytes"])
    if compressed_size:
        compressed = fetch(url, data_start, data_start + compressed_size - 1)
    else:
        compressed = b""
    if method == 0:
        raw = compressed
    elif method == 8:
        raw = zlib.decompress(compressed, -zlib.MAX_WBITS)
    else:
        raise RuntimeError(f"Unsupported compression method {method}: {member['name']}")
    expected_size = int(member["uncompressed_bytes"])
    expected_crc = str(member["crc32"]).lower()
    actual_crc = f"{binascii.crc32(raw) & 0xffffffff:08x}"
    if len(raw) != expected_size or actual_crc != expected_crc:
        raise RuntimeError(
            f"Verification failed for {member['name']}: "
            f"size {len(raw)}/{expected_size}, CRC {actual_crc}/{expected_crc}"
        )
    output = safe_output(destination_root, str(member["name"]))
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(output.name + ".partial")
    temporary.write_bytes(raw)
    temporary.replace(output)
    return {
        "name": member["name"],
        "output": str(output),
        "compressed_bytes_fetched": compressed_size,
        "uncompressed_bytes_written": len(raw),
        "crc32": actual_crc,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--match", required=True, help="Python regular expression matched with re.search")
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    expression = re.compile(args.match)
    selected = [m for m in manifest["members"] if expression.search(str(m["name"]))]
    if not selected:
        raise SystemExit("No ZIP members matched")
    receipt = {
        "source_url": manifest["url"],
        "manifest": str(args.manifest),
        "match": args.match,
        "selected_count": len(selected),
        "outputs": [],
    }
    for member in selected:
        if str(member["name"]).endswith("/"):
            continue
        print(f"extracting {member['name']}", flush=True)
        receipt["outputs"].append(
            extract_member(str(manifest["url"]), member, args.destination)
        )
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    else:
        print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()


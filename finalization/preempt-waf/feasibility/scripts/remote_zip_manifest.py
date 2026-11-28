#!/usr/bin/env python3
"""List members of a remote ZIP using HTTP byte ranges.

This inspects the ZIP end record and central directory without downloading the
archive payload. ZIP64 archives are deliberately rejected rather than guessed.
"""

from __future__ import annotations

import argparse
import json
import struct
import urllib.request
from pathlib import Path


EOCD = b"PK\x05\x06"
CENTRAL = b"PK\x01\x02"


def request(url: str, byte_range: str | None = None) -> tuple[bytes, dict[str, str], int]:
    headers = {"User-Agent": "PREEMPT-WAF-feasibility/1.0"}
    if byte_range:
        headers["Range"] = byte_range
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=120) as response:
        return response.read(), dict(response.headers.items()), response.status


def remote_size(url: str) -> int:
    req = urllib.request.Request(
        url,
        method="HEAD",
        headers={"User-Agent": "PREEMPT-WAF-feasibility/1.0"},
    )
    with urllib.request.urlopen(req, timeout=120) as response:
        return int(response.headers["Content-Length"])


def decode_name(raw: bytes, flags: int) -> str:
    return raw.decode("utf-8" if flags & 0x800 else "cp437", errors="replace")


def list_remote_zip(url: str) -> dict[str, object]:
    size = remote_size(url)
    tail_size = min(size, 131_072)
    tail_start = size - tail_size
    tail, headers, status = request(url, f"bytes={tail_start}-{size - 1}")
    if status != 206:
        raise RuntimeError(f"Server ignored byte range (HTTP {status})")
    pos = tail.rfind(EOCD)
    if pos < 0 or pos + 22 > len(tail):
        raise RuntimeError("ZIP end-of-central-directory record not found")
    fields = struct.unpack_from("<4s4H2LH", tail, pos)
    _, disk_no, cd_disk, entries_disk, entries_total, cd_size, cd_offset, comment_len = fields
    if disk_no or cd_disk or entries_disk != entries_total:
        raise RuntimeError("Multi-disk ZIP archives are unsupported")
    if entries_total == 0xFFFF or cd_size == 0xFFFFFFFF or cd_offset == 0xFFFFFFFF:
        raise RuntimeError("ZIP64 archive detected; explicit ZIP64 parsing is required")
    central, _, central_status = request(
        url, f"bytes={cd_offset}-{cd_offset + cd_size - 1}"
    )
    if central_status != 206:
        raise RuntimeError(f"Central-directory range failed (HTTP {central_status})")

    members: list[dict[str, object]] = []
    cursor = 0
    while cursor < len(central):
        if central[cursor : cursor + 4] != CENTRAL:
            raise RuntimeError(f"Invalid central-directory signature at {cursor}")
        values = struct.unpack_from("<4s6H3L5H2L", central, cursor)
        (
            _, _made_by, _needed, flags, method, _mtime, _mdate, crc32,
            compressed_size, uncompressed_size, name_len, extra_len,
            comment_length, _disk_start, _internal_attr, external_attr,
            local_offset,
        ) = values
        base = cursor + 46
        name = decode_name(central[base : base + name_len], flags)
        members.append(
            {
                "name": name,
                "compressed_bytes": compressed_size,
                "uncompressed_bytes": uncompressed_size,
                "compression_method": method,
                "crc32": f"{crc32:08x}",
                "external_attributes": external_attr,
                "local_header_offset": local_offset,
            }
        )
        cursor = base + name_len + extra_len + comment_length
    if len(members) != entries_total:
        raise RuntimeError(f"Expected {entries_total} entries, parsed {len(members)}")
    return {
        "url": url,
        "archive_bytes": size,
        "content_range": headers.get("Content-Range"),
        "zip_comment_bytes": comment_len,
        "member_count": len(members),
        "total_member_compressed_bytes": sum(int(x["compressed_bytes"]) for x in members),
        "total_member_uncompressed_bytes": sum(int(x["uncompressed_bytes"]) for x in members),
        "members": members,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = list_remote_zip(args.url)
    rendered = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()


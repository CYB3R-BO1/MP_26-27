#!/usr/bin/env python3
"""Independent capture-overlap and lightweight structural checks.

Ground truth here is protocol-spec structural knowledge, not MARISSA output:
DNS has a 12-byte fixed header; Modbus/TCP has a 7-byte MBAP header followed
by a one-byte function code.  The checks validate those structures directly
from application-layer bytes and compare only boundary presence.
"""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import statistics
import struct
from collections import Counter
from pathlib import Path

from scapy.all import rdpcap

from marissa.pcap import Packet


EXPECTED_BOUNDARIES = {
    "dns": [2, 4, 6, 8, 10, 12],
    "modbus": [2, 4, 6, 7, 8],
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def application_bytes(packet) -> bytes:
    return bytes.fromhex(Packet(packet).get_applayer())


def capture_record(path: Path, protocol: str) -> tuple[dict, list[bytes], list[bytes]]:
    packets = rdpcap(str(path))
    raw = [bytes(packet) for packet in packets]
    app = [application_bytes(packet) for packet in packets]
    lengths = [len(item) for item in app]
    layers = Counter(
        layer.__name__ for packet in packets for layer in packet.layers()
    )
    record = {
        "path": str(path),
        "sha256": sha256_file(path),
        "file_bytes": path.stat().st_size,
        "packets": len(packets),
        "unique_raw_packets": len(set(raw)),
        "unique_application_messages": len(set(app)),
        "application_length_bytes": {
            "min": min(lengths),
            "median": statistics.median(lengths),
            "max": max(lengths),
        },
        "layer_occurrences": dict(sorted(layers.items())),
    }

    if protocol == "dns":
        valid = 0
        queries = 0
        responses = 0
        qdcounts = Counter()
        for message in app:
            if len(message) < 12:
                continue
            _, flags, qd, _, _, _ = struct.unpack(">HHHHHH", message[:12])
            valid += 1
            responses += bool(flags & 0x8000)
            queries += not bool(flags & 0x8000)
            qdcounts[qd] += 1
        record["independent_dns_check"] = {
            "messages_with_12_byte_header": valid,
            "queries": queries,
            "responses": responses,
            "qdcount_distribution": dict(sorted(qdcounts.items())),
        }
    elif protocol == "modbus":
        valid = 0
        protocol_id_zero = 0
        length_consistent = 0
        function_codes = Counter()
        for message in app:
            if len(message) < 8:
                continue
            _, protocol_id, declared_length, _ = struct.unpack(">HHHB", message[:7])
            valid += 1
            protocol_id_zero += protocol_id == 0
            length_consistent += declared_length == len(message) - 6
            function_codes[message[7]] += 1
        record["independent_modbus_tcp_check"] = {
            "messages_with_mbap_and_function_code": valid,
            "protocol_id_zero": protocol_id_zero,
            "length_field_consistent": length_consistent,
            "function_code_distribution": {
                str(key): value for key, value in sorted(function_codes.items())
            },
        }
    return record, raw, app


def overlap_record(smaller: list[bytes], larger: list[bytes]) -> dict:
    small_set = set(smaller)
    large_set = set(larger)
    intersection = small_set & large_set
    union = small_set | large_set
    return {
        "sequence_prefix_equal": smaller == larger[: len(smaller)],
        "smaller_unique_count": len(small_set),
        "larger_unique_count": len(large_set),
        "shared_unique_count": len(intersection),
        "smaller_unique_contained_fraction": (
            len(intersection) / len(small_set) if small_set else 0.0
        ),
        "jaccard_unique": len(intersection) / len(union) if union else 1.0,
    }


def inferred_boundary_record(output_csv: Path, protocol: str) -> dict:
    expected = set(EXPECTED_BOUNDARIES[protocol])
    by_cluster: dict[str, set[int]] = {}
    with output_csv.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            cluster = row["cluster"]
            if cluster in by_cluster:
                continue
            fields = ast.literal_eval(row["fields"])
            # MARISSA stores character offsets in its hex/alignment string.
            ends_bytes = {
                int((int(start) + int(length)) / 2)
                for start, length, _field_type in fields
            }
            by_cluster[cluster] = ends_bytes
    fixed_header_end = max(expected)
    header_boundaries = {
        cluster: {value for value in boundaries if value <= fixed_header_end}
        for cluster, boundaries in by_cluster.items()
    }
    recalls = {}
    precisions = {}
    f1s = {}
    for cluster, boundaries in header_boundaries.items():
        true_positive = len(expected & boundaries)
        recall = true_positive / len(expected)
        precision = true_positive / len(boundaries) if boundaries else 0.0
        recalls[cluster] = recall
        precisions[cluster] = precision
        f1s[cluster] = (
            2 * precision * recall / (precision + recall)
            if precision + recall
            else 0.0
        )
    return {
        "output_csv": str(output_csv),
        "expected_fixed_boundaries_bytes": sorted(expected),
        "cluster_count": len(by_cluster),
        "cluster_boundary_recall": recalls,
        "cluster_boundary_precision_within_fixed_header": precisions,
        "cluster_boundary_f1_within_fixed_header": f1s,
        "mean_cluster_boundary_recall": statistics.mean(recalls.values()),
        "mean_cluster_boundary_precision_within_fixed_header": statistics.mean(
            precisions.values()
        ),
        "mean_cluster_boundary_f1_within_fixed_header": statistics.mean(f1s.values()),
        "min_cluster_boundary_recall": min(recalls.values()),
        "max_cluster_boundary_recall": max(recalls.values()),
        "inferred_boundaries_within_fixed_header_by_cluster": {
            cluster: sorted(boundaries)
            for cluster, boundaries in header_boundaries.items()
        },
        "total_inferred_boundary_count_by_cluster": {
            cluster: len(boundaries) for cluster, boundaries in by_cluster.items()
        },
        "scope_warning": (
            "Precision/recall is restricted to independently known fixed-header "
            "boundaries. It is not whole-message field accuracy: alignments may insert "
            "gaps and DNS names are variable-length."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", required=True, type=Path)
    parser.add_argument("--results", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    report: dict = {"captures": {}, "overlap": {}, "inferred_structure": {}}
    cached: dict[tuple[str, int], tuple[list[bytes], list[bytes]]] = {}
    for protocol in ("dns", "modbus"):
        report["captures"][protocol] = {}
        for size in (100, 500, 1000):
            path = args.artifact / "dataset" / f"{protocol}_{size}.pcap"
            record, raw, app = capture_record(path, protocol)
            report["captures"][protocol][str(size)] = record
            cached[(protocol, size)] = (raw, app)

        report["overlap"][protocol] = {}
        for smaller_size, larger_size in ((100, 500), (100, 1000), (500, 1000)):
            smaller_raw, smaller_app = cached[(protocol, smaller_size)]
            larger_raw, larger_app = cached[(protocol, larger_size)]
            key = f"{smaller_size}_vs_{larger_size}"
            report["overlap"][protocol][key] = {
                "raw_packets": overlap_record(smaller_raw, larger_raw),
                "application_messages": overlap_record(smaller_app, larger_app),
            }

        report["inferred_structure"][protocol] = {}
        for size in (100, 500, 1000):
            output_csv = args.results / f"{protocol}_{size}_r1" / "output" / "output.csv"
            report["inferred_structure"][protocol][str(size)] = inferred_boundary_record(
                output_csv, protocol
            )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

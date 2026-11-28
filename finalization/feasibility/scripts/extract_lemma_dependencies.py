#!/usr/bin/env python3
"""Extract conservative, order-based Tamarin reuse-lemma dependency candidates.

This is intentionally not a semantic proof-dependency extractor.  A previous
lemma marked ``reuse`` is available to later proofs, so each such relationship
is recorded as a candidate that must be confirmed from proof states/traces.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

LEMMA = re.compile(
    r"(?m)^\s*lemma\s+([A-Za-z0-9_]+)\s*(?:\[([^\]]*)\])?\s*:"
)


def analyze(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    lemmas = []
    preceding_reuse = []
    edges = []
    for match in LEMMA.finditer(text):
        name = match.group(1)
        attributes = sorted(
            {x.strip() for x in (match.group(2) or "").split(",") if x.strip()}
        )
        for dependency in preceding_reuse:
            edges.append(
                {
                    "from": dependency,
                    "to": name,
                    "kind": "potential_prior_reuse_lemma",
                    "confirmed_used_in_proof": False,
                }
            )
        lemmas.append({"name": name, "attributes": attributes})
        if "reuse" in attributes:
            preceding_reuse.append(name)
    return {
        "path": str(path),
        "lemma_count": len(lemmas),
        "reuse_lemma_count": sum("reuse" in x["attributes"] for x in lemmas),
        "source_lemma_count": sum(
            any(a in {"source", "sources"} for a in x["attributes"])
            for x in lemmas
        ),
        "candidate_edge_count": len(edges),
        "lemmas": lemmas,
        "candidate_edges": edges,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("models", nargs="+", type=Path)
    args = parser.parse_args()
    result = {
        "method": "ordered reuse-attribute candidate extraction",
        "limitation": (
            "Edges mean only that a prior reuse lemma is available to a later "
            "proof. They do not prove that the later proof actually used it."
        ),
        "models": [analyze(path) for path in args.models],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

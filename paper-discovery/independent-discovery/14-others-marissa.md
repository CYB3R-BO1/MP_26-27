# MARISSA: Efficient Inference of Network Protocols using Similarity Digest Clustering and Multiple Sequence Algorithms

> **Status:** Candidate reference — independent discovery review, 27 November 2026. No final project choice implied. Source metadata and abstract/previous discovery evidence are distinguished from proposed hypotheses. Full-text table/figure checks, licenses, reproduction and novelty review are incomplete unless explicitly noted.

## 1. Paper identification

| Field | Value |
| --- | --- |
| Submitted by | Independent discovery (AI-assisted; not attributed to a teammate) |
| Preference | Second |
| Assigned source/category | 7 — Others |
| Authors | Pablo Ruiz-Lezcano, Daniel Uroz, Ricardo J. Rodríguez |
| Conference/journal | IEEE EuroS&P 2026 (official accepted listing) |
| Publication/acceptance date | 2026 |
| Primary paper / DOI | https://doi.org/10.1109/EuroSP68448.2026.00084 |
| Source code URL + license | https://github.com/reverseame/MARISSA (GPL-3.0 per prior review; exact commit/license and execution pending) |
| Dataset/benchmark URL + license | Repository dataset directory documented in prior review; exact dataset license and sizes pending |
| Cybersecurity problem/domain | Network protocol format inference for security analysis |
| AI techniques | Unsupervised density-based clustering and sequence analysis |

## 2. Problem and motivation

**Exact cybersecurity problem:** Undocumented protocols impede analysis of IoT and proprietary network communications.

**Why it matters:** Understanding message structures supports security analysis without binary reverse engineering.

**Prior research limitation:** Paper title and prior review describe efficiency of inference; full section-level limitations pending.

## 3. Methodology

- **Core technical idea:** Cluster similar network messages using similarity digests, then infer message formats through sequence algorithms.
- **Input data:** Captured messages from legally accessible local protocols
- **Output:** Inferred protocol message structures
- **Main components / model / verification:** Similarity digests, unsupervised clustering, multiple sequence alignment
- **What AI contributes (and why):** Unsupervised grouping avoids needing manually labeled messages; proposed learned embedding could improve inference.
- **Architecture:** our conceptual schematic (not the authors' original figure):

```text
Local packet captures -> message representation -> clustering -> format inference
```

## 4. Experimental evidence

| Item | Detail and source location |
| --- | --- |
| Datasets and size | Prior review reports nine protocols including DNS, DHCP, MQTT, Modbus; sizes and exact license pending |
| Baseline systems | Prior review reports four tools; exact baseline configurations pending |
| Evaluation metrics | Field inference accuracy, clustering quality, execution time, sample efficiency |
| Exact numerical results | Prior review reports 2–15x speedup across comparisons; exact figure and comparator not rechecked, provisional only. |
| Hardware/compute | Python/Docker implementation documented; scoped CPU experiments plausible; original environment pending. |
| Known threats to validity | Encrypted/fragmented traffic, preprocessing and sample diversity, field ground truth. |
| Reproduction status | Not attempted by our team |

Author-reported or previously surfaced numbers are not independent measurements. Statistical significance, table-level comparators and reproducibility are not established by this discovery review. Do not use provisional numerical claims in the final report until verified against the primary paper.

## 5. Candidate research gaps

| Gap | Evidence (section/page) | Author-acknowledged or our inference? | Possible overlap in 2024–2026 work |
| --- | --- | --- | --- |
| Low-sample format inference | inferred; compare existing neural protocol reverse engineering. | Our inference / proposed question | Not systematically checked; see related-work targets below. |
| Learned message embeddings | inferred; TransRE overlap likely. | Our inference / proposed question | Not systematically checked; see related-work targets below. |
| Downstream security usefulness | inferred; format inference alone is not vulnerability discovery. | Our inference / proposed question | Not systematically checked; see related-work targets below. |

A perceived gap is **not established novelty** until independently checked.

## 6. Potential methodological improvements

- **Hypothesis A:** Compare lightweight learned packet representations against digest clustering under limited observations.
- **Hypothesis B (alternative or complementary):** Assess inferred field structure on held-out local protocol versions and a controlled downstream verification task.
- **Expected security/efficiency benefit:** More useful protocol structures with fewer captured messages and controlled cost.
- **Experiment and ablation plan:** Use a small known-protocol capture set with field ground truth; compare original method and simple representation baselines; vary samples; report field precision/recall, clustering and runtime; ablate learned representation.
- **Risk of failure or overlap:** Classical ML baseline; TransRE and protocol inference literature may already address extension.

Do not finalize a project architecture at discovery stage.

## 7. Implementation feasibility by 2026-12-31

| Requirement | Assessment |
| --- | --- |
| Public code verified and actually tested? | https://github.com/reverseame/MARISSA (GPL-3.0 per prior review; exact commit/license and execution pending); not executed. |
| Datasets available and legally usable? | Repository dataset directory documented in prior review; exact dataset license and sizes pending; confirm terms before use. |
| Models/inference APIs available? | Unsupervised density-based clustering and sequence analysis; no paid APIs allowed; local feasibility not demonstrated. |
| Hardware, API cost, and development effort | Python/Docker implementation documented; scoped CPU experiments plausible; original environment pending. |
| Realistic five-week minimum implementation | One to three protocols and local CPU inference; no binary analysis. |
| Features deliberately excluded | Full production IoT protocol reverse engineering, encrypted payload recovery, paid APIs. |
| Top blockers | Dataset licenses, original execution, field-label validation, related-work overlap. |
| Verdict | Conditional |

## 8. Two-group potential (7 members)

- **Group A (4 members) — possible independently measurable contribution:** Representation and clustering experiments
- **Group B (3 members) — distinct but complementary contribution:** Field inference and held-out validation
- **How the contributions integrate:** Shared packet and cluster representation
- **How each group demonstrates a result separately:** A reports clustering/sample efficiency; B reports field recovery and utility

Provisional only; no team assignment is implied.

## 9. Consistent selection rubric (1–5 each)

Provisional discovery assessments, not rankings or experimental measurements. Reassess after full text and feasibility checks.

| Criterion | Score / 5 | Evidence |
| --- | --- | --- |
| Research quality and relevance | 5 | IEEE EuroS&P 2026 (official accepted listing); Network protocol format inference for security analysis |
| Implementation feasibility | 4 | One to three protocols and local CPU inference; no binary analysis. Blockers: Dataset licenses, original execution, field-label validation, related-work overlap. |
| Novelty potential | 3 | Classical ML baseline; TransRE and protocol inference literature may already address extension. |
| Different from previous federated/continual/graph IDS | 5 | Problem: Undocumented protocols impede analysis of IoT and proprietary network communications. |
| Meaningful AI for cybersecurity | 4 | Unsupervised grouping avoids needing manually labeled messages; proposed learned embedding could improve inference. |
| Technically justified modernity | 4 | Unsupervised density-based clustering and sequence analysis |
| Public resources/reproducibility | 4 | https://github.com/reverseame/MARISSA (GPL-3.0 per prior review; exact commit/license and execution pending); Repository dataset directory documented in prior review; exact dataset license and sizes pending |
| Measurable improvement | 5 | Field inference accuracy, clustering quality, execution time, sample efficiency |
| Two complementary contributions | 4 | Representation and clustering experiments / Field inference and held-out validation |
| **Total** | **38/45** | Critical blockers outweigh totals. |

## 10. Final assessment

- **Strongest three reasons to shortlist:** Verified venue; local network analysis; public code.
- **Three weaknesses or risks:** Classical ML; exact datasets pending; extension novelty.
- **Unverified claims to investigate:** Dataset licenses, original execution, field-label validation, related-work overlap.; exact paper sections/tables, relevant licenses, compute and full related work.
- **Recommendation:** Conditional — discovery candidate only; no shortlisting decision.
- **One-sentence argument versus competing papers:** Different from CAP/Elastispec and previous IDS; practical protocol security precursor.

## 11. Supporting references

- Primary paper: https://doi.org/10.1109/EuroSP68448.2026.00084
- Official venue/record: https://eurosp2026.ieee-security.org/accepted_and_awards.html
- Repository/benchmark: https://github.com/reverseame/MARISSA (GPL-3.0 per prior review; exact commit/license and execution pending); Repository dataset directory documented in prior review; exact dataset license and sizes pending
- Closest related 2024–2026 work: TransRE https://doi.org/10.1145/3797124 ; ProtocolGuard (NDSS 2026).

## Submission checklist

- [x] Bibliographic details verified from primary publication (venue/publisher or accepted listing; see specific caveats)
- [x] Author claims separated from personal hypotheses
- [ ] Actual figures/tables used for quantitative results
- [ ] Code, datasets, licenses and compute availability checked
- [ ] Research gap supported by evidence and related-work review
- [x] December 31 feasibility assessed (provisional)
- [x] Two-group contributions considered
- [x] Nine rubric scores justified (provisional)


# Loop-Filter: A Feedback Control Approach for Eliminating Link Flooding Attack

> **Status:** Candidate reference — independent discovery review, 27 November 2026. No final project choice implied. Source metadata and abstract/previous discovery evidence are distinguished from proposed hypotheses. Full-text table/figure checks, licenses, reproduction and novelty review are incomplete unless explicitly noted.

## 1. Paper identification

| Field | Value |
| --- | --- |
| Submitted by | Independent discovery (AI-assisted; not attributed to a teammate) |
| Preference | First |
| Assigned source/category | 6 — IEEE TIFS |
| Authors | Can Chen, Qinghao Wang, Ning Lu, Wenbo Shi |
| Conference/journal | IEEE Transactions on Information Forensics and Security, vol. 21, pp. 272–287 (2026) |
| Publication/acceptance date | 2026 volume; DOI assigned 2025. Membership in exact user-linked collection not verified. |
| Primary paper / DOI | https://doi.org/10.1109/TIFS.2025.3640856 |
| Source code URL + license | Not found/verified |
| Dataset/benchmark URL + license | Original network experiment configuration and data not verified |
| Cybersecurity problem/domain | Active network defense against link flooding |
| AI techniques | Feedback control and reinforcement learning (prior discovery characterization; full method pending) |

## 2. Problem and motivation

**Exact cybersecurity problem:** Network congestion attacks can adapt to static filtering and disrupt availability.

**Why it matters:** Protection should preserve legitimate throughput rather than classify traffic alone.

**Prior research limitation:** Title/publisher metadata establish feedback-control approach; detailed method/sections pending.

## 3. Methodology

- **Core technical idea:** Prior discovery describes adaptive filtering and cross-domain coordination; verify full text before design.
- **Input data:** Network state and feedback (provisional)
- **Output:** Defensive filtering decisions (provisional)
- **Main components / model / verification:** Feedback loop; learning and collaboration details need source verification
- **What AI contributes (and why):** Potential learned action policy, subject to verifying actual paper methodology.
- **Architecture:** our conceptual schematic (not the authors' original figure):

```text
Simulated network state -> feedback policy -> mitigation -> service availability
```

## 4. Experimental evidence

| Item | Detail and source location |
| --- | --- |
| Datasets and size | Not verified |
| Baseline systems | Not verified |
| Evaluation metrics | Proposed legitimate throughput, link utilization, recovery time, unnecessary filtering |
| Exact numerical results | No exact values verified; do not cite numerical performance. |
| Hardware/compute | Proposed small simulation may run on CPU; original hardware unknown. |
| Known threats to validity | Simulation fidelity, legitimate traffic disruption, adaptive adversaries, policy stability. |
| Reproduction status | Not attempted by our team |

Author-reported or previously surfaced numbers are not independent measurements. Statistical significance, table-level comparators and reproducibility are not established by this discovery review. Do not use provisional numerical claims in the final report until verified against the primary paper.

## 5. Candidate research gaps

| Gap | Evidence (section/page) | Author-acknowledged or our inference? | Possible overlap in 2024–2026 work |
| --- | --- | --- | --- |
| Single-domain constrained deployment | inferred from prior discovery; original scope needs checking. | Our inference / proposed question | Not systematically checked; see related-work targets below. |
| Protection of legitimate service | inferred; compare mitigation/control approaches. | Our inference / proposed question | Not systematically checked; see related-work targets below. |
| Budget-aware adaptive policy | inferred; novelty unverified. | Our inference / proposed question | Not systematically checked; see related-work targets below. |

A perceived gap is **not established novelty** until independently checked.

## 6. Potential methodological improvements

- **Hypothesis A:** Study bounded defensive action policy in isolated network simulation.
- **Hypothesis B (alternative or complementary):** Measure legitimate service continuity and recovery versus fixed control.
- **Expected security/efficiency benefit:** Availability under controlled congestion without excessive collateral filtering.
- **Experiment and ablation plan:** After verifying full paper, model benign and synthetic congestion in local simulation; compare static and feedback baseline, learned controller and ablations; fixed resources.
- **Risk of failure or overlap:** Original implementation unavailable; may be a conventional controller rather than substantial AI; exact collection uncertain.

Do not finalize a project architecture at discovery stage.

## 7. Implementation feasibility by 2026-12-31

| Requirement | Assessment |
| --- | --- |
| Public code verified and actually tested? | Not found/verified; not executed. |
| Datasets available and legally usable? | Original network experiment configuration and data not verified; confirm terms before use. |
| Models/inference APIs available? | Feedback control and reinforcement learning (prior discovery characterization; full method pending); no paid APIs allowed; local feasibility not demonstrated. |
| Hardware, API cost, and development effort | Proposed small simulation may run on CPU; original hardware unknown. |
| Realistic five-week minimum implementation | One software network topology with synthetic local workloads. |
| Features deliberately excluded | Blockchain infrastructure, multi-domain production deployment, live attack traffic. |
| Top blockers | Full text, exact collection, code, baseline, novelty. |
| Verdict | Conditional |

## 8. Two-group potential (7 members)

- **Group A (4 members) — possible independently measurable contribution:** Network simulation and controller
- **Group B (3 members) — distinct but complementary contribution:** Availability/overhead evaluation and safe constraints
- **How the contributions integrate:** Shared simulation state and action interface
- **How each group demonstrates a result separately:** A reports control performance; B reports service continuity

Provisional only; no team assignment is implied.

## 9. Consistent selection rubric (1–5 each)

Provisional discovery assessments, not rankings or experimental measurements. Reassess after full text and feasibility checks.

| Criterion | Score / 5 | Evidence |
| --- | --- | --- |
| Research quality and relevance | 4 | IEEE Transactions on Information Forensics and Security, vol. 21, pp. 272–287 (2026); Active network defense against link flooding |
| Implementation feasibility | 3 | One software network topology with synthetic local workloads. Blockers: Full text, exact collection, code, baseline, novelty. |
| Novelty potential | 3 | Original implementation unavailable; may be a conventional controller rather than substantial AI; exact collection uncertain. |
| Different from previous federated/continual/graph IDS | 5 | Problem: Network congestion attacks can adapt to static filtering and disrupt availability. |
| Meaningful AI for cybersecurity | 3 | Potential learned action policy, subject to verifying actual paper methodology. |
| Technically justified modernity | 4 | Feedback control and reinforcement learning (prior discovery characterization; full method pending) |
| Public resources/reproducibility | 2 | Not found/verified; Original network experiment configuration and data not verified |
| Measurable improvement | 4 | Proposed legitimate throughput, link utilization, recovery time, unnecessary filtering |
| Two complementary contributions | 4 | Network simulation and controller / Availability/overhead evaluation and safe constraints |
| **Total** | **32/45** | Critical blockers outweigh totals. |

## 10. Final assessment

- **Strongest three reasons to shortlist:** Established journal; active defense; measurable service outcomes.
- **Three weaknesses or risks:** 2025 DOI; exact collection not verified; missing code/full method.
- **Unverified claims to investigate:** Full text, exact collection, code, baseline, novelty.; exact paper sections/tables, relevant licenses, compute and full related work.
- **Recommendation:** Conditional — discovery candidate only; no shortlisting decision.
- **One-sentence argument versus competing papers:** More action-oriented than UTFormer and LLMBA, but much less resource-verified.

## 11. Supporting references

- Primary paper: https://doi.org/10.1109/TIFS.2025.3640856
- Official venue/record: https://dblp.org/db/journals/tifs/tifs21.html ; https://ieeexplore.ieee.org/xpl/tocresult.jsp?isnumber=11313711&punumber=10206
- Repository/benchmark: Not found/verified; Original network experiment configuration and data not verified
- Closest related 2024–2026 work: EcoShield (IEEE TNSE 2026, author publication list); adaptive congestion mitigation review pending.

## Submission checklist

- [x] Bibliographic details verified from primary publication (venue/publisher or accepted listing; see specific caveats)
- [x] Author claims separated from personal hypotheses
- [ ] Actual figures/tables used for quantitative results
- [ ] Code, datasets, licenses and compute availability checked
- [ ] Research gap supported by evidence and related-work review
- [x] December 31 feasibility assessed (provisional)
- [x] Two-group contributions considered
- [x] Nine rubric scores justified (provisional)


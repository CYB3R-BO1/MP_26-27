# ProtocolGuard: Detecting Protocol Non-compliance Bugs via LLM-guided Static Analysis and Dynamic Verification

> **Status:** Candidate reference — independent discovery review, 27 November 2026. No final project choice implied. Source metadata and abstract/previous discovery evidence are distinguished from proposed hypotheses. Full-text table/figure checks, licenses, reproduction and novelty review are incomplete unless explicitly noted.

## 1. Paper identification

| Field | Value |
| --- | --- |
| Submitted by | Independent discovery (AI-assisted; not attributed to a teammate) |
| Preference | First |
| Assigned source/category | 4 — NDSS |
| Authors | Xiangpu Song, Longjia Pei, Jianliang Wu, Yingpei Zeng, Gaoshuo He, Chaoshun Zuo, Xiaofeng Liu, Qingchuan Zhao, Shanqing Guo |
| Conference/journal | NDSS 2026 |
| Publication/acceptance date | February 2026 |
| Primary paper / DOI | https://www.ndss-symposium.org/wp-content/uploads/2026-f521-paper.pdf |
| Source code URL + license | https://secartifacts.github.io/ndss2026/results (artifact Available per teammate's review; actual package/license/run pending) |
| Dataset/benchmark URL + license | 11 protocol implementations reported; exact target versions and licenses pending |
| Cybersecurity problem/domain | Network protocol implementation security |
| AI techniques | LLM-guided static analysis and dynamic verification |

## 2. Problem and motivation

**Exact cybersecurity problem:** Implementations can violate protocol requirements in security-relevant ways.

**Why it matters:** Implementation deviations can undermine intended network security guarantees.

**Prior research limitation:** Official program abstract identifies ambiguity of natural-language specifications; teammate review cites Section VI limitations.

## 3. Methodology

- **Core technical idea:** Use LLM-assisted analysis to derive checks, then verify candidate violations through runtime testing.
- **Input data:** Protocol specification and implementation code
- **Output:** Dynamically verified non-compliance findings
- **Main components / model / verification:** Program slicing, assertion generation, verification harness
- **What AI contributes (and why):** LLM connects specification semantics to implementation; runtime evidence constrains errors.
- **Architecture:** our conceptual schematic (not the authors' original figure):

```text
Specification + implementation -> analysis -> assertions -> local dynamic verification
```

## 4. Experimental evidence

| Item | Detail and source location |
| --- | --- |
| Datasets and size | 11 protocol implementations per prior discovery; exact versions pending |
| Baseline systems | Existing protocol bug detection tools; exact configurations pending |
| Evaluation metrics | Verified violations, precision/recall, assertion correctness, coverage |
| Exact numerical results | Earlier discovery reports 158 non-compliance bugs across 11 implementations; table/section not rechecked in this pass. Official program states precision/recall improvement without exact values in retrieved abstract. |
| Hardware/compute | Original model/API and C toolchain requirements need verification; no paid inference allowed in proposed scope. |
| Known threats to validity | Specification ambiguity, oracle fidelity, path coverage, assertion errors. |
| Reproduction status | Not attempted by our team |

Author-reported or previously surfaced numbers are not independent measurements. Statistical significance, table-level comparators and reproducibility are not established by this discovery review. Do not use provisional numerical claims in the final report until verified against the primary paper.

## 5. Candidate research gaps

| Gap | Evidence (section/page) | Author-acknowledged or our inference? | Possible overlap in 2024–2026 work |
| --- | --- | --- | --- |
| Runtime execution context for assertion generation | author-acknowledged Section VI per existing teammate review; dynamic program analysis overlap unchecked. | Author-acknowledged per cited review; verify section | Not systematically checked; see related-work targets below. |
| Protocol-aware exploration | author-acknowledged Section VI per teammate review; existing state-aware fuzzing overlap. | Author-acknowledged per cited review; verify section | Not systematically checked; see related-work targets below. |
| Callback-aware slicing | author-acknowledged per teammate review; interprocedural analysis overlap. | Author-acknowledged per cited review; verify section | Not systematically checked; see related-work targets below. |

A perceived gap is **not established novelty** until independently checked.

## 6. Potential methodological improvements

- **Hypothesis A:** Use bounded runtime context to improve assertion reliability in local test fixtures.
- **Hypothesis B (alternative or complementary):** Measure state-aware verification and compare against fixed verification budget.
- **Expected security/efficiency benefit:** More independently verified deviations with fewer incorrect assertions.
- **Experiment and ablation plan:** Reproduce one small open-source implementation in a local sandbox, compare baseline assertion/verification versus scoped improvements, report compilation and oracle correctness, coverage and cost.
- **Risk of failure or overlap:** Original authors already suggest these directions; local LM may be insufficient.

Do not finalize a project architecture at discovery stage.

## 7. Implementation feasibility by 2026-12-31

| Requirement | Assessment |
| --- | --- |
| Public code verified and actually tested? | https://secartifacts.github.io/ndss2026/results (artifact Available per teammate's review; actual package/license/run pending); not executed. |
| Datasets available and legally usable? | 11 protocol implementations reported; exact target versions and licenses pending; confirm terms before use. |
| Models/inference APIs available? | LLM-guided static analysis and dynamic verification; no paid APIs allowed; local feasibility not demonstrated. |
| Hardware, API cost, and development effort | Original model/API and C toolchain requirements need verification; no paid inference allowed in proposed scope. |
| Realistic five-week minimum implementation | One protocol and small local test set; local inference feasibility gate. |
| Features deliberately excluded | Full 11-implementation evaluation, paid APIs, binary analysis and third-party testing. |
| Top blockers | Artifact, toolchain, local model and novelty. |
| Verdict | Conditional |

## 8. Two-group potential (7 members)

- **Group A (4 members) — possible independently measurable contribution:** Specification-to-assertion validation
- **Group B (3 members) — distinct but complementary contribution:** Runtime verification and state coverage
- **How the contributions integrate:** Shared assertion interface and controlled test oracle
- **How each group demonstrates a result separately:** A reports correctness; B reports verified violations and coverage

Provisional only; no team assignment is implied.

## 9. Consistent selection rubric (1–5 each)

Provisional discovery assessments, not rankings or experimental measurements. Reassess after full text and feasibility checks.

| Criterion | Score / 5 | Evidence |
| --- | --- | --- |
| Research quality and relevance | 5 | NDSS 2026; Network protocol implementation security |
| Implementation feasibility | 2 | One protocol and small local test set; local inference feasibility gate. Blockers: Artifact, toolchain, local model and novelty. |
| Novelty potential | 4 | Original authors already suggest these directions; local LM may be insufficient. |
| Different from previous federated/continual/graph IDS | 5 | Problem: Implementations can violate protocol requirements in security-relevant ways. |
| Meaningful AI for cybersecurity | 5 | LLM connects specification semantics to implementation; runtime evidence constrains errors. |
| Technically justified modernity | 5 | LLM-guided static analysis and dynamic verification |
| Public resources/reproducibility | 3 | https://secartifacts.github.io/ndss2026/results (artifact Available per teammate's review; actual package/license/run pending); 11 protocol implementations reported; exact target versions and licenses pending |
| Measurable improvement | 5 | Verified violations, precision/recall, assertion correctness, coverage |
| Two complementary contributions | 5 | Specification-to-assertion validation / Runtime verification and state coverage |
| **Total** | **39/45** | Critical blockers outweigh totals. |

## 10. Final assessment

- **Strongest three reasons to shortlist:** Strong venue; concrete network protocol problem; author-acknowledged gaps.
- **Three weaknesses or risks:** API risk; C toolchain; authors already propose some fixes.
- **Unverified claims to investigate:** Artifact, toolchain, local model and novelty.; exact paper sections/tables, relevant licenses, compute and full related work.
- **Recommendation:** Conditional — discovery candidate only; no shortlisting decision.
- **One-sentence argument versus competing papers:** Independently retained from Harsha's existing submission; more distinct from IDS than WebSpotter.

## 11. Supporting references

- Primary paper: https://www.ndss-symposium.org/wp-content/uploads/2026-f521-paper.pdf
- Official venue/record: https://www.ndss-symposium.org/ndss2026/accepted-papers/
- Repository/benchmark: https://secartifacts.github.io/ndss2026/results (artifact Available per teammate's review; actual package/license/run pending); 11 protocol implementations reported; exact target versions and licenses pending
- Closest related 2024–2026 work: Existing review ../harsha-vardhan/02-protocolguard.md ; TamRL https://arxiv.org/abs/2605.23643 .

## Submission checklist

- [x] Bibliographic details verified from primary publication (venue/publisher or accepted listing; see specific caveats)
- [x] Author claims separated from personal hypotheses
- [ ] Actual figures/tables used for quantitative results
- [ ] Code, datasets, licenses and compute availability checked
- [ ] Research gap supported by evidence and related-work review
- [x] December 31 feasibility assessed (provisional)
- [x] Two-group contributions considered
- [x] Nine rubric scores justified (provisional)


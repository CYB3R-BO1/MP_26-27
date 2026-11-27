# PathProb: Probabilistic Inference and Path Scoring for Enhanced and Flexible BGP Route Leak Detection

> **Status:** Candidate reference — independent discovery review, 27 November 2026. No final project choice implied. Source metadata and abstract/previous discovery evidence are distinguished from proposed hypotheses. Full-text table/figure checks, licenses, reproduction and novelty review are incomplete unless explicitly noted.

## 1. Paper identification

| Field | Value |
| --- | --- |
| Submitted by | Independent discovery (AI-assisted; not attributed to a teammate) |
| Preference | Second |
| Assigned source/category | 4 — NDSS |
| Authors | Yingqian Hao, Hui Zou, Lu Zhou, Yuxuan Chen, Yanbiao Li |
| Conference/journal | NDSS 2026 |
| Publication/acceptance date | February 2026 |
| Primary paper / DOI | https://www.ndss-symposium.org/ndss-paper/pathprob-probabilistic-inference-and-path-scoring-for-enhanced-and-flexible-bgp-route-leak-detection/ |
| Source code URL + license | https://github.com/hyq8868/PathProb (license/run pending); https://secartifacts.github.io/ndss2026/results |
| Dataset/benchmark URL + license | https://doi.org/10.5281/zenodo.17920056 (artifact link; download/license pending) |
| Cybersecurity problem/domain | BGP routing security |
| AI techniques | Topology-aware probabilistic inference (not necessarily deep learning) |

## 2. Problem and motivation

**Exact cybersecurity problem:** Route leaks undermine Internet routing; deterministic relationship assumptions can be unreliable.

**Why it matters:** Improper routing can cause disruption or unintended transit.

**Prior research limitation:** Official program abstract motivates topology-aware probabilities and path legitimacy scoring.

## 3. Methodology

- **Core technical idea:** Infer distributions over AS link relationships and score AS paths.
- **Input data:** AS topology and routing paths
- **Output:** Path legitimacy scores / leak candidates
- **Main components / model / verification:** Probabilistic relationship inference, scoring, validation
- **What AI contributes (and why):** Statistical inference models uncertain relationships; defensive extension must go beyond classification.
- **Architecture:** our conceptual schematic (not the authors' original figure):

```text
Routing observations -> probabilistic inference -> path score -> proposed safe routing decision
```

## 4. Experimental evidence

| Item | Detail and source location |
| --- | --- |
| Datasets and size | High-confidence validation dataset noted by official program; sizes and splits pending |
| Baseline systems | Existing relationship inference methods; exact names/configurations pending |
| Evaluation metrics | Inference accuracy, leak detection; proposed legitimate route acceptance, convergence, availability |
| Exact numerical results | Official program reports improved inference performance; exact numerical results not rechecked. NDSS artifact page lists PathProb (slightly different subtitle) as Available, Functional and Reproduced; independent artifact badge does not mean team reproduction. |
| Hardware/compute | Scoped offline routing simulation likely CPU-feasible; original data size and hardware pending. |
| Known threats to validity | Incomplete topology, uncertain labels, temporal drift, disruption from erroneous rejection. |
| Reproduction status | Not attempted by our team |

Author-reported or previously surfaced numbers are not independent measurements. Statistical significance, table-level comparators and reproducibility are not established by this discovery review. Do not use provisional numerical claims in the final report until verified against the primary paper.

## 5. Candidate research gaps

| Gap | Evidence (section/page) | Author-acknowledged or our inference? | Possible overlap in 2024–2026 work |
| --- | --- | --- | --- |
| Safe decisions under uncertain scores | inferred from scoring output; routing policy overlap unchecked. | Our inference / proposed question | Not systematically checked; see related-work targets below. |
| Temporal robustness | inferred; review route leak evaluation literature. | Our inference / proposed question | Not systematically checked; see related-work targets below. |
| Risk-constrained filtering | proposed mitigation rather than another classifier; deployment consequences need simulation. | Our inference / proposed question | Not systematically checked; see related-work targets below. |

A perceived gap is **not established novelty** until independently checked.

## 6. Potential methodological improvements

- **Hypothesis A:** Assess probability calibration and uncertainty under held-out routing scenarios.
- **Hypothesis B (alternative or complementary):** Evaluate conservative simulated route-handling policy using scores.
- **Expected security/efficiency benefit:** Improve routing safety without rejecting legitimate reachability.
- **Experiment and ablation plan:** Offline replay or isolated simulated AS topology; compare fixed score threshold, calibrated policy and conventional routing policy; measure legitimate acceptance, leak avoidance, convergence and compute.
- **Risk of failure or overlap:** Original focus detection; proposed mitigation may be too policy-centric or already studied.

Do not finalize a project architecture at discovery stage.

## 7. Implementation feasibility by 2026-12-31

| Requirement | Assessment |
| --- | --- |
| Public code verified and actually tested? | https://github.com/hyq8868/PathProb (license/run pending); https://secartifacts.github.io/ndss2026/results; not executed. |
| Datasets available and legally usable? | https://doi.org/10.5281/zenodo.17920056 (artifact link; download/license pending); confirm terms before use. |
| Models/inference APIs available? | Topology-aware probabilistic inference (not necessarily deep learning); no paid APIs allowed; local feasibility not demonstrated. |
| Hardware, API cost, and development effort | Scoped offline routing simulation likely CPU-feasible; original data size and hardware pending. |
| Realistic five-week minimum implementation | Small replay/simulation, no real BGP announcements. |
| Features deliberately excluded | Internet-scale deployment, traffic classification, production route manipulation. |
| Top blockers | Dataset/license, BGP simulation expertise, novelty. |
| Verdict | Conditional |

## 8. Two-group potential (7 members)

- **Group A (4 members) — possible independently measurable contribution:** Probability calibration and baseline inference
- **Group B (3 members) — distinct but complementary contribution:** Safe decision policy and simulation
- **How the contributions integrate:** Shared AS path scores and replay environment
- **How each group demonstrates a result separately:** A reports calibration; B reports availability and mitigation

Provisional only; no team assignment is implied.

## 9. Consistent selection rubric (1–5 each)

Provisional discovery assessments, not rankings or experimental measurements. Reassess after full text and feasibility checks.

| Criterion | Score / 5 | Evidence |
| --- | --- | --- |
| Research quality and relevance | 5 | NDSS 2026; BGP routing security |
| Implementation feasibility | 4 | Small replay/simulation, no real BGP announcements. Blockers: Dataset/license, BGP simulation expertise, novelty. |
| Novelty potential | 3 | Original focus detection; proposed mitigation may be too policy-centric or already studied. |
| Different from previous federated/continual/graph IDS | 4 | Problem: Route leaks undermine Internet routing; deterministic relationship assumptions can be unreliable. |
| Meaningful AI for cybersecurity | 3 | Statistical inference models uncertain relationships; defensive extension must go beyond classification. |
| Technically justified modernity | 4 | Topology-aware probabilistic inference (not necessarily deep learning) |
| Public resources/reproducibility | 5 | https://github.com/hyq8868/PathProb (license/run pending); https://secartifacts.github.io/ndss2026/results; https://doi.org/10.5281/zenodo.17920056 (artifact link; download/license pending) |
| Measurable improvement | 5 | Inference accuracy, leak detection; proposed legitimate route acceptance, convergence, availability |
| Two complementary contributions | 4 | Probability calibration and baseline inference / Safe decision policy and simulation |
| **Total** | **37/45** | Critical blockers outweigh totals. |

## 10. Final assessment

- **Strongest three reasons to shortlist:** Verified venue; reproduced artifact; routing security.
- **Three weaknesses or risks:** Detection-centric baseline; policy risk; exact data not downloaded.
- **Unverified claims to investigate:** Dataset/license, BGP simulation expertise, novelty.; exact paper sections/tables, relevant licenses, compute and full related work.
- **Recommendation:** Conditional — discovery candidate only; no shortlisting decision.
- **One-sentence argument versus competing papers:** More infrastructure-focused than WebSpotter; less AI-depth than TamRL.

## 11. Supporting references

- Primary paper: https://www.ndss-symposium.org/ndss-paper/pathprob-probabilistic-inference-and-path-scoring-for-enhanced-and-flexible-bgp-route-leak-detection/
- Official venue/record: https://www.ndss-symposium.org/ndss2026/accepted-papers/
- Repository/benchmark: https://github.com/hyq8868/PathProb (license/run pending); https://secartifacts.github.io/ndss2026/results; https://doi.org/10.5281/zenodo.17920056 (artifact link; download/license pending)
- Closest related 2024–2026 work: RPKI/ASPA and probabilistic AS inference literature (review pending).

## Submission checklist

- [x] Bibliographic details verified from primary publication (venue/publisher or accepted listing; see specific caveats)
- [x] Author claims separated from personal hypotheses
- [ ] Actual figures/tables used for quantitative results
- [ ] Code, datasets, licenses and compute availability checked
- [ ] Research gap supported by evidence and related-work review
- [x] December 31 feasibility assessed (provisional)
- [x] Two-group contributions considered
- [x] Nine rubric scores justified (provisional)


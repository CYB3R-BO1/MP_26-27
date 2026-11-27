# Network-Level Prompt and Trait Leakage in Local Research Agents

> **Status:** Candidate reference — independent discovery review, 27 November 2026. No final project choice implied. Source metadata and abstract/previous discovery evidence are distinguished from proposed hypotheses. Full-text table/figure checks, licenses, reproduction and novelty review are incomplete unless explicitly noted.

## 1. Paper identification

| Field | Value |
| --- | --- |
| Submitted by | Independent discovery (AI-assisted; not attributed to a teammate) |
| Preference | First |
| Assigned source/category | 2 — USENIX Security Cycle 1 |
| Authors | Hyejun Jeong, Mohammadreza Teymoorianfard, Abhinav Kumar, Amir Houmansadr, Eugene Bagdasarian |
| Conference/journal | USENIX Security 2026, Cycle 1 (official list confirms) |
| Publication/acceptance date | 2026 proceedings |
| Primary paper / DOI | https://www.usenix.org/conference/usenixsecurity26/presentation/jeong |
| Source code URL + license | https://github.com/umass-aisec/wra (linked research code; contents/license/run not verified in this pass) |
| Dataset/benchmark URL + license | WRA traces from real search queries and synthetic personas; original trace download and license not checked |
| Cybersecurity problem/domain | Network privacy of local AI agents |
| AI techniques | LLM-based research agents and inference; proposed learned defensive policy |

## 2. Problem and motivation

**Exact cybersecurity problem:** Network metadata from research agents can expose confidential task information despite encryption.

**Why it matters:** Local deployment does not prevent disclosure to network intermediaries; agent browsing creates distinctive patterns.

**Prior research limitation:** Official Cycle 1 abstract identifies leakage from agent-specific browsing behavior and evaluates mitigations.

## 3. Methodology

- **Core technical idea:** Analyze agent traffic traces and quantify task/trait leakage; original paper studies protection alternatives.
- **Input data:** Agent network metadata, task labels and synthetic personas
- **Output:** Leakage measurements and defense evaluation
- **Main components / model / verification:** Trace dataset, inference evaluation, OBELS metric, domain-diversity/obfuscation mitigations
- **What AI contributes (and why):** AI creates the workload and leakage inference; proposed extension uses learning for protective decisions, not just analysis.
- **Architecture:** our conceptual schematic (not the authors' original figure):

```text
Local agent -> network traces -> leakage evaluation -> adaptive defense hypothesis
```

## 4. Experimental evidence

| Item | Detail and source location |
| --- | --- |
| Datasets and size | Real user search queries and synthetic persona traces; size not verified |
| Baseline systems | Unmitigated agents and mitigation variants; exact configurations pending |
| Evaluation metrics | OBELS, trait recovery, task utility, mitigation overhead |
| Exact numerical results | Official Cycle 1 abstract reports 70–140 domains per request, over 73% prompt functional/domain knowledge recovered, up to 19 of 32 latent traits, and average 29% reduction in attack effectiveness from mitigations. Table-level verification pending. |
| Hardware/compute | Offline trace evaluation may be CPU-feasible; live agents and evaluation models may require GPU/API; no paid tokens assumed. |
| Known threats to validity | Synthetic personas, agent-version drift, privacy of traces, evaluation model dependence. |
| Reproduction status | Not attempted by our team |

Author-reported or previously surfaced numbers are not independent measurements. Statistical significance, table-level comparators and reproducibility are not established by this discovery review. Do not use provisional numerical claims in the final report until verified against the primary paper.

## 5. Candidate research gaps

| Gap | Evidence (section/page) | Author-acknowledged or our inference? | Possible overlap in 2024–2026 work |
| --- | --- | --- | --- |
| Adaptive privacy–utility tradeoff | official abstract discusses mitigations; inferred extension; traffic shaping literature unchecked. | Our inference / proposed question | Not systematically checked; see related-work targets below. |
| Generalization across agent workloads | inferred; requires held-out agent/task traces. | Our inference / proposed question | Not systematically checked; see related-work targets below. |
| Local evaluation without frontier judges | inferred; benchmark metric fidelity and overlap unchecked. | Our inference / proposed question | Not systematically checked; see related-work targets below. |

A perceived gap is **not established novelty** until independently checked.

## 6. Potential methodological improvements

- **Hypothesis A:** Learn a lightweight policy for selecting protective network behavior from trace features.
- **Hypothesis B (alternative or complementary):** Evaluate privacy and task utility under a fixed overhead constraint.
- **Expected security/efficiency benefit:** Reduced leakage without excessive traffic cost or task disruption.
- **Experiment and ablation plan:** Offline replay of legally usable traces plus controlled local agent workload if feasible; compare unprotected, fixed mitigation and learned policy; separate tasks; measure OBELS or validated proxy, latency, bandwidth and utility.
- **Risk of failure or overlap:** Original mitigations may overlap; offline proxy may not establish live-agent protection.

Do not finalize a project architecture at discovery stage.

## 7. Implementation feasibility by 2026-12-31

| Requirement | Assessment |
| --- | --- |
| Public code verified and actually tested? | https://github.com/umass-aisec/wra (linked research code; contents/license/run not verified in this pass); not executed. |
| Datasets available and legally usable? | WRA traces from real search queries and synthetic personas; original trace download and license not checked; confirm terms before use. |
| Models/inference APIs available? | LLM-based research agents and inference; proposed learned defensive policy; no paid APIs allowed; local feasibility not demonstrated. |
| Hardware, API cost, and development effort | Offline trace evaluation may be CPU-feasible; live agents and evaluation models may require GPU/API; no paid tokens assumed. |
| Realistic five-week minimum implementation | One trace collection and replay-based defense simulation; local live pilot only if resources permit. |
| Features deliberately excluded | Large-scale new trace generation, paid inference, real users' private data. |
| Top blockers | Trace availability/license, metric implementation and local evaluation model, novelty. |
| Verdict | Conditional |

## 8. Two-group potential (7 members)

- **Group A (4 members) — possible independently measurable contribution:** Trace processing, privacy metrics and leakage evaluation
- **Group B (3 members) — distinct but complementary contribution:** Learned privacy controller and overhead/utility assessment
- **How the contributions integrate:** Shared replay interface and fixed budgets
- **How each group demonstrates a result separately:** A reports leakage and evaluation validity; B reports protection–utility frontier

Provisional only; no team assignment is implied.

## 9. Consistent selection rubric (1–5 each)

Provisional discovery assessments, not rankings or experimental measurements. Reassess after full text and feasibility checks.

| Criterion | Score / 5 | Evidence |
| --- | --- | --- |
| Research quality and relevance | 5 | USENIX Security 2026, Cycle 1 (official list confirms); Network privacy of local AI agents |
| Implementation feasibility | 3 | One trace collection and replay-based defense simulation; local live pilot only if resources permit. Blockers: Trace availability/license, metric implementation and local evaluation model, novelty. |
| Novelty potential | 4 | Original mitigations may overlap; offline proxy may not establish live-agent protection. |
| Different from previous federated/continual/graph IDS | 5 | Problem: Network metadata from research agents can expose confidential task information despite encryption. |
| Meaningful AI for cybersecurity | 4 | AI creates the workload and leakage inference; proposed extension uses learning for protective decisions, not just analysis. |
| Technically justified modernity | 5 | LLM-based research agents and inference; proposed learned defensive policy |
| Public resources/reproducibility | 3 | https://github.com/umass-aisec/wra (linked research code; contents/license/run not verified in this pass); WRA traces from real search queries and synthetic personas; original trace download and license not checked |
| Measurable improvement | 5 | OBELS, trait recovery, task utility, mitigation overhead |
| Two complementary contributions | 5 | Trace processing, privacy metrics and leakage evaluation / Learned privacy controller and overhead/utility assessment |
| **Total** | **39/45** | Critical blockers outweigh totals. |

## 10. Final assessment

- **Strongest three reasons to shortlist:** Verified Cycle 1 paper; emerging AI/network intersection; defensive extension.
- **Three weaknesses or risks:** Trace access; original AI mainly workload/attack; live utility costs.
- **Unverified claims to investigate:** Trace availability/license, metric implementation and local evaluation model, novelty.; exact paper sections/tables, relevant licenses, compute and full related work.
- **Recommendation:** Conditional — discovery candidate only; no shortlisting decision.
- **One-sentence argument versus competing papers:** Distinct from network IDS and generic agent safety; complementary to Securitas.

## 11. Supporting references

- Primary paper: https://www.usenix.org/conference/usenixsecurity26/presentation/jeong
- Official venue/record: https://www.usenix.org/conference/usenixsecurity26/cycle1-accepted-papers
- Repository/benchmark: https://github.com/umass-aisec/wra (linked research code; contents/license/run not verified in this pass); WRA traces from real search queries and synthetic personas; original trace download and license not checked
- Closest related 2024–2026 work: Securitas https://www.usenix.org/conference/nsdi26/presentation/xie-guorui ; agent traffic privacy work review pending.

## Submission checklist

- [x] Bibliographic details verified from primary publication (venue/publisher or accepted listing; see specific caveats)
- [x] Author claims separated from personal hypotheses
- [ ] Actual figures/tables used for quantitative results
- [ ] Code, datasets, licenses and compute availability checked
- [ ] Research gap supported by evidence and related-work review
- [x] December 31 feasibility assessed (provisional)
- [x] Two-group contributions considered
- [x] Nine rubric scores justified (provisional)


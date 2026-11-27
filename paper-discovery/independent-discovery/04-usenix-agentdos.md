# Autonomy Comes with Costs: Detecting Denial-of-Service Vulnerabilities Caused by Resource Abusing in LLM-based Agents

> **Status:** Candidate reference — independent discovery review, 27 November 2026. No final project choice implied. Source metadata and abstract/previous discovery evidence are distinguished from proposed hypotheses. Full-text table/figure checks, licenses, reproduction and novelty review are incomplete unless explicitly noted.

## 1. Paper identification

| Field | Value |
| --- | --- |
| Submitted by | Independent discovery (AI-assisted; not attributed to a teammate) |
| Preference | Second |
| Assigned source/category | 2 — USENIX Security Cycle 1 |
| Authors | Jiaqi Luo, Jiarun Dai, Fengyu Liu, Songyang Peng, Youkun Shi, Tong Bu, Geng Hong, Xudong Pan, Yuan Zhang |
| Conference/journal | USENIX Security 2026 Cycle 1 |
| Publication/acceptance date | 2026 proceedings |
| Primary paper / DOI | https://www.usenix.org/conference/usenixsecurity26/presentation/luo |
| Source code URL + license | https://zenodo.org/records/18242998 (artifact access conditional/unverified; license not verified) |
| Dataset/benchmark URL + license | 20 open-source agent applications in paper; exact workloads and benchmark access not verified |
| Cybersecurity problem/domain | AI application resource security / service availability |
| AI techniques | LLM-assisted directed greybox fuzzing; proposed lightweight learned resource controller |

## 2. Problem and motivation

**Exact cybersecurity problem:** Agent resource lifecycle defects can cause service denial through excessive resource use.

**Why it matters:** Autonomous tool use can amplify a task's consumption of memory, compute or other resources.

**Prior research limitation:** Official abstract identifies insufficient resource governance and three lifecycle patterns.

## 3. Methodology

- **Core technical idea:** AgentDoS analyzes resource lifecycles and generates functionality-specific prompts to guide directed testing.
- **Input data:** Agent application and resource lifecycle observations
- **Output:** Validated resource-exhaustion findings
- **Main components / model / verification:** Lifecycle analysis, directed fuzzing, LLM seed generation, execution measurement
- **What AI contributes (and why):** LLM creates context-specific seeds; proposed defensive learning predicts when safe intervention is needed.
- **Architecture:** our conceptual schematic (not the authors' original figure):

```text
Local agent -> resource observations -> controller -> bounded execution -> utility measurement
```

## 4. Experimental evidence

| Item | Detail and source location |
| --- | --- |
| Datasets and size | 20 open-source agents (official abstract) |
| Baseline systems | Exact fuzzing comparators pending |
| Evaluation metrics | Validated defects, resource consumption, legitimate task completion |
| Exact numerical results | Official abstract: 36 previously unknown vulnerabilities affecting 16 agents; 15 CVE IDs assigned. Not independently reproduced; exact tables pending. |
| Hardware/compute | Original LLM costs not verified; proposed local controller CPU-feasible if fixed workloads are available. |
| Known threats to validity | Resource limits and workload fidelity; false interruption; test environments. |
| Reproduction status | Not attempted by our team |

Author-reported or previously surfaced numbers are not independent measurements. Statistical significance, table-level comparators and reproducibility are not established by this discovery review. Do not use provisional numerical claims in the final report until verified against the primary paper.

## 5. Candidate research gaps

| Gap | Evidence (section/page) | Author-acknowledged or our inference? | Possible overlap in 2024–2026 work |
| --- | --- | --- | --- |
| Adaptive resource governance | abstract motivates missing governance; proposed defensive extension; prior runtime control overlap unchecked. | Our inference / proposed question | Not systematically checked; see related-work targets below. |
| Task-preserving intervention | inferred; compare fixed quotas. | Our inference / proposed question | Not systematically checked; see related-work targets below. |
| Generalization across tools | inferred; benchmark diversity pending. | Our inference / proposed question | Not systematically checked; see related-work targets below. |

A perceived gap is **not established novelty** until independently checked.

## 6. Potential methodological improvements

- **Hypothesis A:** Train lightweight resource-budget allocation/intervention policy from controlled benign workloads.
- **Hypothesis B (alternative or complementary):** Measure safety and task utility versus fixed quota and timeout baselines.
- **Expected security/efficiency benefit:** Maintain service availability while avoiding premature termination.
- **Experiment and ablation plan:** Use mock/local agent workloads in isolated containers with strict caps; compare fixed limits and learned policy; evaluate benign completion, resource usage and intervention latency.
- **Risk of failure or overlap:** Not traditional network security; controller may be redundant with existing resource governance.

Do not finalize a project architecture at discovery stage.

## 7. Implementation feasibility by 2026-12-31

| Requirement | Assessment |
| --- | --- |
| Public code verified and actually tested? | https://zenodo.org/records/18242998 (artifact access conditional/unverified; license not verified); not executed. |
| Datasets available and legally usable? | 20 open-source agent applications in paper; exact workloads and benchmark access not verified; confirm terms before use. |
| Models/inference APIs available? | LLM-assisted directed greybox fuzzing; proposed lightweight learned resource controller; no paid APIs allowed; local feasibility not demonstrated. |
| Hardware, API cost, and development effort | Original LLM costs not verified; proposed local controller CPU-feasible if fixed workloads are available. |
| Realistic five-week minimum implementation | Two local agent workloads and one resource type; bounded test harness. |
| Features deliberately excluded | Full AgentDoS reproduction, paid APIs, public service tests. |
| Top blockers | Artifact access, local-agent setup, representative tasks, novelty. |
| Verdict | Conditional |

## 8. Two-group potential (7 members)

- **Group A (4 members) — possible independently measurable contribution:** Resource instrumentation and workload suite
- **Group B (3 members) — distinct but complementary contribution:** Controller and utility evaluation
- **How the contributions integrate:** Shared workload and resource telemetry
- **How each group demonstrates a result separately:** A reports resource profiles; B reports mitigation and completion

Provisional only; no team assignment is implied.

## 9. Consistent selection rubric (1–5 each)

Provisional discovery assessments, not rankings or experimental measurements. Reassess after full text and feasibility checks.

| Criterion | Score / 5 | Evidence |
| --- | --- | --- |
| Research quality and relevance | 5 | USENIX Security 2026 Cycle 1; AI application resource security / service availability |
| Implementation feasibility | 3 | Two local agent workloads and one resource type; bounded test harness. Blockers: Artifact access, local-agent setup, representative tasks, novelty. |
| Novelty potential | 3 | Not traditional network security; controller may be redundant with existing resource governance. |
| Different from previous federated/continual/graph IDS | 5 | Problem: Agent resource lifecycle defects can cause service denial through excessive resource use. |
| Meaningful AI for cybersecurity | 4 | LLM creates context-specific seeds; proposed defensive learning predicts when safe intervention is needed. |
| Technically justified modernity | 5 | LLM-assisted directed greybox fuzzing; proposed lightweight learned resource controller |
| Public resources/reproducibility | 2 | https://zenodo.org/records/18242998 (artifact access conditional/unverified; license not verified); 20 open-source agent applications in paper; exact workloads and benchmark access not verified |
| Measurable improvement | 4 | Validated defects, resource consumption, legitimate task completion |
| Two complementary contributions | 4 | Resource instrumentation and workload suite / Controller and utility evaluation |
| **Total** | **35/45** | Critical blockers outweigh totals. |

## 10. Final assessment

- **Strongest three reasons to shortlist:** Verified venue; real resource problem; runtime defensive extension.
- **Three weaknesses or risks:** Artifact restrictions; original costs unknown; domain fit.
- **Unverified claims to investigate:** Artifact access, local-agent setup, representative tasks, novelty.; exact paper sections/tables, relevant licenses, compute and full related work.
- **Recommendation:** Conditional — discovery candidate only; no shortlisting decision.
- **One-sentence argument versus competing papers:** Modern AI AppSec alternative, not a network-first candidate.

## 11. Supporting references

- Primary paper: https://www.usenix.org/conference/usenixsecurity26/presentation/luo
- Official venue/record: https://www.usenix.org/conference/usenixsecurity26/cycle1-accepted-papers
- Repository/benchmark: https://zenodo.org/records/18242998 (artifact access conditional/unverified; license not verified); 20 open-source agent applications in paper; exact workloads and benchmark access not verified
- Closest related 2024–2026 work: Agent sandboxing, resource governors and adaptive scheduling (review pending).

## Submission checklist

- [x] Bibliographic details verified from primary publication (venue/publisher or accepted listing; see specific caveats)
- [x] Author claims separated from personal hypotheses
- [ ] Actual figures/tables used for quantitative results
- [ ] Code, datasets, licenses and compute availability checked
- [ ] Research gap supported by evidence and related-work review
- [x] December 31 feasibility assessed (provisional)
- [x] Two-group contributions considered
- [x] Nine rubric scores justified (provisional)


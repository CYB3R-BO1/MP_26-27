# A Distributed Multi-Agent Deep Reinforcement Learning-Based Anti-Jamming Approach for Mega LEO Constellations

> **Status:** Candidate reference — independent discovery review, 27 November 2026. No final project choice implied. Source metadata and abstract/previous discovery evidence are distinguished from proposed hypotheses. Full-text table/figure checks, licenses, reproduction and novelty review are incomplete unless explicitly noted.

## 1. Paper identification

| Field | Value |
| --- | --- |
| Submitted by | Independent discovery (AI-assisted; not attributed to a teammate) |
| Preference | Second |
| Assigned source/category | 6 — IEEE TIFS |
| Authors | Wei Li, Kexin Chen, Xiao-Lu Liu, Luliang Jia, Jian Wu, Quan Chen, Wenting Cao (DBLP record) |
| Conference/journal | IEEE Transactions on Information Forensics and Security, vol. 21 (2026) |
| Publication/acceptance date | 2026 publication; exact user-linked collection membership unverified |
| Primary paper / DOI | https://ieeexplore.ieee.org/abstract/document/11447302 ; https://doi.org/10.1109/TIFS.2026.3675852 |
| Source code URL + license | Not found/verified |
| Dataset/benchmark URL + license | Satellite-network simulation; parameters and artifacts not verified |
| Cybersecurity problem/domain | Wireless network security and anti-jamming |
| AI techniques | Distributed multi-agent deep RL, local interaction Markov game |

## 2. Problem and motivation

**Exact cybersecurity problem:** Maintain communications under interference in resource-constrained satellite networks.

**Why it matters:** Reliable communication requires adaptive choices without expensive coordination.

**Prior research limitation:** Publisher abstract describes anti-jamming challenge and offline training/online execution; section details pending.

## 3. Methodology

- **Core technical idea:** Train distributed agents offline and execute decentralized defensive policies online.
- **Input data:** Local communication environment observations (exact features pending)
- **Output:** Adaptive communication decisions (exact action space pending)
- **Main components / model / verification:** Local interaction Markov game, distributed deep RL, offline training/online execution
- **What AI contributes (and why):** Agents learn defensive decisions under network uncertainty rather than predict attack labels.
- **Architecture:** our conceptual schematic (not the authors' original figure):

```text
Simulated nodes -> local RL policies -> communication decisions -> reliability feedback
```

## 4. Experimental evidence

| Item | Detail and source location |
| --- | --- |
| Datasets and size | Simulation; original configurations not verified |
| Baseline systems | Not verified |
| Evaluation metrics | Communication reliability, throughput and coordination overhead (proposed; exact original metrics pending) |
| Exact numerical results | Publisher abstract describes convergence/asymptotic optimality analysis; no numeric results verified. |
| Hardware/compute | Simulation avoids real satellites; original training budget unknown. |
| Known threats to validity | Simulation realism, interference assumptions, transfer to real systems, reward design. |
| Reproduction status | Not attempted by our team |

Author-reported or previously surfaced numbers are not independent measurements. Statistical significance, table-level comparators and reproducibility are not established by this discovery review. Do not use provisional numerical claims in the final report until verified against the primary paper.

## 5. Candidate research gaps

| Gap | Evidence (section/page) | Author-acknowledged or our inference? | Possible overlap in 2024–2026 work |
| --- | --- | --- | --- |
| Communication-constrained coordination | inferred; compare decentralized MARL. | Our inference / proposed question | Not systematically checked; see related-work targets below. |
| Lightweight policy execution | inferred; original may already cover. | Our inference / proposed question | Not systematically checked; see related-work targets below. |
| Generalization across interference conditions | inferred; related work review pending. | Our inference / proposed question | Not systematically checked; see related-work targets below. |

A perceived gap is **not established novelty** until independently checked.

## 6. Potential methodological improvements

- **Hypothesis A:** Evaluate a small decentralized policy in a simplified local simulator.
- **Hypothesis B (alternative or complementary):** Study coordination budget versus reliability and recovery.
- **Expected security/efficiency benefit:** Reliable communication under simulated interference with reduced coordination overhead.
- **Experiment and ablation plan:** Verify original simulator/model first; compare simple non-learning and MARL baselines on fixed synthetic scenarios; ablate observation and coordination.
- **Risk of failure or overlap:** Satellite/wireless domain learning curve; original code unavailable; may not fit AppSec goals.

Do not finalize a project architecture at discovery stage.

## 7. Implementation feasibility by 2026-12-31

| Requirement | Assessment |
| --- | --- |
| Public code verified and actually tested? | Not found/verified; not executed. |
| Datasets available and legally usable? | Satellite-network simulation; parameters and artifacts not verified; confirm terms before use. |
| Models/inference APIs available? | Distributed multi-agent deep RL, local interaction Markov game; no paid APIs allowed; local feasibility not demonstrated. |
| Hardware, API cost, and development effort | Simulation avoids real satellites; original training budget unknown. |
| Realistic five-week minimum implementation | Small generic simulation if original methodology can be reproduced. |
| Features deliberately excluded | Real radio transmissions, satellite hardware, full-scale constellation. |
| Top blockers | Exact collection, full text, simulator, compute, communications expertise. |
| Verdict | Conditional |

## 8. Two-group potential (7 members)

- **Group A (4 members) — possible independently measurable contribution:** Simulator and distributed policy
- **Group B (3 members) — distinct but complementary contribution:** Coordination and robustness evaluation
- **How the contributions integrate:** Shared local observation model
- **How each group demonstrates a result separately:** A reports reliability; B reports coordination cost

Provisional only; no team assignment is implied.

## 9. Consistent selection rubric (1–5 each)

Provisional discovery assessments, not rankings or experimental measurements. Reassess after full text and feasibility checks.

| Criterion | Score / 5 | Evidence |
| --- | --- | --- |
| Research quality and relevance | 4 | IEEE Transactions on Information Forensics and Security, vol. 21 (2026); Wireless network security and anti-jamming |
| Implementation feasibility | 2 | Small generic simulation if original methodology can be reproduced. Blockers: Exact collection, full text, simulator, compute, communications expertise. |
| Novelty potential | 3 | Satellite/wireless domain learning curve; original code unavailable; may not fit AppSec goals. |
| Different from previous federated/continual/graph IDS | 5 | Problem: Maintain communications under interference in resource-constrained satellite networks. |
| Meaningful AI for cybersecurity | 5 | Agents learn defensive decisions under network uncertainty rather than predict attack labels. |
| Technically justified modernity | 4 | Distributed multi-agent deep RL, local interaction Markov game |
| Public resources/reproducibility | 2 | Not found/verified; Satellite-network simulation; parameters and artifacts not verified |
| Measurable improvement | 4 | Communication reliability, throughput and coordination overhead (proposed; exact original metrics pending) |
| Two complementary contributions | 4 | Simulator and distributed policy / Coordination and robustness evaluation |
| **Total** | **33/45** | Critical blockers outweigh totals. |

## 10. Final assessment

- **Strongest three reasons to shortlist:** Established journal; meaningful MARL; active protection.
- **Three weaknesses or risks:** Specialized wireless domain; no verified code; original compute unknown.
- **Unverified claims to investigate:** Exact collection, full text, simulator, compute, communications expertise.; exact paper sections/tables, relevant licenses, compute and full related work.
- **Recommendation:** Conditional — discovery candidate only; no shortlisting decision.
- **One-sentence argument versus competing papers:** More active defense than UTFormer, but higher implementation uncertainty.

## 11. Supporting references

- Primary paper: https://ieeexplore.ieee.org/abstract/document/11447302 ; https://doi.org/10.1109/TIFS.2026.3675852
- Official venue/record: https://dblp.org/db/journals/tifs/tifs21.html ; https://ieeexplore.ieee.org/xpl/tocresult.jsp?isnumber=11313711&punumber=10206
- Repository/benchmark: Not found/verified; Satellite-network simulation; parameters and artifacts not verified
- Closest related 2024–2026 work: Decentralized MARL for spectrum access and anti-jamming (review pending).

## Submission checklist

- [x] Bibliographic details verified from primary publication (venue/publisher or accepted listing; see specific caveats)
- [x] Author claims separated from personal hypotheses
- [ ] Actual figures/tables used for quantitative results
- [ ] Code, datasets, licenses and compute availability checked
- [ ] Research gap supported by evidence and related-work review
- [x] December 31 feasibility assessed (provisional)
- [x] Two-group contributions considered
- [x] Nine rubric scores justified (provisional)


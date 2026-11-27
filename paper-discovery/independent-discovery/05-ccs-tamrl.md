# Less Effort, Shorter Proofs: Reinforcement Learning for Security Protocol Analysis in Tamarin

> **Status:** Candidate reference — independent discovery review, 27 November 2026. No final project choice implied. Source metadata and abstract/previous discovery evidence are distinguished from proposed hypotheses. Full-text table/figure checks, licenses, reproduction and novelty review are incomplete unless explicitly noted.

## 1. Paper identification

| Field | Value |
| --- | --- |
| Submitted by | Independent discovery (AI-assisted; not attributed to a teammate) |
| Preference | First |
| Assigned source/category | 3 — ACM CCS |
| Authors | Matthias Cosler, Cas Cremers, Bernd Finkbeiner, Mohamed Ghanem, Niklas Medinger |
| Conference/journal | ACM CCS 2026 (accepted listing) |
| Publication/acceptance date | 2026; preprint 22 May 2026 |
| Primary paper / DOI | https://arxiv.org/abs/2605.23643 |
| Source code URL + license | https://github.com/MatCos/TamRL ; https://github.com/niklasmedinger/Tamarin-ML-API (license and execution pending) |
| Dataset/benchmark URL + license | https://zenodo.org/records/22819846 (artifact data; protocol models and checkpoints documented; download/license pending) |
| Cybersecurity problem/domain | Formal security verification of network protocols |
| AI techniques | RL, neural heuristic, Monte Carlo tree search |

## 2. Problem and motivation

**Exact cybersecurity problem:** Automated security protocol proofs can require expensive search and substantial manual heuristics.

**Why it matters:** Checkable proofs and counterexamples support secure authentication and communication protocol design.

**Prior research limitation:** Preprint abstract describes human effort and time in automated protocol verification.

## 3. Methodology

- **Core technical idea:** Learn proof-search heuristics from completed subproofs through an RL interface to Tamarin.
- **Input data:** Tamarin protocol models and proof states
- **Output:** Independently checkable proof scripts / verification results
- **Main components / model / verification:** Stateless Tamarin API, MCTS, neural heuristic and proof verifier
- **What AI contributes (and why):** Learns which search choices improve verification efficiency; correctness remains checked by Tamarin.
- **Architecture:** our conceptual schematic (not the authors' original figure):

```text
Protocol model -> RL-guided MCTS -> proof candidate -> Tamarin validation
```

## 4. Experimental evidence

| Item | Detail and source location |
| --- | --- |
| Datasets and size | 16 protocol case studies (preprint abstract); artifact includes models |
| Baseline systems | Tamarin standard search and human-engineered heuristics |
| Evaluation metrics | Automatically solved lemmas, proof length, wall-clock time, memory |
| Exact numerical results | Abstract reports more automatically solved proofs than standard search and shorter proofs than standard and human-engineered heuristics; exact per-case tables pending. Repository documents four YubikeyHSM lemmas in under five minutes on CPU (demo claim, not own run). |
| Hardware/compute | CPU demo documented; full training multiple GPU-days per prior discovery, precise hardware and schedule pending. |
| Known threats to validity | Model fidelity, proof selection bias, hardware-dependent runtime, benchmark leakage. |
| Reproduction status | Not attempted by our team |

Author-reported or previously surfaced numbers are not independent measurements. Statistical significance, table-level comparators and reproducibility are not established by this discovery review. Do not use provisional numerical claims in the final report until verified against the primary paper.

## 5. Candidate research gaps

| Gap | Evidence (section/page) | Author-acknowledged or our inference? | Possible overlap in 2024–2026 work |
| --- | --- | --- | --- |
| Budget-aware search | inferred from proof-search cost; check related learned search work. | Our inference / proposed question | Not systematically checked; see related-work targets below. |
| Cross-protocol generalization | inferred; verify training/test partition and existing results. | Our inference / proposed question | Not systematically checked; see related-work targets below. |
| Lightweight heuristic or search allocation | inferred; avoid merely tuning existing parameters. | Our inference / proposed question | Not systematically checked; see related-work targets below. |

A perceived gap is **not established novelty** until independently checked.

## 6. Potential methodological improvements

- **Hypothesis A:** Compare a lightweight heuristic or budget-conditioned policy with released and standard Tamarin heuristics.
- **Hypothesis B (alternative or complementary):** Study adaptive allocation of verification time across held-out lemmas.
- **Expected security/efficiency benefit:** More verified properties within fixed wall-clock/memory budgets.
- **Experiment and ablation plan:** Run documented CPU smoke test; freeze a small protocol/lemma split; compare standard heuristic, released policy, simple heuristic and proposed method at fixed budgets; ablate budget features; independently check all proofs.
- **Risk of failure or overlap:** Formal methods learning curve; existing TamRL may already address extension; retraining too expensive.

Do not finalize a project architecture at discovery stage.

## 7. Implementation feasibility by 2026-12-31

| Requirement | Assessment |
| --- | --- |
| Public code verified and actually tested? | https://github.com/MatCos/TamRL ; https://github.com/niklasmedinger/Tamarin-ML-API (license and execution pending); not executed. |
| Datasets available and legally usable? | https://zenodo.org/records/22819846 (artifact data; protocol models and checkpoints documented; download/license pending); confirm terms before use. |
| Models/inference APIs available? | RL, neural heuristic, Monte Carlo tree search; no paid APIs allowed; local feasibility not demonstrated. |
| Hardware, API cost, and development effort | CPU demo documented; full training multiple GPU-days per prior discovery, precise hardware and schedule pending. |
| Realistic five-week minimum implementation | CPU example plus a few protocol models, released policy and modest search-controller experiment. |
| Features deliberately excluded | Full original GPU training; creating entire new prover; real protocol implementation audits. |
| Top blockers | Tamarin/API dependencies, artifact weights, learning curve, novelty and team hardware. |
| Verdict | Conditional |

## 8. Two-group potential (7 members)

- **Group A (4 members) — possible independently measurable contribution:** Learned heuristic/search method and baseline
- **Group B (3 members) — distinct but complementary contribution:** Budget allocation and held-out protocol evaluation
- **How the contributions integrate:** Common Tamarin API and proof validation
- **How each group demonstrates a result separately:** A reports proof success/length; B reports resource efficiency and transfer

Provisional only; no team assignment is implied.

## 9. Consistent selection rubric (1–5 each)

Provisional discovery assessments, not rankings or experimental measurements. Reassess after full text and feasibility checks.

| Criterion | Score / 5 | Evidence |
| --- | --- | --- |
| Research quality and relevance | 5 | ACM CCS 2026 (accepted listing); Formal security verification of network protocols |
| Implementation feasibility | 4 | CPU example plus a few protocol models, released policy and modest search-controller experiment. Blockers: Tamarin/API dependencies, artifact weights, learning curve, novelty and team hardware. |
| Novelty potential | 4 | Formal methods learning curve; existing TamRL may already address extension; retraining too expensive. |
| Different from previous federated/continual/graph IDS | 5 | Problem: Automated security protocol proofs can require expensive search and substantial manual heuristics. |
| Meaningful AI for cybersecurity | 5 | Learns which search choices improve verification efficiency; correctness remains checked by Tamarin. |
| Technically justified modernity | 5 | RL, neural heuristic, Monte Carlo tree search |
| Public resources/reproducibility | 4 | https://github.com/MatCos/TamRL ; https://github.com/niklasmedinger/Tamarin-ML-API (license and execution pending); https://zenodo.org/records/22819846 (artifact data; protocol models and checkpoints documented; download/license pending) |
| Measurable improvement | 5 | Automatically solved lemmas, proof length, wall-clock time, memory |
| Two complementary contributions | 5 | Learned heuristic/search method and baseline / Budget allocation and held-out protocol evaluation |
| **Total** | **42/45** | Critical blockers outweigh totals. |

## 10. Final assessment

- **Strongest three reasons to shortlist:** Verified venue; checkable outcomes; documented CPU demonstration.
- **Three weaknesses or risks:** Formal methods expertise; original training cost; extension novelty.
- **Unverified claims to investigate:** Tamarin/API dependencies, artifact weights, learning curve, novelty and team hardware.; exact paper sections/tables, relevant licenses, compute and full related work.
- **Recommendation:** Conditional — discovery candidate only; no shortlisting decision.
- **One-sentence argument versus competing papers:** Stronger network fit and lower paid inference dependency than MirrorGuard or PBFuzz.

## 11. Supporting references

- Primary paper: https://arxiv.org/abs/2605.23643
- Official venue/record: https://www.sigsac.org/ccs/CCS2026/program/accepted-papers.html
- Repository/benchmark: https://github.com/MatCos/TamRL ; https://github.com/niklasmedinger/Tamarin-ML-API (license and execution pending); https://zenodo.org/records/22819846 (artifact data; protocol models and checkpoints documented; download/license pending)
- Closest related 2024–2026 work: Tamarin https://tamarin-prover.com/ ; ProtocolGuard (NDSS 2026); learned theorem proving review pending.

## Submission checklist

- [x] Bibliographic details verified from primary publication (venue/publisher or accepted listing; see specific caveats)
- [x] Author claims separated from personal hypotheses
- [ ] Actual figures/tables used for quantitative results
- [ ] Code, datasets, licenses and compute availability checked
- [ ] Research gap supported by evidence and related-work review
- [x] December 31 feasibility assessed (provisional)
- [x] Two-group contributions considered
- [x] Nine rubric scores justified (provisional)


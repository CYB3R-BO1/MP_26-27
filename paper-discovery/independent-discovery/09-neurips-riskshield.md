# Safe Actions Can Form Unsafe Traces: Benchmarking and Shielding Compositional Emergent Risk in AI Agents

> **Status:** Candidate reference — independent discovery review, 27 November 2026. No final project choice implied. Source metadata and abstract/previous discovery evidence are distinguished from proposed hypotheses. Full-text table/figure checks, licenses, reproduction and novelty review are incomplete unless explicitly noted.

## 1. Paper identification

| Field | Value |
| --- | --- |
| Submitted by | Independent discovery (AI-assisted; not attributed to a teammate) |
| Preference | First |
| Assigned source/category | 5 — NeurIPS |
| Authors | Complete author list not verified; Xiu Su and Zhongze Wu author pages list the work |
| Conference/journal | NeurIPS 2026 listing/author records; final proceedings entry pending |
| Publication/acceptance date | 2026 accepted/listed; publication date not verified |
| Primary paper / DOI | https://acceptodds.com/papers/neurips2026-153882 (secondary mirror; primary final paper not retrieved) |
| Source code URL + license | https://anonymous.4open.science/r/RiskShield-2284 (anonymous link; access/license/run not verified) |
| Dataset/benchmark URL + license | CER-Bench synthetic traces; exact download and license not verified |
| Cybersecurity problem/domain | AI-agent runtime execution security |
| AI techniques | Sequential risk reasoning and trace-level shielding |

## 2. Problem and motivation

**Exact cybersecurity problem:** Sequences of individually acceptable actions can violate security constraints when combined.

**Why it matters:** A per-call monitor may miss cumulative effects in agentic applications.

**Prior research limitation:** Retrieved mirror describes compositionality gap and trace-level intervention; original full text/sections unverified.

## 3. Methodology

- **Core technical idea:** Benchmark compositional risk in stateful execution traces and shield unsafe sequences.
- **Input data:** Agent action history and execution state
- **Output:** Trace-level intervention / risk decision
- **Main components / model / verification:** CER-Bench, RiskShield, stateful trace evaluation
- **What AI contributes (and why):** Reasoning over action history rather than isolated inputs; local learned monitor proposed.
- **Architecture:** our conceptual schematic (not the authors' original figure):

```text
Action trace -> learned cumulative-risk monitor -> safe intervention -> task outcome
```

## 4. Experimental evidence

| Item | Detail and source location |
| --- | --- |
| Datasets and size | CER-Bench synthetic tasks; OS-Harm evaluation referenced by mirror |
| Baseline systems | R-Judge, ToolEmu, AgentHarm, ToolShield and other trace/action approaches mentioned in mirror; exact experiment comparators pending |
| Evaluation metrics | Unsafe trace rate, benign completion, intervention cost |
| Exact numerical results | Prior discovery noted 440 tasks and 19,525 actions; primary table/figure not retrieved; do not use as verified results. Mirror mentions 175 OS-Harm trajectories; exact experimental context pending. |
| Hardware/compute | Original evaluation includes frontier agents; offline small-model training may be feasible, but unverified. |
| Known threats to validity | Synthetic-to-real transfer, label quality, incomplete action state, overlap with generic safety. |
| Reproduction status | Not attempted by our team |

Author-reported or previously surfaced numbers are not independent measurements. Statistical significance, table-level comparators and reproducibility are not established by this discovery review. Do not use provisional numerical claims in the final report until verified against the primary paper.

## 5. Candidate research gaps

| Gap | Evidence (section/page) | Author-acknowledged or our inference? | Possible overlap in 2024–2026 work |
| --- | --- | --- | --- |
| Network tool-call sequences | inferred; not established original gap. | Our inference / proposed question | Not systematically checked; see related-work targets below. |
| Lightweight temporal monitor | inferred; compare existing trace shields. | Our inference / proposed question | Not systematically checked; see related-work targets below. |
| Local benchmark transfer | inferred; test held-out workflows. | Our inference / proposed question | Not systematically checked; see related-work targets below. |

A perceived gap is **not established novelty** until independently checked.

## 6. Potential methodological improvements

- **Hypothesis A:** Study a small learned stateful monitor for cumulative security consequences on local traces.
- **Hypothesis B (alternative or complementary):** Evaluate intervention policy versus action-only monitor in a controlled tool environment.
- **Expected security/efficiency benefit:** Fewer unsafe sequences without blocking valid workflows.
- **Experiment and ablation plan:** Obtain legal trace benchmark; compare action-only, rule/state baseline and learned temporal model; hold out task families; measure intervention and completion.
- **Risk of failure or overlap:** Safety vs cybersecurity boundary; primary and artifact not verified; novelty uncertain.

Do not finalize a project architecture at discovery stage.

## 7. Implementation feasibility by 2026-12-31

| Requirement | Assessment |
| --- | --- |
| Public code verified and actually tested? | https://anonymous.4open.science/r/RiskShield-2284 (anonymous link; access/license/run not verified); not executed. |
| Datasets available and legally usable? | CER-Bench synthetic traces; exact download and license not verified; confirm terms before use. |
| Models/inference APIs available? | Sequential risk reasoning and trace-level shielding; no paid APIs allowed; local feasibility not demonstrated. |
| Hardware, API cost, and development effort | Original evaluation includes frontier agents; offline small-model training may be feasible, but unverified. |
| Realistic five-week minimum implementation | Offline trace-based prototype only; local mock tools. |
| Features deliberately excluded | Paid inference, GUI-scale agent evaluation, generic AI safety. |
| Top blockers | Primary paper/author verification, artifact, licenses, labels and model requirements. |
| Verdict | Conditional |

## 8. Two-group potential (7 members)

- **Group A (4 members) — possible independently measurable contribution:** Trace benchmark and sequence representation
- **Group B (3 members) — distinct but complementary contribution:** Monitor and intervention evaluation
- **How the contributions integrate:** Common trace and security outcome labels
- **How each group demonstrates a result separately:** A reports generalization; B reports safety/utility tradeoff

Provisional only; no team assignment is implied.

## 9. Consistent selection rubric (1–5 each)

Provisional discovery assessments, not rankings or experimental measurements. Reassess after full text and feasibility checks.

| Criterion | Score / 5 | Evidence |
| --- | --- | --- |
| Research quality and relevance | 3 | NeurIPS 2026 listing/author records; final proceedings entry pending; AI-agent runtime execution security |
| Implementation feasibility | 3 | Offline trace-based prototype only; local mock tools. Blockers: Primary paper/author verification, artifact, licenses, labels and model requirements. |
| Novelty potential | 3 | Safety vs cybersecurity boundary; primary and artifact not verified; novelty uncertain. |
| Different from previous federated/continual/graph IDS | 5 | Problem: Sequences of individually acceptable actions can violate security constraints when combined. |
| Meaningful AI for cybersecurity | 4 | Reasoning over action history rather than isolated inputs; local learned monitor proposed. |
| Technically justified modernity | 5 | Sequential risk reasoning and trace-level shielding |
| Public resources/reproducibility | 2 | https://anonymous.4open.science/r/RiskShield-2284 (anonymous link; access/license/run not verified); CER-Bench synthetic traces; exact download and license not verified |
| Measurable improvement | 4 | Unsafe trace rate, benign completion, intervention cost |
| Two complementary contributions | 4 | Trace benchmark and sequence representation / Monitor and intervention evaluation |
| **Total** | **33/45** | Critical blockers outweigh totals. |

## 10. Final assessment

- **Strongest three reasons to shortlist:** Modern agent problem; stateful reasoning; measurable utility.
- **Three weaknesses or risks:** Primary artifact not verified; synthetic data; network fit limited.
- **Unverified claims to investigate:** Primary paper/author verification, artifact, licenses, labels and model requirements.; exact paper sections/tables, relevant licenses, compute and full related work.
- **Recommendation:** Conditional — discovery candidate only; no shortlisting decision.
- **One-sentence argument versus competing papers:** More sequence-focused than MirrorGuard; not yet a verified project foundation.

## 11. Supporting references

- Primary paper: https://acceptodds.com/papers/neurips2026-153882 (secondary mirror; primary final paper not retrieved)
- Official venue/record: https://dev.neurips.cc/Downloads/2026 ; https://xiusu.github.io/
- Repository/benchmark: https://anonymous.4open.science/r/RiskShield-2284 (anonymous link; access/license/run not verified); CER-Bench synthetic traces; exact download and license not verified
- Closest related 2024–2026 work: AgentHarm, OS-Harm, ToolShield (primary records and overlap review pending).

## Submission checklist

- [ ] Bibliographic details verified from primary publication (venue/publisher or accepted listing; see specific caveats)
- [x] Author claims separated from personal hypotheses
- [ ] Actual figures/tables used for quantitative results
- [ ] Code, datasets, licenses and compute availability checked
- [ ] Research gap supported by evidence and related-work review
- [x] December 31 feasibility assessed (provisional)
- [x] Two-group contributions considered
- [x] Nine rubric scores justified (provisional)


# Specializing Language Models for Textual Fuzzing via Reinforcement Learning

> **Status:** Candidate reference — independent discovery review, 27 November 2026. No final project choice implied. Source metadata and abstract/previous discovery evidence are distinguished from proposed hypotheses. Full-text table/figure checks, licenses, reproduction and novelty review are incomplete unless explicitly noted.

## 1. Paper identification

| Field | Value |
| --- | --- |
| Submitted by | Independent discovery (AI-assisted; not attributed to a teammate) |
| Preference | Second |
| Assigned source/category | 1 — IEEE S&P |
| Authors | Jiayi Lin, Liangcai Su, Junzhe Li, Chenxiong Qian |
| Conference/journal | IEEE S&P 2026 (preprint title adds R1-Fuzz) |
| Publication/acceptance date | 2026 proceedings; preprint September 2025 |
| Primary paper / DOI | https://ieeexplore.ieee.org/abstract/document/11573566 ; https://arxiv.org/abs/2509.20384 |
| Source code URL + license | https://github.com/HKU-System-Security-Lab/R1-Fuzz ; https://huggingface.co/0gal1/R1-Fuzz-7B (licenses and runnable setup not verified) |
| Dataset/benchmark URL + license | Textual fuzzing targets and training data described in preprint; exact downloads/licenses pending |
| Cybersecurity problem/domain | Software testing and text protocol security (extension) |
| AI techniques | RL post-training, Qwen2.5-7B, coverage feedback |

## 2. Problem and motivation

**Exact cybersecurity problem:** Textual fuzzing struggles to produce inputs that exercise deep program logic.

**Why it matters:** Useful inputs must satisfy syntax and semantic constraints; coverage-guided testing benefits from informed generation.

**Prior research limitation:** Preprint abstract and introduction identify shallow exploration and cost of larger LMs.

## 3. Methodology

- **Core technical idea:** Specialize a small language model using coverage-derived questions and distance-based rewards; use it within fuzzing.
- **Input data:** Program coverage information and textual test-generation tasks
- **Output:** Candidate textual inputs for a local test harness
- **Main components / model / verification:** Coverage slicing, reward construction, RL post-training, fuzzing workflow
- **What AI contributes (and why):** Learns useful input generation rather than relying only on generic prompting.
- **Architecture:** our conceptual schematic (not the authors' original figure):

```text
Coverage feedback -> specialized local LM -> input -> test harness -> coverage
```

## 4. Experimental evidence

| Item | Detail and source location |
| --- | --- |
| Datasets and size | Real-world compilers/interpreters/database engines; exact benchmark sizes pending |
| Baseline systems | State-of-the-art fuzzers and larger LMs; table-level comparators pending |
| Evaluation metrics | Coverage, confirmed bugs, time and compute |
| Exact numerical results | Preprint abstract reports up to 75% higher coverage and 29 previously unknown vulnerabilities; per-target comparators/table not checked. |
| Hardware/compute | Released 7B model; full RL training not feasible; quantized inference feasibility depends on hardware. |
| Known threats to validity | Target-specific buildability, model leakage, coverage not equivalent to security impact. |
| Reproduction status | Not attempted by our team |

Author-reported or previously surfaced numbers are not independent measurements. Statistical significance, table-level comparators and reproducibility are not established by this discovery review. Do not use provisional numerical claims in the final report until verified against the primary paper.

## 5. Candidate research gaps

| Gap | Evidence (section/page) | Author-acknowledged or our inference? | Possible overlap in 2024–2026 work |
| --- | --- | --- | --- |
| Resource-aware generation scheduling | cost motivation in abstract; inferred extension; hybrid fuzzing overlap unchecked. | Our inference / proposed question | Not systematically checked; see related-work targets below. |
| Transfer to text protocol workloads | original targets textual software; inferred; protocol fuzzing literature unchecked. | Our inference / proposed question | Not systematically checked; see related-work targets below. |
| Small-model efficiency | preprint cost motivation; inferred; quantization impact unverified. | Our inference / proposed question | Not systematically checked; see related-work targets below. |

A perceived gap is **not established novelty** until independently checked.

## 6. Potential methodological improvements

- **Hypothesis A:** Evaluate released model on a small authorized local text-protocol benchmark without retraining.
- **Hypothesis B (alternative or complementary):** Test a feedback-based invocation scheduler at fixed inference budgets.
- **Expected security/efficiency benefit:** Coverage and validated test yield per unit compute.
- **Experiment and ablation plan:** Compare conventional local fuzzing, fixed-frequency model invocation and adaptive scheduling on isolated test programs; compare coverage and time, ablate scheduling.
- **Risk of failure or overlap:** PBFuzz and other hybrid fuzzers overlap; local model quality and cost uncertain.

Do not finalize a project architecture at discovery stage.

## 7. Implementation feasibility by 2026-12-31

| Requirement | Assessment |
| --- | --- |
| Public code verified and actually tested? | https://github.com/HKU-System-Security-Lab/R1-Fuzz ; https://huggingface.co/0gal1/R1-Fuzz-7B (licenses and runnable setup not verified); not executed. |
| Datasets available and legally usable? | Textual fuzzing targets and training data described in preprint; exact downloads/licenses pending; confirm terms before use. |
| Models/inference APIs available? | RL post-training, Qwen2.5-7B, coverage feedback; no paid APIs allowed; local feasibility not demonstrated. |
| Hardware, API cost, and development effort | Released 7B model; full RL training not feasible; quantized inference feasibility depends on hardware. |
| Realistic five-week minimum implementation | One or two local test targets; prebuilt weights only. |
| Features deliberately excluded | Full RL training, binary reverse engineering, real third-party targets. |
| Top blockers | Model download/license, hardware, target builds, novelty. |
| Verdict | Conditional |

## 8. Two-group potential (7 members)

- **Group A (4 members) — possible independently measurable contribution:** Local fuzzing harness and baseline
- **Group B (3 members) — distinct but complementary contribution:** Inference scheduling and cost evaluation
- **How the contributions integrate:** Shared coverage feedback and time budget
- **How each group demonstrates a result separately:** A reports coverage and reproducibility; B reports efficiency

Provisional only; no team assignment is implied.

## 9. Consistent selection rubric (1–5 each)

Provisional discovery assessments, not rankings or experimental measurements. Reassess after full text and feasibility checks.

| Criterion | Score / 5 | Evidence |
| --- | --- | --- |
| Research quality and relevance | 5 | IEEE S&P 2026 (preprint title adds R1-Fuzz); Software testing and text protocol security (extension) |
| Implementation feasibility | 2 | One or two local test targets; prebuilt weights only. Blockers: Model download/license, hardware, target builds, novelty. |
| Novelty potential | 3 | PBFuzz and other hybrid fuzzers overlap; local model quality and cost uncertain. |
| Different from previous federated/continual/graph IDS | 5 | Problem: Textual fuzzing struggles to produce inputs that exercise deep program logic. |
| Meaningful AI for cybersecurity | 5 | Learns useful input generation rather than relying only on generic prompting. |
| Technically justified modernity | 5 | RL post-training, Qwen2.5-7B, coverage feedback |
| Public resources/reproducibility | 3 | https://github.com/HKU-System-Security-Lab/R1-Fuzz ; https://huggingface.co/0gal1/R1-Fuzz-7B (licenses and runnable setup not verified); Textual fuzzing targets and training data described in preprint; exact downloads/licenses pending |
| Measurable improvement | 4 | Coverage, confirmed bugs, time and compute |
| Two complementary contributions | 4 | Local fuzzing harness and baseline / Inference scheduling and cost evaluation |
| **Total** | **36/45** | Critical blockers outweigh totals. |

## 10. Final assessment

- **Strongest three reasons to shortlist:** Verified conference; genuine learning; released model link.
- **Three weaknesses or risks:** 7B inference; builds; not primarily network security.
- **Unverified claims to investigate:** Model download/license, hardware, target builds, novelty.; exact paper sections/tables, relevant licenses, compute and full related work.
- **Recommendation:** Conditional — discovery candidate only; no shortlisting decision.
- **One-sentence argument versus competing papers:** Narrower than Incalmo, but zero-paid inference must be demonstrated.

## 11. Supporting references

- Primary paper: https://ieeexplore.ieee.org/abstract/document/11573566 ; https://arxiv.org/abs/2509.20384
- Official venue/record: https://sp2026.ieee-security.org/accepted-papers.html
- Repository/benchmark: https://github.com/HKU-System-Security-Lab/R1-Fuzz ; https://huggingface.co/0gal1/R1-Fuzz-7B (licenses and runnable setup not verified); Textual fuzzing targets and training data described in preprint; exact downloads/licenses pending
- Closest related 2024–2026 work: PBFuzz https://arxiv.org/abs/2512.04611 ; hybrid LLM fuzzing review pending.

## Submission checklist

- [x] Bibliographic details verified from primary publication (venue/publisher or accepted listing; see specific caveats)
- [x] Author claims separated from personal hypotheses
- [ ] Actual figures/tables used for quantitative results
- [ ] Code, datasets, licenses and compute availability checked
- [ ] Research gap supported by evidence and related-work review
- [x] December 31 feasibility assessed (provisional)
- [x] Two-group contributions considered
- [x] Nine rubric scores justified (provisional)


# PBFuzz: Agentic Directed Fuzzing for PoV Generation

> **Status:** Candidate reference — second preference, not a finalized project. arXiv preprint is dated 4 December 2025; Zenodo artifact record states acceptance to ACM CCS 2026 on 5 June 2026. Reproduction has not been attempted.

## 1. Paper identification

| Field | Value |
| --- | --- |
| Submitted by | Umesh Chandra |
| Preference | Second |
| Source/category | ACM CCS 2026 |
| Authors | Haochen Zeng, Andrew Bao, Jiajun Cheng, Chengyu Song |
| Venue | ACM CCS 2026 |
| Date | arXiv preprint 4 December 2025; Zenodo artifact record says accepted 5 June 2026 |
| Primary paper | https://arxiv.org/abs/2512.04611 |
| Code/license | https://github.com/sgzeng/pbfuzz — current repository declares PolyForm Noncommercial 1.0.0; check exact commit/version and comply with terms |
| Artifact | https://zenodo.org/records/20770567 |
| Benchmark | https://github.com/HexHive/magma ; target-project licenses must be checked individually |
| Domain | Software vulnerability discovery, directed fuzzing, proof-of-vulnerability (PoV) generation |
| AI techniques | LLM agentic code reasoning, semantic constraint extraction, persistent campaign memory, property-based input generation, execution/debugging feedback |

## 2. Problem and motivation

**Problem:** A PoV input must both reach vulnerable code and satisfy the conditions that trigger the bug. Directed greybox fuzzers can guide execution toward a target but may fail to satisfy semantic triggering conditions. One-shot LLM input generation can produce plausible inputs but often fails on complex vulnerabilities.

**Why it matters:** Reproducible PoVs help confirm static-analysis alerts, reproduce bugs, validate patches and prioritize remediation. A verified trigger is stronger evidence than merely reaching a suspicious line.

**Prior limitation:** The paper identifies reachability constraints and triggering constraints. It argues existing directed fuzzing and LLM-assisted fuzzing struggle to solve both efficiently. PBFuzz automates an iterative analyst process: inspect code, form a hypothesis, generate inputs, execute, inspect feedback and refine.

Source: https://arxiv.org/abs/2512.04611 .

## 3. Methodology

- **Core idea:** An LLM-driven directed-fuzzing agent reasons about a target bug, extracts semantic constraints, creates property-based input generators, runs them and uses debugging feedback to refine its hypothesis until a PoV is found or budget is exhausted.
- **Input:** Target program/source repository, bug identifier or vulnerable location, build/run information, static analysis and execution feedback.
- **Output:** Test input triggering the target vulnerability, with campaign evidence and PoV validation.
- **Components:** (1) autonomous code reasoning for semantic reachability/triggering constraints; (2) custom program-analysis tools; (3) persistent memory to avoid hypothesis drift; (4) property-based testing that preserves input structure; (5) execution/debugger feedback.
- **AI contribution:** The LLM interprets source and reasons about semantic conditions difficult to encode as generic mutation heuristics. Conventional fuzzing/property-based testing execute and explore candidate inputs; runtime validation remains essential.
- **Architecture:** Use the paper architecture figure with attribution. The current public repository packages PBFuzz as DeepSeek Harness plugins with a PIER loop (PLAN → IMPLEMENT → EXECUTE → REFLECT). This maintained repository may have evolved since the original paper artifact; do not assume every current detail is identical to the paper version.

## 4. Experimental evidence

| Item | Evidence |
| --- | --- |
| Dataset | Magma benchmark; paper reports experiments over 129 CVEs and nine additional security bugs across nine software projects. |
| Baselines | Directed greybox and coverage-guided fuzzers, including AFLGo and AFL++ with CmpLog; exact configurations vary by experiment. |
| Metrics | Vulnerabilities triggered, unique vulnerabilities, time-to-exposure (TTE), campaign time/budget, PoV validity and API cost. |
| Results | Paper reports 57 vulnerabilities triggered and 17 uniquely triggered compared with existing fuzzers. Per-target budget is 30 minutes versus 24 hours for conventional approaches in the comparison. Median TTE is 339 seconds vs 8,680 seconds for AFL++ with CmpLog (reported 25.6× speedup). API cost reported around US$1.83 per vulnerability. |
| Real-world evidence | Paper reports reproducing three FFmpeg 1-day CVEs without public PoVs and identifying three previously unknown Bento4 vulnerabilities. Author-reported, not independently reproduced. |
| Compute/setup | Current repository requires Ubuntu 22.04/24.04 x86-64, Node.js 22+, Python 3.11+ and DeepSeek Harness with API key. Optional C/C++ static analysis requires LLVM 14. |
| Validity risks | Depends on target buildability, bug-oracle quality, static-analysis accuracy, LLM/API behavior, campaign budget and benchmark representativeness. Triggers must be independently validated. |
| Reproduction | Not attempted. Paper, current repository README, license and Zenodo artifact metadata inspected; no build/campaign run. |

Sources: https://arxiv.org/abs/2512.04611 ; https://github.com/sgzeng/pbfuzz ; https://zenodo.org/records/20770567 ; https://github.com/HexHive/magma .

## 5. Candidate research gaps

| Gap | Rationale | Type | Related work to compare |
| --- | --- | --- | --- |
| Cost-aware campaign scheduling | LLM calls add measurable cost; decide when to ask for a new hypothesis versus continue mutation/property-based search | Our inference | LLM-guided and hybrid fuzzers |
| Malformed-input exploration | Structured property-based generators may miss bugs requiring malformed/partially invalid inputs; combine structured generation with controlled mutation | Our inference; check paper discussion | Grammar-aware and mutation-based fuzzing |
| Independent PoV validation | Add a separate oracle/triage stage for reproducibility, sanitizer evidence and crash uniqueness | Our inference | Crash deduplication and oracle design |
| Transfer campaign knowledge | Reuse validated constraints/generators across related versions without stale hypotheses | Our inference | Fuzzing corpus reuse and agent memory |

These are hypotheses, not established novelty. Compare recent agentic fuzzers before claiming a contribution.

## 6. Potential methodological improvements

- **Hypothesis A:** A hybrid search controller alternating LLM semantic hypotheses with mutation/property-based exploration reduces LLM cost while maintaining or increasing verified PoV yield.
- **Hypothesis B:** An independent validation/triage layer validates triggers, deduplicates crashes and ranks reproducible PoVs using sanitizer/debugger evidence.
- **Expected benefit:** More verified vulnerabilities per unit time/API cost, fewer false PoVs, improved malformed-input coverage and lower TTE.
- **Experiment:** On a small fixed Magma subset, compare baseline PBFuzz, PBFuzz + hybrid mutation, and PBFuzz + validation/triage under identical time/API budgets. Measure verified PoVs, unique bugs, TTE, coverage, false-trigger rate and cost. Ablate LLM planning, mutation, memory and validation.
- **Risk:** PBFuzz is already an advanced agentic fuzzer. A new prompt or generic mutation step is not enough; compare carefully with PBFuzz, AFL++/CmpLog and recent hybrid/agentic fuzzing.

## 7. Feasibility by 2026-12-31

| Requirement | Assessment |
| --- | --- |
| Code verified and tested? | Public repository and README inspected; not executed. Current repo packages DeepSeek Harness plugins and may have evolved since paper artifact. |
| Dataset availability | Zenodo v2 artifact contains code/build scripts and prebuilt static-analysis results for nine Magma bugs. Check Magma and target licenses. |
| Model/API | Requires DeepSeek Harness and configured DeepSeek API key; check current availability, pricing and rate limits. |
| Hardware/setup | Linux x86-64, Node 22+, Python 3.11+; optional LLVM 14. Target builds and fuzzing can be resource intensive. |
| Five-week prototype | Conditional: one language and 2–3 Magma targets; reproduce artifact flow, then add one controller or validation improvement. |
| Excluded scope | Full nine-project reproduction, broad language support, new static analyzer, production deployment, large-scale zero-day discovery. |
| Blockers | Linux environment, target builds, API cost/key, sandboxed execution, oracle validation, noncommercial license restrictions. |
| Verdict | **Conditional** — focused benchmark prototype plausible; full reproduction not guaranteed. |

**License caution:** Current PBFuzz repository declares PolyForm Noncommercial 1.0.0. It permits noncommercial research/education under its terms but restricts commercial use and imposes distribution/notice obligations. Confirm with the supervisor before modifying or redistributing; public GitHub does not mean unrestricted permissive licensing.

## 8. Two-group potential (7 members)

- **Group A (4):** Cost-aware hybrid search controller combining LLM semantic hypotheses with property-based and mutation fuzzing. Measure verified PoV yield, TTE, coverage and API cost.
- **Group B (3):** Independent PoV validation/triage using reproducible execution, sanitizer/debugger evidence and crash deduplication. Measure false-trigger rate, unique validated bugs and triage time.
- **Integration:** Group A proposes candidate inputs/campaigns; Group B validates and ranks PoVs. Validation feedback can guide the next search iteration.
- **Separate evidence:** A compares search strategies under equal time/API budgets; B evaluates validation accuracy/reproducibility on generated and known-trigger inputs.

Provisional only; no team assignment implied.

## 9. Selection rubric (1–5)

| Criterion | Score | Evidence |
| --- | ---: | --- |
| Research quality/relevance | 5 | Practical software-security problem, CCS 2026 artifact record and benchmark evaluation |
| Feasibility | 3 | Focused Linux/Magma prototype plausible; build and API setup nontrivial |
| Novelty potential | 4 | Hybrid search scheduling and independent PoV validation are possible; literature check pending |
| Different from previous IDS | 5 | Software vulnerability testing, not network IDS |
| Meaningful AI for cybersecurity | 5 | LLM agentic code reasoning central to constraint extraction |
| Modernity | 5 | Agent reasoning, program analysis, property testing and runtime feedback |
| Public resources | 4 | Public repository and Zenodo artifact; noncommercial license, no reproduction |
| Measurable improvement | 5 | PoV yield, unique bugs, TTE, coverage, false triggers, API cost |
| Two contributions | 5 | Search efficiency and independent validation separable and integrable |
| **Total** | **41/45** | Provisional; license and environment are critical constraints |

## 10. Final assessment

- **Three strengths:** Practical PoV generation problem; measurable Magma results and real-world cases reported by authors; public source/artifact supports a scoped prototype.
- **Three risks:** Linux/toolchain/API dependent; full reproduction is substantial; current repository's noncommercial license and post-publication evolution need care.
- **Unverified:** Exact ACM DOI/proceedings metadata; reproduce at least one Magma target; current API cost; target licenses and artifact commit corresponding to paper.
- **Recommendation:** **Recommend as candidate**, conditional on setup test and supervisor acceptance of license.
- **Argument:** PBFuzz provides a distinct AI-for-software-security direction measured by verified vulnerabilities and discovery efficiency, without repeating intrusion detection.

## 11. Supporting references

- Paper: https://arxiv.org/abs/2512.04611
- Source: https://github.com/sgzeng/pbfuzz
- CCS 2026 artifact v2: https://zenodo.org/records/20770567
- Magma: https://github.com/HexHive/magma
- AFL++: https://github.com/AFLplusplus/AFLplusplus
- License: https://polyformproject.org/licenses/noncommercial/1.0.0/

## Submission checklist

- [x] Paper and source links recorded; DOI to verify
- [x] Author claims separated from hypotheses
- [x] Results attributed to paper
- [x] Code/artifact/benchmark/license inspected; no reproduction claimed
- [x] Gaps framed as hypotheses pending literature review
- [x] Deadline feasibility assessed
- [x] Two-group contributions considered
- [x] Nine rubric scores justified

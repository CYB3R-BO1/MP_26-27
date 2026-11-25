# ProtocolGuard: Detecting Protocol Non-compliance Bugs via LLM-guided Static Analysis and Dynamic Verification

> **Status:** Candidate reference — second preference in this individual discovery submission. This is not a final project choice. Author-acknowledged limitations are distinguished from proposed extensions.

## 1. Paper identification

| Field | Value |
| --- | --- |
| Submitted by | Harsha Vardhan |
| Preference | Second |
| Assigned source/category | NDSS 2026 |
| Authors | Xiangpu Song, Longjia Pei, Jianliang Wu, Yingpei Zeng, Gaoshuo He, Chaoshun Zuo, Xiaofeng Liu, Qingchuan Zhao, Shanqing Guo |
| Conference/journal | Network and Distributed System Security (NDSS) Symposium 2026 |
| Publication/acceptance date | Presented at NDSS, 23–27 February 2026 |
| Primary paper / DOI | [NDSS PDF](https://www.ndss-symposium.org/wp-content/uploads/2026-f521-paper.pdf) · [DOI: 10.14722/ndss.2026.240521](https://doi.org/10.14722/ndss.2026.240521) |
| Source code URL + license | [songxpu/ProtocolGuard](https://github.com/songxpu/ProtocolGuard) — public; license not verified |
| Dataset/benchmark URL + license | [Zenodo artifact, DOI 10.5281/zenodo.17933922](https://doi.org/10.5281/zenodo.17933922) and 11 evaluated open-source protocol implementations; benchmark/data licensing needs individual verification |
| Cybersecurity problem/domain | Detecting protocol-specification non-compliance bugs in network protocol implementations |
| AI techniques | LLM-guided program slicing, semantic inconsistency analysis, LLM-generated assertions and test-case descriptions/scripts |

## 2. Problem and motivation

**Exact cybersecurity problem:** Protocol implementations can silently deviate from normative requirements in RFCs or other specifications. These logic errors may not cause crashes, so memory-safety sanitizers and conventional crash-based fuzzing can miss them.

**Why it matters:** Protocol non-compliance can cause interoperability failures and security vulnerabilities. The paper's MQTT motivating example describes silent truncation of oversized client identifiers, which can cause distinct clients to collide.

**Prior research limitation:** Section I and Section II explain that heuristic static analysis can be brittle across implementation styles; differential testing can miss a fault shared by all compared implementations; and manual validation/root-cause analysis is expensive. The paper also explains that direct LLM analysis of an entire codebase creates excessive context.

## 3. Methodology

- **Core technical idea:** Extract normative protocol rules, identify relevant implementation code using LLM-guided program slicing, detect semantic inconsistencies, then validate suspected bugs dynamically.
- **Input data:** Protocol specifications (e.g. RFCs), C source code for protocol implementations, build/analysis artifacts and protocol test inputs.
- **Output:** Candidate non-compliance findings, instrumented assertions, dynamically verified failures and proof-of-concept test cases.
- **Main components / model / verification:**
  1. Protocol rule extraction: hybrid keyword filtering and LLM refinement.
  2. LLM-guided program slicing: identify relevant handlers, collect context, perform rule-oriented forward slicing and prune unrelated code.
  3. LLM-based inconsistency detection: compare normative rules with implementation logic.
  4. Fuzzing-based dynamic verification: generate assertions and targeted initial inputs, instrument the implementation and use directed protocol fuzzing to validate findings.
- **What AI contributes (and why):** LLMs interpret natural-language specification requirements and code semantics, guide slicing, propose assertions and generate counterexample descriptions/scripts. Static analysis and fuzzing provide program evidence and dynamic confirmation.
- **Architecture:** See Fig. 1 in the primary paper (PDF p. 4). Four major stages: rule extraction, program slicing, inconsistency detection and dynamic verification.

## 4. Experimental evidence

| Item | Detail and source location |
| --- | --- |
| Datasets and size | 11 widely used protocol implementations covering six protocols; the paper extracts 420 normative rules (reported in the evaluation/talk materials; verify exact table/section before formal reuse). Implementations include MQTT, TLS, DHCP, FTP and others. |
| Baseline systems | AI-powered code editors Cursor with Claude 3.7 Sonnet and DeepSeek R1; comparisons with static analysis and protocol fuzzing approaches. |
| Evaluation metrics | Precision, recall, confirmed bug count, assertion compilation/semantic accuracy, assertion-triggering rate and fuzzing crash/bug discovery. |
| Exact numerical results | Abstract: 158 non-compliance bugs discovered, 70 confirmed. Section II / evaluation reports 156 previously unknown bugs and 90.6% overall precision for discovery; comparison on four programs reports ProtocolGuard 86.3% precision and 81.3% recall versus Cursor+Claude 3.7 at 71.7% precision and 76.8% recall (Section VI.B). Assertion generation: 88.9% average implementation accuracy and 68.4% average crash-triggering rate (Section VI.C). ProtocolGuard-generated initial seeds produced on average 155.2% more assertion-triggered unique crashes than random seeds (Section VI.D). |
| Hardware/compute | Artifact README specifies Ubuntu 22.04.3, Python 3.10, Go 1.18.1, LLVM 12 and 14, Cursor, and third-party LLVM/SVF/AFLNet-related dependencies. LLM service/API access is required; compute and API cost not independently measured. |
| Known threats to validity | Manual assessment of findings; evaluation of detailed precision/recall on four programs due to time-intensive expert review; C-only support; assertion quality depends on context; fuzzer may generate invalid inputs; some workflow stages require manual intervention. |
| Reproduction status | Not attempted. NDSS artifact page lists ProtocolGuard as Available; Functional/Reproduced status was not shown in the checked results. |

All quantitative figures above are author-reported. Our team has not independently reproduced them.

## 5. Candidate research gaps

| Gap | Evidence (section/page) | Author-acknowledged or our inference? | Possible overlap in 2024–2026 work |
| --- | --- | --- | --- |
| Improve assertion generation with runtime execution state | Section VI, “Inaccuracy in Assertion Generation”: current agent sees static code and may misunderstand control flow/variable state; authors propose incorporating dynamic execution information. | Explicitly acknowledged by authors | Must compare with dynamic LLM program analysis, trace-conditioned assertion generation and runtime-guided repair/testing. |
| Improve valid-input exploration of deep protocol paths | Section VI, “Ineffectiveness of Fuzzing-based Dynamic Verification”: syntactically invalid inputs may be rejected early; authors suggest protocol-aware mutation or symbolic execution. | Explicitly acknowledged by authors | Protocol-aware fuzzing and grammar/state-aware mutation are active areas; novelty requires a specific measurable improvement over existing fuzzers. |
| Avoid one frequently triggered assertion dominating fuzzing | Section VI, “Manual Effort”: users may manually disable triggered assertions; authors suggest shared-memory tracking and automatic disabling. | Explicitly acknowledged by authors, with a suggested solution already in the paper | High overlap risk because the authors already outline a memory-based feedback solution. Do not claim this idea alone as novel. |
| Improve completeness for callback-based architectures and C++ implementations | Section VI, “Inaccuracy of LLM-guided Program Slicing”: handler-centric slicing can miss callback paths; current framework is C-focused and C++ support is future work. | Explicitly acknowledged by authors | Must compare with interprocedural/callback-aware static analysis and C++ program slicing research. |

A perceived gap is not established novelty until independently checked. The authors already propose several of these directions; a project must define a distinct, testable contribution rather than simply implement their stated future work.

## 6. Potential methodological improvements

- **Hypothesis A:** Build a runtime-context package for assertion review: collect bounded execution traces, relevant variable values and branch/path information for a candidate violation, then ask the LLM to revise or validate the assertion. Measure compile success, semantic correctness and dynamic trigger rate.
- **Hypothesis B (alternative or complementary):** Evaluate a protocol-aware seed/mutation layer that preserves message structure and state while targeting a specific rule violation. Compare against the original directed-fuzzing configuration and random seeds.
- **Expected security/efficiency benefit:** Reduce invalid assertions and early-rejected inputs; improve the proportion of candidate violations that can be dynamically confirmed.
- **Experiment and ablation plan:** Select one supported C implementation and one protocol initially; reproduce a small baseline; compare static-only versus runtime-context assertion generation; compare baseline mutation versus protocol-aware mutation. Measure assertion compilation rate, expert-reviewed semantic correctness, valid-input rate, target-path coverage, assertion coverage, confirmed findings and time-to-confirmation.
- **Risk of failure or overlap:** The authors explicitly identify runtime context and protocol-aware mutation as future directions. These are not novel by themselves. Need a narrower contribution and a related-work comparison. The repository's setup is complex and depends on external LLM tooling.

Do not finalize a project architecture at discovery stage.

## 7. Implementation feasibility by 2026-12-31

| Requirement | Assessment |
| --- | --- |
| Public code verified and actually tested? | Public repository and README verified; not installed or executed by our team. |
| Datasets available and legally usable? | Zenodo artifact is public; evaluated protocol implementations are open source. Individual project and dataset licenses must be checked before reuse. |
| Models/inference APIs available? | README requires Cursor and an LLM API configuration; API/model availability and costs need verification. |
| Hardware, API cost, and development effort | Ubuntu 22.04, Python 3.10, Go 1.18, LLVM 12/14, SVF and AFLNet-related toolchains. High integration effort; API cost depends on selected model and usage. |
| Realistic five-week minimum implementation | Conditional: limit scope to one C-based MQTT implementation and a small number of protocol rules; first reproduce one static-to-dynamic workflow before adding one improvement. |
| Features deliberately excluded | All six protocols, full multi-language support, broad C++ support, production vulnerability disclosure and full reproduction of every reported bug. |
| Top blockers | Toolchain compatibility; LLVM/SVF/AFLNet build complexity; external LLM service access/cost; ground-truth review; time needed to understand the protocol implementation. |
| Verdict | **Conditional** — technically rich and well aligned, but substantially higher integration risk than WebSpotter. |

## 8. Two-group potential (7 members)

- **Group A (4 members) — possible independently measurable contribution:** LLM-guided specification/code analysis with runtime-context evidence for assertion generation. Measure assertion correctness, compilation and reviewer-confirmed precision.
- **Group B (3 members) — distinct but complementary contribution:** Protocol-aware test generation and fuzzing feedback for dynamic verification. Measure valid-input rate, path/assertion coverage and time-to-confirmation.
- **How the contributions integrate:** Group A supplies candidate rule violations and assertions; Group B attempts to trigger and verify those assertions with targeted protocol inputs.
- **How each group demonstrates a result separately:** Group A evaluates assertion quality on a fixed set of candidate findings; Group B evaluates fuzzing efficiency on a fixed set of verified assertions/rules.

Provisional only; no team assignment is implied.

## 9. Consistent selection rubric (1–5 each)

5 = excellent; 4 = good; 3 = conditional; 2 = weak; 1 = poor.

| Criterion | Score / 5 | Evidence |
| --- | ---: | --- |
| Research quality and relevance | 5 | NDSS 2026 paper addressing silent protocol non-compliance bugs with a substantial evaluation. |
| Implementation feasibility | 3 | Public code/artifact, but multi-toolchain build and LLM integration create significant schedule risk. |
| Novelty potential | 3 | Explicit limitations offer research questions, but authors already propose some improvements and related-work overlap is likely. |
| Different from previous federated/continual/graph IDS | 5 | Protocol implementation analysis and fuzzing are distinct from FedShield-CTI. |
| Meaningful AI for cybersecurity | 5 | LLM reasoning is central to rule extraction, slicing, inconsistency analysis and assertion/test generation. |
| Technically justified modernity | 5 | Combines LLM-assisted program analysis with dynamic protocol verification. |
| Public resources/reproducibility | 4 | Public repository and Zenodo artifact; artifact status only Available in checked NDSS results, not reproduced. |
| Measurable improvement | 5 | Precision/recall, assertion correctness, coverage, valid-input rate and time-to-confirmation. |
| Two complementary contributions | 5 | Static/LLM analysis and dynamic verification form distinct, measurable stages. |
| **Total** | **40/45** | Provisional discussion score; feasibility blockers can outweigh total. |

Scores support discussion; critical feasibility blockers can outweigh a high total.

## 10. Final assessment

- **Strongest three reasons to shortlist:**
  1. Important network-security problem involving silent protocol logic errors.
  2. LLM use is technically integrated with static analysis and dynamic verification, not merely a chatbot interface.
  3. The paper explicitly documents limitations and provides measurable evaluation dimensions.
- **Three weaknesses or risks:**
  1. Complex setup involving LLVM, SVF, AFLNet and external LLM tooling.
  2. The authors already identify and suggest several obvious extensions, increasing novelty-overlap risk.
  3. Manual review and protocol-specific setup make broad reproduction difficult within five weeks.
- **Unverified claims to investigate:** License of source and benchmark components; exact costs and supported LLM provider configuration; successful build on our environment; exact protocol-by-protocol benchmark details; independent reproducibility.
- **Recommendation:** **Conditional** — strong research quality, but proceed only if a minimal end-to-end baseline can be built early.
- **One-sentence argument versus competing papers:** ProtocolGuard offers a deeper program-analysis and protocol-security problem with explicit author-documented gaps, but it carries higher implementation and novelty risk than WebSpotter.

## 11. Supporting references

- Primary paper: [NDSS 2026 PDF](https://www.ndss-symposium.org/wp-content/uploads/2026-f521-paper.pdf) · [DOI](https://doi.org/10.14722/ndss.2026.240521)
- Repository/benchmark: [ProtocolGuard GitHub](https://github.com/songxpu/ProtocolGuard) · [Zenodo artifact](https://doi.org/10.5281/zenodo.17933922) · [NDSS 2026 artifact results](https://secartifacts.github.io/ndss2026/results)
- Closest related 2024–2026 work: Include RIBDetector, EBugDec, ParDiff, PARCLEANSE, AFLNet, SelectFuzz and recent protocol-aware fuzzing work in the related-work review; compare the exact proposed extension against these before claiming novelty.

## Submission checklist

- [x] Bibliographic details verified from primary publication
- [x] Author claims separated from personal hypotheses
- [x] Actual figures/tables used for quantitative results
- [ ] Code, datasets, licenses and compute availability checked by running the artifact
- [ ] Research gap supported by evidence and related-work review
- [x] December 31 feasibility assessed provisionally
- [x] Two-group contributions considered
- [x] Nine rubric scores justified

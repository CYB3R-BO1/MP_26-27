# CAP: Detecting Network Device Misconfigurations with Context-Aware Prompting of LLMs

> **Status:** Category 7 candidate reference (second preference). Not selected as the major project.

## 1. Paper identification

| Field | Value |
| --- | --- |
| Submitted by | Uday |
| Category | Others |
| Venue | ACM SIGMETRICS 2026 / Proceedings of the ACM on Measurement and Analysis of Computing Systems (POMACS) |
| Paper | [PDF](https://aaron.gember-jacobson.com/docs/pomacs2026cap.pdf) |
| DOI | [10.1145/3805631](https://doi.org/10.1145/3805631) |
| Source code | Not verified as publicly released |
| Full evaluation dataset | Not verified as publicly released |
| Domain | Network device configuration and misconfiguration analysis |
| AI methods | Context-aware prompting, hierarchical representations of configurations, LLM reasoning and retrieval |

## 2. Problem and motivation

Network device configuration correctness depends on relationships across sections and sometimes multiple devices. Large full-file LLM prompts can waste context and obscure evidence, while naive splitting can discard cross-reference dependencies. CAP investigates giving LLMs precisely relevant configuration context to identify misconfigurations.

## 3. Methodology

The approach organizes configuration into a hierarchy and lets the model retrieve related or referenced sections during analysis instead of always using an entire document. Relevant relationships (neighbors, similar components and references) inform subsequent LLM diagnosis.

- **Input:** Network device configurations.
- **Output:** Diagnosed configuration inconsistencies/misconfigurations.
- **AI's role:** Selecting/using contextual configuration information to reason about errors.
- **Core research question:** Whether selective contextual prompting improves diagnosis versus standard LLM input approaches.

Consult the PDF for exact algorithms and full architecture.

## 4. Experimental evidence

| Item | Evidence / verification |
| --- | --- |
| Evaluated configurations | Reportedly includes Internet2 and two university networks |
| Baselines | Conventional prompting approaches; exact names/scores must be obtained from original paper tables |
| Main reported result | Improved misconfiguration diagnosis in the authors' experiments; numerical values not independently verified here |
| Code | Not verified available |
| Complete dataset | Not verified available |
| Reproduction status | Not attempted |

Do **not** infer reproducibility from the existence of a paper alone.

## 5. Candidate research gaps

| Hypothesis | Rationale | Status |
| --- | --- | --- |
| Security intent in retrieval | Configuration adjacency may not capture the policy's purpose | Potential, needs evaluation |
| Deterministic check of findings | LLMs may falsely flag valid configurations | Potential, compare existing checkers |
| Incremental audits | Rechecking only impacted dependencies after policy changes could be faster | Potential, literature survey required |
| Cost-aware context selection | Reduce irrelevant retrieval/model calls without reducing recall | Potential experimental contribution |

These are literature-review hypotheses, **not proven novelty**.

## 6. Potential improvements and testing

A candidate system could compare full-context, chunked prompting, structural retrieval and intent-aware retrieval. Validate model findings with deterministic reachability/policy tests. Measure misconfiguration F1, false-positive rate, latency, tokens and robustness to irrelevant/missing configuration lines. Establish realistic and licensed ground truth first.

## 7. Implementation feasibility by December 31, 2026

**Conditional / moderate:** The core idea can be adapted using configuration parsers, small LLMs or hosted inference, and an independent policy verifier. Reproduction of the original method and dataset may be difficult if source code and network configurations are not released.

- Public implementation: unverified.
- Data accessibility: unverified.
- Main risk: faithful replication and sufficiently realistic benchmark.
- Minimal deliverable: restricted device ACL/policy configurations with seeded/canonical errors.
- Defer: support for every routing protocol/vendor and unrestricted operational-scale systems.

## 8. Potential two-group decomposition (not selected)

- **4 members:** Configuration dependency extraction and selective context prompting; evaluate detection quality/latency.
- **3 members:** Formal checking of findings and false-positive reduction; evaluate verified detection quality.
- **Integration:** Diagnosis supplies candidate security findings, checker validates them.
- **Risk:** This particular decomposition may overlap with existing LLM plus verification research; novelty requires literature review.

## 9. Criteria assessment

| Criterion | Provisional judgment |
| --- | --- |
| Quality / relevance | Strong 2026 measurement research venue |
| Feasibility | Moderate because experimental resources unverified |
| Novelty | Plausible, still to establish |
| Different from earlier projects | High |
| AI for cybersecurity | High |
| Modern | Strong |
| Resources | Uncertain |
| Measurable | F1/false positives, latency, tokens, robustness |
| Two-group fit | Plausible |

No numeric score assigned until shared team comparison.

## 10. Verdict

**Recommend as complementary reference, conditional on resources.** Strong relevance to LLM-based network security analysis and clear evaluation questions. Biggest risk is unverified code and dataset accessibility. Final project choice will be among the full 14-paper shortlist.

## 11. Related references

- [CAP publication](https://doi.org/10.1145/3805631)
- [Elastispec](https://purdue-isl.github.io/papers-pdf/Sigcomm26_ElastiSpec.pdf)
- [Cornetto benchmark](https://github.com/nsg-ethz/cornetto)
- [Batfish](https://github.com/batfish/batfish)

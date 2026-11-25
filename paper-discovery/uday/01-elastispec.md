# Elastispec: Formalizing Enterprise Firewall Management with Informal and Elastic Specifications

> **Status:** Category 7 candidate reference (first preference). Not selected as the major project.

## 1. Paper identification

| Field | Value |
| --- | --- |
| Submitted by | Uday |
| Category | Others |
| Conference | ACM SIGCOMM 2026 |
| Paper | [PDF](https://purdue-isl.github.io/papers-pdf/Sigcomm26_ElastiSpec.pdf) |
| DOI | [10.1145/3789240.3829191](https://doi.org/10.1145/3789240.3829191) |
| Source code | [Purdue-ISL/Elastispec](https://github.com/Purdue-ISL/Elastispec) (public repository; reproduction not attempted) |
| Domain | Enterprise firewall policy verification |
| AI methods | LLM-based extraction of informal networking requirements; structured specifications and deterministic auditing |

## 2. Problem and motivation

Enterprise firewall requirements are often specified in vendor manuals or informal natural-language application documentation. Translating them into unambiguous allowed/required communication policies and checking network configurations manually is error-prone and difficult to scale. The paper explores making these requirements formally auditable.

## 3. Methodology

The system translates informal networking requirements into structured domain-specific security specifications with LLM assistance, resolves enterprise context, and audits firewall/network policy against the specifications with deterministic reasoning.

- **Input:** Vendor/application documentation, contextual enterprise network information, firewall configuration.
- **Output:** Structured communication requirements and reported compliance issues.
- **AI's role:** Extracting and formalizing informal specifications.
- **Non-AI component:** Deterministic policy evaluation/auditing.

Refer to the original PDF for the authors' architecture and exact translation/auditing pipeline; no reproduced original figure is included here.

## 4. Experimental evidence

| Item | Evidence / verification |
| --- | --- |
| Main reported metric | Approximately 61% to 96% specification translation accuracy compared to the evaluated baseline, as reported by the authors |
| Baselines / exact sample | Check specific PDF evaluation tables before quoting as independently established |
| Datasets / examples | Public repository has example inputs/specifications and audit/translation components |
| Code | Available, but neither baseline reproduction nor dependencies tested for this review |
| Reproduction status | Not attempted |
| Training compute | No foundation model training required for a scoped extension; exact original inference cost not independently verified |

The numerical claim is **author-reported**, not a result reproduced by this team.

## 5. Candidate research gaps

| Hypothesis | Rationale | Status |
| --- | --- | --- |
| Explicit uncertainty handling | Requirements may be ambiguous, conflicting, incomplete or stale | Potential extension; needs prior-work search |
| Conservative repair proposals | Move from auditing findings to minimal corrective recommendations | Potential extension; related verification-guided repair already exists |
| Regression-safe policy change | Ensure fixes preserve required connectivity and don't open unintended communication | Must establish difference from existing formal repair work |
| Inference efficiency | Examine smaller models and reduced token/latency budgets | Requires controlled baselines |

These are **potential**, not confirmed original gaps.

## 6. Potential improvements and testing

A possible experiment could compare basic prompting against calibrated extraction with uncertainty flags; validate proposed policies using an independent checker; then measure extraction accuracy, false positives and coverage. A separate, more ambitious experiment could rank minimal firewall repairs subject to reachability invariants. Repair must not be framed as an original idea without surveying existing work.

## 7. Implementation feasibility by December 31, 2026

**Conditional / moderate–high:** A restricted proof-of-concept using IPv4 ACLs, TCP/UDP reachability and a small collection of network configurations is plausible with seven team members. Build on public reference code and formal tools (e.g. Batfish or Z3) rather than training a large model. Primary risks: correctly defining ground truth and producing defensible, non-clone research comparisons.

- Source code: public, not run.
- Dataset/license compatibility: still requires checking.
- Hardware: small-model/API approach plausible; cost not measured.
- Minimal experiment: policy extraction → deterministic checking → error analysis.
- Defer: full enterprise heterogeneity and multi-vendor production support.

## 8. Potential two-group decomposition (not selected)

- **4 members:** Intent extraction and uncertainty-aware requirements validation; assess precision/recall and false-positive reduction.
- **3 members:** Security-constrained policy verification or repair ranking, with regression checks and measurable correctness.
- **Integration:** First group supplies structured requirements; second tests or acts on them.
- **Risk:** Strong novelty must be proven, particularly for automated repair.

## 9. Criteria assessment

| Criterion | Provisional judgment |
| --- | --- |
| Quality / relevance | Strong 2026 systems/network venue |
| Feasibility | Good with disciplined scope |
| Novelty | Plausible, still to establish |
| Different from earlier projects | High |
| AI for cybersecurity | High |
| Modern | Strong |
| Resources | Public code; full reproducibility not demonstrated |
| Measurable | Accuracy, FP rate, security correctness, efficiency |
| Two-group fit | Plausible |

No numeric score assigned here until the shared team review.

## 10. Verdict

**Recommend as a strong reference candidate.** Strengths are the venue, network-security relevance, and public implementation. Main limitations are uncertain reproducibility of every result, scope risk, and the need to distinguish any proposed changes from prior work. The team will choose from all 14 papers.

## 11. Related references

- [Elastispec repository](https://github.com/Purdue-ISL/Elastispec)
- [Cornetto: Benchmarking LLM-Driven Network Configuration Repair](https://arxiv.org/abs/2604.22513) / [repository](https://github.com/nsg-ethz/cornetto)
- [NetInspector preprint](https://arxiv.org/abs/2609.21103)
- [Batfish](https://github.com/batfish/batfish)
- [Z3](https://github.com/Z3Prover/z3)

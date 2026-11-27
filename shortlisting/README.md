# Phase 2 — Final shortlist

**Decision date:** 27 November 2026  
**Status:** Shortlist frozen; Phase 2 closed at the selection and documentation level. Practical reproduction, novelty verification and final project selection remain pending.  
**Project implementation/evaluation deadline:** 31 December 2026.

## Selection principles

- Prefer meaningful AI algorithms and active cybersecurity mechanisms over LLM-assisted reporting or policy automation.
- Network security preferred; practical AppSec directions are eligible.
- Avoid repeating FedShield-CTI or TRENCH-IDS, including federated, continual and conventional graph-based IDS research.
- No paid inference APIs. Local compute and hardware availability must be demonstrated.
- Feasibility is a mandatory gate, not a weighted score. Do not rank candidates numerically before collecting evidence.
- The project must offer original, testable research and two complementary contributions for groups of four and three.

## Frozen shortlist (not a ranking)

| Paper | Venue | Main attraction | Principal risk | Investigation allocation |
| --- | --- | --- | --- | --- |
| [MARISSA](../paper-discovery/independent-discovery/14-others-marissa.md) | IEEE EuroS&P 2026 | Lightweight protocol inference | Novelty and downstream security value | 2 members |
| [TamRL](../paper-discovery/independent-discovery/05-ccs-tamrl.md) | ACM CCS 2026 | Learned formal proof search | Formal methods learning curve and compute | 2 members |
| [WebSpotter](../paper-discovery/harsha-vardhan/01-webspotter.md) | NDSS 2026 | Reproducible AppSec research | Becoming another detector rather than a protection mechanism | 1 member |
| [CenRL](../paper-discovery/independent-discovery/01-sp-cenrl.md) | IEEE S&P 2026 | Lightweight learning for network measurements | Incremental bandit contribution | 1 member |
| [Securitas](../paper-discovery/independent-discovery/13-others-securitas.md) | USENIX NSDI 2026 | Active network privacy protection | Testbed integration, compute and license | 1 member |

**Reserve:** [Elastispec](../paper-discovery/uday/01-elastispec.md), with [CAP](../paper-discovery/uday/02-cap.md) as supporting literature. Elastispec is not an active sixth candidate: its translator's local-model compatibility and originality remain unresolved. ProtocolGuard is not shortlisted because the documented LLM/toolchain requirements add deadline and budget risk.

## Resource evidence and research questions

The following is a consolidation of prior shortlisting reviews and the team's supplied Securitas follow-up, not a new independent artifact execution. Published hardware and documented local support do not establish performance on team laptops. Dataset/model licenses, exact repository revisions and actual peak resource use must be recorded during testing.

### MARISSA

- [Paper](https://doi.org/10.1109/EuroSP68448.2026.00084), [repository](https://github.com/reverseame/MARISSA), [author explanation](https://reversea.me/index.php/inferring-network-protocols-from-traffic-with-marissa/).
- Python 3.11, Poetry, MAFFT; Docker documented; GPL-3.0 reported. Dataset directory reported; verify individual capture contents, ground truth and terms. Baseline does not inherently require GPU or paid API.
- **Question:** Can lightweight learned representations and uncertainty-aware inference recover message fields more reliably from limited observations and demonstrate measurable downstream security utility?
- Possible complementary contributions: message representation/clustering and reliable field inference/validation.
- Baselines: original MARISSA, simple byte representations; compare against TransRE, FLINT and FieldWeaver in related-work review. Do not claim neural embeddings alone as novel.
- Metrics: clustering V-measure/ARI, field-boundary F1, sample efficiency, runtime, memory and downstream validation utility.
- Gate: run one labeled capture and check inferred boundaries. Missing variation in observed fields can make inference fundamentally underdetermined.

### TamRL

- [Paper](https://arxiv.org/abs/2605.23643), [framework](https://github.com/MatCos/TamRL), [Tamarin ML API](https://github.com/niklasmedinger/Tamarin-ML-API), [artifact](https://zenodo.org/records/22819846).
- MIT framework reported; protocol models may use separate GPL terms. Python 3.11 and modified Tamarin; 16 protocol case studies and documented CPU demonstration. Full training requires multiple GPU-days, outside default scope.
- **Question:** Can learned proof-search guidance improve the number of verified properties under strict compute limits?
- Possible complementary contributions: lightweight learned search and adaptive verification-budget allocation.
- Baselines: default Tamarin heuristics and original TamRL under comparable budgets; inspect related learned theorem proving and search work.
- Metrics: verified lemmas, proof length, wall time, explored states and memory. Proof checking remains independent of the AI.
- Gate: execute documented small YubiKey HSM CPU demonstration; establish accessible benchmark, checkpoint compatibility, proof validation and training budget. Formal model verification is not verification of the actual implementation.

### WebSpotter

- [Paper](https://www.ndss-symposium.org/wp-content/uploads/2026-s1029-paper.pdf), [repository](https://github.com/Sec-AI-research/WebSpotter), [dataset artifact](https://doi.org/10.5281/zenodo.16978408), [NDSS artifact results](https://secartifacts.github.io/ndss2026/results).
- Prior review records Available, Functional and Reproduced badges; Python 3.9/PyTorch, CSIC, PKDD, FPAD and FPAD-OOD. CPU support documented; 16 GB RAM and ~12 GB recommended GPU VRAM in prior review; original RTX 4090. Core artifact needs no paid inference. Confirm licenses separately.
- **Question:** Can confidence-aware localization and independent mitigation validation improve actual web application protection without blocking legitimate requests?
- Possible complementary contributions: calibrated localization/abstention and regression-safe mitigation selection.
- Baselines: original localization and WAF rule-generation pipeline, fixed-confidence decisions and conventional rules. Original work already evaluates unseen attack patterns and poisoning and generates WAF rules.
- Metrics: legitimate-request blocking rate, security effectiveness, calibration, malicious-request recall and latency.
- Gate: run one documented localization experiment, verify data access and assemble independent benign-request evaluation. Reject if the extension is only another detection classifier.

### CenRL

- [Paper](https://ieeexplore.ieee.org/abstract/document/11573591), [author page](https://levanhieu.com/publication/cenrl_sp_2026/), [repository](https://github.com/r-andlab/cenrl), [artifact](https://doi.org/10.5281/zenodo.17382167).
- Prior follow-up reports GPL-3.0, Tranco/GFWatch/Russia/Kazakhstan inputs and evaluation scripts, epsilon-greedy/UCB/Thompson sampling. Access, provenance and licenses of individual datasets still need checking. CPU-first offline evaluation; no paid inference.
- **Question:** Does explicit cost and uncertainty modelling improve useful measurement discovery and coverage under a fixed resource budget beyond existing bandit strategies?
- Possible complementary contributions: contextual cost-sensitive policy and uncertainty-aware exploration/coverage evaluation.
- Baselines: random, round-robin, epsilon-greedy, UCB, Thompson sampling, original CenRL and applicable cost-aware bandits. Original method already adapts to changing censorship.
- Metrics: useful findings per cost, coverage, regret, adaptation delay and overhead.
- Gate: execute controlled offline evaluation with included inputs; confirm replayability and relevance. No live censorship probing is needed.

### Securitas

- [Published paper](https://www.usenix.org/conference/nsdi26/presentation/xie-guorui), [PDF](https://www.usenix.org/system/files/nsdi26-xie-guorui.pdf), [original repository](https://github.com/xgr19/Securitas), [additional training repository](https://github.com/YiJia-Zhu/Securitas-fork), [ISCX data](https://www.unb.ca/cic/datasets/vpn.html).
- Team-supplied follow-up cites Appendices B/C: single-layer LSTM with 32 hidden units, policy-gradient learning, RTX 2080 Ti (11 GB), Python 3.8/PyTorch 1.9.1, CW100/HomeMole/ISCX, BMv2/eBPF/Mininet and a software testbed with two VMs on one laptop. These details are documentation-level evidence supplied in the discussion, not independently rechecked in this commit. Pretrained classifier checkpoint documented; policy checkpoint, training dependencies, exact artifact correspondence, testbed completeness and code/data licenses require confirmation.
- **Question:** Can a learned protection policy maintain privacy under held-out workloads and changing network conditions while meeting strict bandwidth and latency budgets?
- Possible complementary contributions: resource-aware policy learning and independent privacy/communication-utility evaluation.
- Baselines: no protection, fixed protection, original learned policy and appropriate resource-aware defenses; the original paper already optimizes privacy versus bandwidth. Novelty must go beyond that objective.
- Metrics: leakage or adversary inference effectiveness, bandwidth overhead, latency, utility, generalization and compute.
- Gate: run offline preprocessing/classifier/policy evaluation and establish that the software testbed can run on available hardware. Do not assume CPU training or deployment success from the small model architecture. No specialized networking hardware is planned.

## Phase 3 handoff — feasibility and finalization

| Date (2026) | Objective |
| --- | --- |
| November 27 | Freeze shortlist and agree on gates |
| November 28–29 | Parallel practical feasibility and related-work investigation |
| November 30 | Eliminate failed candidates, develop two proposals and discuss with professor |
| December 1 | Start the selected project, subject to approval |
| December 31 | Complete implementation and experimental evaluation |

Allocation is by number of members, not named assignments. The team must decide individuals and confirm hardware. The final 4+3 division is for the eventual project, not the temporary seven-person feasibility allocation.

Each investigation must submit a completed [feasibility report](FEASIBILITY_TEMPLATE.md) with logs, pinned versions, hardware/runtime, access/license evidence, baseline metrics, nearest related work and a precise hypothesis.

### Mandatory go/no-go gates

1. Executable baseline or independently defensible reference implementation.
2. Legally usable and accessible evaluation data, models and dependencies.
3. Zero paid inference and measured resource requirements compatible with actual hardware and deadline.
4. A credible, falsifiable research hypothesis beyond the original work and closest alternatives.
5. A practical security outcome and two complementary independently measurable contributions.
6. Scoped evaluation with strong baselines, ablations, held-out tests where relevant, and a reproducible experiment plan.

If a gate is unresolved, mark **Conditional** and specify the evidence needed by November 30. Do not label a failed or untested implementation as reproduced. Select final proposals only after evidence review; if fewer than two pass, reassess the reserve or narrow scope explicitly.

## Closure

- [x] Five candidates selected and frozen, with one reserve.
- [x] Resource documentation, candidate hypotheses and main risks consolidated.
- [x] Seven investigation slots and timeline agreed.
- [ ] Baseline execution (0/5 confirmed at closure).
- [ ] Dataset/model license and local hardware validation.
- [ ] Focused novelty verification and go/no-go decisions.
- [ ] Two final proposals and professor approval.

Phase 2 selection is complete. No project, architecture or final research novelty claim is approved yet. Discovery files remain unchanged.

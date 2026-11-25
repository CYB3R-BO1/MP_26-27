# MirrorGuard: Toward Secure Computer-Use Agents via Simulation-to-Real Reasoning Correction

> **Status:** Candidate reference — first preference, not a finalized project. Reproduction has not been attempted. Author-reported results are distinguished from proposed work.

## 1. Paper identification

| Field | Value |
| --- | --- |
| Submitted by | Umesh Chandra |
| Preference | First |
| Source/category | ACM CCS 2026 |
| Authors | Wenqi Zhang, Yulin Shen, Changyue Jiang, Jiarun Dai, Geng Hong, Xudong Pan |
| Venue | ACM CCS 2026 (verify final proceedings entry before final report) |
| Date | arXiv preprint posted 19 January 2026; final acceptance date not independently verified here |
| Primary paper | https://arxiv.org/abs/2601.12822 |
| Code and license | https://github.com/WhitzardAgent/MirrorGuard — repository declares MIT |
| Model/project | https://bmz-q-q.github.io/MirrorGuard/ and https://huggingface.co/WhitzardAgent/MirrorGuard |
| Benchmarks | OS-Harm, RiOSWorld; OSWorld for utility evaluation. Check benchmark terms and exact canonical RiOSWorld citation before reuse. |
| Domain | Computer-use agent (CUA) security, GUI prompt injection, unsafe OS actions, privacy/data leakage |
| AI techniques | VLMs, LLM-based neural-symbolic simulation, synthetic trajectory generation, supervised reasoning correction |

## 2. Problem and motivation

**Problem:** Computer-use agents interpret natural-language instructions and visual GUI content, then take actions on operating systems. Malicious instructions embedded in webpages or UI content, or unsafe user requests, can induce harmful operations. Monitor-and-block defenses can stop an unsafe action but may also terminate legitimate tasks, creating a security–utility trade-off.

**Why it matters:** CUAs can interact with terminals, browsers and files. A manipulated action may expose private data, alter permissions, download malware or damage system state.

**Prior limitation:** Action-level blocking intervenes after the agent has reasoned about an operation. MirrorGuard instead intervenes at the reasoning stage and attempts to replace insecure reasoning with a safe alternative. It also argues that text-only safety training does not necessarily transfer to visual GUI interactions. Source: paper motivation/method, https://arxiv.org/abs/2601.12822.

## 3. Methodology

- **Core idea:** Train a reasoning-correction module using security-related trajectories generated in a text-based neural-symbolic simulated desktop (MirrorWorld), then use the trained VLM to correct insecure thoughts in real GUI agents.
- **Input:** Task instructions, simulated desktop state and trajectories; at deployment, agent reasoning and visual GUI context.
- **Output:** Corrected safe reasoning that steers the agent toward a safer action.
- **Pipeline:** (1) MirrorWorld constructs risky and benign GUI scenarios; (2) simulator maintains structured state; (3) unsafe thoughts are identified and corrected; (4) data is formatted for VLM fine-tuning; (5) correction module is integrated with computer-use agents.
- **AI contribution:** LLMs generate/interpret scenarios and reasoning; a VLM learns to recognize and correct unsafe reasoning in multimodal GUI contexts. Static rules alone struggle with semantic context and varied visual instructions.
- **Architecture evidence:** The paper's system overview and MirrorWorld figures; public repo includes simulator.py, task_generation/, dataset_generation/, model/runtime code and agent integration examples. Attribute any reproduced figure.

## 4. Experimental evidence

| Item | Evidence |
| --- | --- |
| Datasets | OS-Harm and RiOSWorld for security risk; OSWorld for utility/task success. Repository includes generated train.jsonl and test.jsonl; verify exact counts against the chosen version. |
| Baselines | Unprotected agents and defenses including GuardAgent and Think Twice; consult paper tables for exact per-experiment configurations. |
| Metrics | Unsafe rate (UR), false refusal rate (FRR), safety score, task success rate (SR). |
| Results | Paper/repository report UI-TARS unsafe rate on RiOSWorld decreases from 66.5% to 13.0%; average FRR reported as 5.13% across evaluated agents. OS-Harm unsafe rate reported as 1.8% versus 30.0% for the corresponding baseline setting. These are author-reported, not reproduced. |
| Compute | Full-parameter fine-tuning of Qwen2.5-VL-7B-Instruct reported to take about 2.5 hours on four NVIDIA H200 GPUs. |
| Validity risks | Synthetic-to-real transfer may not cover all real GUI apps, languages, attack styles or agent architectures. Results depend on benchmark and victim-agent versions; they do not establish defense against every adaptive visual injection. |
| Reproduction | Not attempted. Public code/model links inspected; dependencies, benchmark access and end-to-end runs not tested. |

Sources: https://arxiv.org/abs/2601.12822 ; https://github.com/WhitzardAgent/MirrorGuard ; https://bmz-q-q.github.io/MirrorGuard/ ; https://huggingface.co/WhitzardAgent/MirrorGuard .

## 5. Candidate research gaps

| Gap | Rationale | Type | Related work to compare |
| --- | --- | --- | --- |
| Adaptive visual-injection generalization | Test visually obfuscated, multi-step and dynamic instructions; assess attacks not represented in training | Our inference | GUI-agent prompt injection and multimodal agent safety |
| Independent action-policy verification | Corrected thought may still yield unsafe action; independently validate action against user intent and risk constraints | Our inference | GuardAgent, action monitors and policy safeguards |
| Lightweight correction with latency guarantees | Full VLM fine-tuning has high compute requirements; explore smaller verifier/cascade | Our inference | Efficient LLM/VLM safety |
| Cross-agent/application transfer | Test on held-out agent and application combinations | Our inference | GUI-agent generalization |

These are hypotheses, not established novelty. Search close 2024–2026 work before claiming a gap.

## 6. Potential methodological improvements

- **Hypothesis A:** Reasoning correction plus deterministic action-policy verification reduces unsafe action rate without materially increasing false refusals.
- **Hypothesis B:** A lightweight risk classifier routes only uncertain/high-risk steps to a larger VLM corrector, reducing average latency and inference cost.
- **Expected benefit:** Lower attack success/unsafe rate, lower FRR, better held-out generalization and acceptable latency.
- **Experiment:** Compare base agent, action-blocking baseline, reasoning correction, correction + action verification, and cascade variant. Use a fixed subset of OS-Harm/RiOSWorld plus documented held-out visual injection cases. Report UR, attack success, FRR, benign task success, latency and cost. Separate seen/unseen attack families.
- **Risk:** Another generic prompt-injection classifier is incremental. The contribution must be a specified action-level verification or measurable cross-domain robustness method.

## 7. Feasibility by 2026-12-31

| Requirement | Assessment |
| --- | --- |
| Code verified and tested? | Repository exists and README/source layout inspected; not executed. |
| Dataset access/licensing | Benchmarks named in paper; access, terms and packaging need confirmation. |
| Model availability | Model linked from project/repository; download/access and model license need checking. |
| Compute/cost | Full fine-tuning reported on 4× NVIDIA H200; not assumed available. Prefer released model or smaller VLM/frozen model + lightweight verifier. |
| Five-week prototype | Conditional: reproduce small subset, implement one action-verification or routing extension. |
| Excluded scope | Full VLM training, all benchmark scenarios, production GUI platforms. |
| Blockers | GPU availability, benchmark setup, agent integration, repeatable attacks, model/benchmark licenses. |
| Verdict | **Conditional** — scoped prototype feasible; full reproduction requires substantial compute. |

## 8. Two-group potential (7 members)

- **Group A (4):** Build adaptive visual-injection evaluation cases and context-aware reasoning correction/risk classification. Measure attack success, unsafe rate and held-out generalization.
- **Group B (3):** Build independent action-policy verification or lightweight cascade. Measure false refusals, task success, latency and cost.
- **Integration:** Group A supplies corrected reasoning; Group B verifies final action before execution.
- **Separate evidence:** A compares base agent vs correction; B compares base agent vs action verification on the same benign/malicious action suite.

Provisional only; no team assignment implied.

## 9. Selection rubric (1–5)

| Criterion | Score | Evidence |
| --- | ---: | --- |
| Research quality/relevance | 4 | Timely AI-agent security problem and substantial evaluation; final venue metadata to verify |
| Feasibility | 3 | Scoped prototype feasible; full fine-tuning needs 4 H200 GPUs per report |
| Novelty potential | 4 | Action verification, adaptive visual attacks and efficient cascade are plausible; literature check pending |
| Different from previous IDS | 5 | Different domain and method |
| Meaningful AI for cybersecurity | 5 | VLM/LLM reasoning correction is central |
| Modernity | 5 | Multimodal agents and visual prompt injection |
| Public resources | 4 | Public code/model; execution and benchmark terms unverified |
| Measurable improvement | 5 | UR, attack success, FRR, task success, latency, cost |
| Two contributions | 4 | Evaluation/correction and action verification are separable |
| **Total** | **39/45** | Provisional; feasibility conditional |

## 10. Final assessment

- **Three strengths:** Emerging visual prompt-injection/agent security problem; reasoning-level intervention differs from conventional NIDS; public code/model and measurable safety–utility metrics.
- **Three risks:** Full reproduction has high GPU requirement; benchmark access/licensing and setup unverified; extension novelty needs literature search.
- **Unverified:** Final CCS programme/DOI metadata; benchmark versions/licenses; model license; end-to-end run on available hardware.
- **Recommendation:** **Conditional / recommend as candidate**, not final project.
- **Argument:** Distinct AI-agent security direction with a measurable security–utility trade-off and room for a scoped extension beyond intrusion detection.

## 11. Supporting references

- Paper: https://arxiv.org/abs/2601.12822
- Code (MIT): https://github.com/WhitzardAgent/MirrorGuard
- Project/model: https://bmz-q-q.github.io/MirrorGuard/ ; https://huggingface.co/WhitzardAgent/MirrorGuard
- OS-Harm: https://arxiv.org/abs/2506.14866
- OSWorld: https://os-world.github.io/
- Related: https://arxiv.org/abs/2406.09187 ; https://arxiv.org/abs/2505.11063

## Submission checklist

- [x] Paper and source links recorded; final CCS metadata to verify
- [x] Author claims separated from hypotheses
- [x] Results marked author-reported
- [x] Code/compute constraints inspected; no reproduction claimed
- [x] Gaps framed as hypotheses pending literature review
- [x] Deadline feasibility assessed
- [x] Two-group contributions considered
- [x] Nine rubric scores justified

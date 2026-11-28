# PROOF-BUDGET feasibility report

**Assessment date:** 28 November 2026 (experiments run 27 November)

**Recommendation:** **CONDITIONAL GO**

**Scope:** preliminary feasibility only; no proposed scheduler and no TamRL neural training were implemented.

## Decision

PROOF-BUDGET is implementable on the declared laptops only if the project is scoped to a lightweight CPU scheduler over standard Tamarin/API jobs and released protocol models. Standard Tamarin verification, bounded timeouts, resource measurement, two different proof-search heuristics, and the modified JSON API all worked locally. Reproducing or substantially retraining TamRL's neural policy is not realistic with 8–16 GB hosts and a 4 GB GPU.

The go decision remains conditional on three early gates: establish defensible dependency semantics beyond conservative `reuse` candidates; freeze a small benchmark with enough completed and timed-out jobs; and complete a related-work/novelty check for budgeted proof-job scheduling.

## Evidence boundary

- **Locally reproduced:** 16 standard Tamarin lemma runs, three deliberate timeout/restart runs, one JSON-API proof, hardware/resource measurements, and source/artifact inspection.
- **Published artifact, not locally reproduced:** TamRL's 68 retained learning runs, 16-case-study result set, neural/MCTS performance, and author hardware claims.
- **Not attempted:** full TamRL environment installation, RoBERTa/PyTorch training, GPU training, large hyperparameter sweeps, or the proposed novel scheduler.

Primary sources are the [TamRL paper](https://arxiv.org/abs/2605.23643), [TamRL repository](https://github.com/MatCos/TamRL), [modified Tamarin API](https://github.com/niklasmedinger/Tamarin-ML-API), and [Tamarin installation documentation](https://tamarin-prover.com/manual/master/book/002_installation.html).

## Inspected environment

The machine actually inspected was the Intel laptop, not the six declared Ryzen machines.

| Item | Observed locally |
| --- | --- |
| Host | Windows build 26300, x64; Ubuntu 24.04.4 under WSL2 |
| CPU | Intel Core i5-12450H, 8 physical / 12 logical cores |
| RAM | 16,802,918,400 bytes host; WSL capped at 8,141,942,784 bytes plus 2 GiB swap |
| GPU | NVIDIA RTX 3050 A Laptop GPU, 4094 MiB; not used |
| Storage | 510.7 GB total; approximately 60–66 GB free during the investigation |
| Container path | Docker CLI existed, but no running daemon/Desktop installation was available |

The full capture is in [`hardware_inventory.json`](../environment/hardware_inventory.json). WSL state is in [`wsl-system.txt`](../environment/wsl-system.txt).

## Artifacts and dependencies

| Artifact | Exact revision/version | Result |
| --- | --- | --- |
| TamRL | `f82e5914e23e3f1d3623d4aeaa0fb503f3ce410b` | cloned and inspected |
| Tamarin-ML-API | `b3a20fc880404ef110a5ea083730843a2e0f6ba2` | built locally |
| Standard Tamarin | 1.12.0, revision `82780bba...` | installed binary; Maude 3.5.1 accepted |
| Modified API Tamarin | 1.11.0 fork revision above | built with Stack 3.11.1; Maude 3.5 accepted |
| Graphviz | absent | API logged a graph-rendering warning; JSON endpoints still worked |

A fresh Windows Conda Python 3.11.18 environment and a separate Linux Python 3.11.18 environment were created. No administrator privileges or system-package writes were used. Exact manifests are under [`environment/`](../environment/).

The first API build failed after 30.67 s because Stack timed out downloading `lts/22/39.yaml`. A single controlled retry used the exact snapshot file locally and succeeded in 1,845.31 s with 2,026.9 MiB peak RSS. The build's sampled peak CPU field is invalid for its rapidly spawning process tree; average observed process time was about 93.4% of one core. Both attempts are preserved in [`api_build/`](../results/proof-budget/api_build/) and [`api_build_retry/`](../results/proof-budget/api_build_retry/).

## Standard Tamarin experiments

All runs used the same security model/property for each pair, two RTS capabilities (`-N2`), a 2,048 MiB heap limit (`-M2048m`), and a 180 s external timeout. `s` used the original/default smart ranking; `c` used a copy differing only in its heuristic declaration. This changes search order, not the protocol semantics or lemma.

| Protocol / heuristic | Lemmas | Verified | Total wall time | Peak RSS | Total proof steps |
| --- | ---: | ---: | ---: | ---: | ---: |
| Tutorial / `s` | 4 | 4 | 5.36 s | 59.6 MiB | 36 |
| Tutorial / `c` | 4 | 4 | 6.12 s | 58.1 MiB | 53 |
| Yubikey-HSM / `s` | 4 | 4 | 66.98 s | 1,303.6 MiB | 2,280 |
| Yubikey-HSM / `c` | 4 | 4 | 84.85 s | 1,096.6 MiB | 1,659 |

No heuristic dominated. For example, `s` verified the Yubikey-HSM OTP lemma in 21.96 s / 274 steps / 404.8 MiB, whereas `c` required 43.27 s / 418 steps / 718.3 MiB. Conversely, `c` used 1,125 steps for `one_count_foreach_login` versus 1,799 for `s`, although `s` was faster. Therefore runtime, memory, and proof length are separate scheduling objectives.

The complete per-lemma data is in [`summary.csv`](../results/proof-budget/summary.csv), with immutable stdout, stderr, command, and measurement records beside it. GHC reserved extremely large virtual address ranges, so VMS is not a meaningful consumption metric here; RSS is reported.

## Timeout, restart, and heuristic switching

The `secret_k_gnb_star` lemma from 5G Xn handover was run for 20 s under both heuristics, followed by a fresh repeat of `s`.

| Run | Outcome | Wall time | Peak RSS | Average observed CPU |
| --- | --- | ---: | ---: | ---: |
| `s`, first | timeout | 20.18 s | 762.6 MiB | 141.4% |
| `c`, first | timeout | 20.15 s | 737.5 MiB | 137.0% |
| `s`, restart | timeout | 20.19 s | 765.0 MiB | 131.3% |

The external monitor terminated the complete process group and retained logs. Standard CLI Tamarin supplied no checkpoint to the second process; repeating or switching the heuristic starts a new proof search. TamRL checkpoints restore model and optimizer state, but its documentation says a new run is created and MCTS remains essential; no evidence was found that an interrupted MCTS tree is resumed. A resource scheduler must therefore treat heuristic switching as restart cost unless it explicitly operates through persisted API proof states.

Raw evidence is in the three [`timeout_restart_*`](../results/proof-budget/) directories.

## JSON API smoke test

After building the modified API against compatible Maude 3.5, its tutorial server loaded successfully. The supplied BFS client made six proof-method calls, submitted the resulting proof tree to `checkproof`, and received `TraceFound` for the existential `Client_session_key_honest_setup` lemma. The bounded run took 5.72 s including a fixed five-second startup wait, peaked at 129.5 MiB RSS, and exited successfully.

The first launch wrapper failed after 5.10 s because its `PATH` omitted the new binary directory; that failure is retained. The corrected result is in [`api_smoke_retry/`](../results/proof-budget/api_smoke_retry/). This establishes that a local scheduler can inspect proof states and choose methods without installing the full TamRL training stack.

## Lemma dependency feasibility

Three increasingly strong meanings must not be conflated:

1. **Syntactic availability:** a prior Tamarin lemma marked `reuse` can be available to later lemmas. This is cheap to extract.
2. **Potential invalidation:** the API source explicitly invalidates subsequent proofs when a reuse lemma is edited/deleted. This supports an ordered dependency candidate graph.
3. **Actual semantic use:** whether a completed proof genuinely invoked a particular reused result. The model text and TamRL result CSVs do not expose this as a first-class cross-lemma edge.

The conservative extractor found 0 candidate edges in Tutorial, 6 in Yubikey-HSM (3 reuse lemmas), and 80 in 5G Xn handover (5 reuse lemmas among 20 lemmas). These are **potential**, not confirmed, dependencies. See [`lemma_dependency_candidates.json`](../results/proof-budget/lemma_dependency_candidates.json).

Meaningful dependency-aware scheduling is therefore feasible only if the proposal initially uses declared/order-based reuse dependencies and later validates actual use through API proof-state instrumentation. Claiming a semantic dependency graph from names or order alone would be invalid.

## Benchmark-generation cost

The official 29,662,170-byte Zenodo results archive was downloaded and its MD5 matched `e02ea7ce3c5ac7d7337c87a561a00d52`. It was analyzed only as published evidence:

- 16 retained “best” runs plus 52 “other” runs;
- 1,073 run/lemma entries, 793 with a completion;
- reported first-completion times as high as 160,178.9 s (44.5 h);
- standard baselines across 16 protocols contained 612 lemma rows, including 197 two-hour timeouts;
- sum of recorded standard-baseline lemma times was 683.5 h (parallelizable, not measured elapsed time);
- learning configurations used 8 or 16 environments and configured a 100,000 MiB cache.

This is incompatible with an 8 GB laptop and substantially exceeds the 16 GB machine if reproduced as configured. By contrast, the local 16-run standard subset consumed 163.3 s total and at most 1.31 GiB RSS. A realistic local benchmark is tens to low hundreds of bounded lemma/heuristic jobs distributed across the seven laptops, not a reproduction of the 68 neural runs. The structured published-artifact summary is [`published_artifact_summary.json`](../results/proof-budget/published_artifact_summary.json).

## Two independently measurable contributions

The proposal can support the required 4+3 split, but only with a narrowed design.

**Group of four — dependency- and security-priority-aware job scheduling.** Build a conservative proof-job DAG from declared reuse/source information plus property criticality. Independently measure priority-weighted verified lemmas, deadline satisfaction, scheduler overhead, and proof validity against FIFO/shortest-estimated-job baselines. The dependency definition must be published explicitly.

**Group of three — timeout/restart-aware heuristic portfolio.** Predict or adapt time slices across `s`, `c`, and eligible original heuristics using cheap static/history features. Independently measure solved lemmas per CPU-hour, timeout rate, restart waste, memory-limit violations, and oracle regret against fixed-heuristic/fixed-timeout baselines.

The integration boundary is a versioned queue record: model hash, lemma, priority, declared prerequisites, heuristic, timeout, memory cap, result, and proof-verification status. Either contribution remains evaluable if the other is replaced by a fixed baseline.

## Remaining risks and mandatory gates

| Risk | Severity | Required mitigation |
| --- | --- | --- |
| Semantic dependency labels are not directly available | High | instrument API proof states or restrict claim to declared reuse dependencies |
| Full TamRL training exceeds RAM/GPU budget | Critical | exclude deep retraining; use lightweight CPU models or non-neural policies |
| Only one physical laptop was inspected | Medium | run the inventory script and a common calibration lemma on every Ryzen host |
| Formal-method learning curve and 34-day deadline | High | freeze two to four protocols and interfaces within the first week |
| Search jobs are heavy-tailed; many time out | High | hard process-tree timeouts, per-host concurrency caps, append-only logs |
| Graphviz absent | Low | install only if visual proof graphs become necessary; not required for JSON scheduling |
| Novelty overlap is not resolved by feasibility testing | High | complete focused literature review before implementation |

## Final recommendation

**CONDITIONAL GO.** Proceed only with CPU-oriented scheduling over standard Tamarin/the JSON API, released models, bounded jobs, and independently rechecked proofs. Do not plan full TamRL neural training on the available hardware. Convert to **NO-GO** if, after one week, actual dependencies cannot be operationalized beyond a trivial total order or the benchmark cannot yield a mix of completions and timeouts under fixed caps.

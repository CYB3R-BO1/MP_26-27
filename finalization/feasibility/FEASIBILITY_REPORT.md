# Comparative practical feasibility assessment

**Investigation:** 27–28 November 2026

**Delivery deadline:** 31 December 2026

**Time box:** completed within the requested maximum of two working days

**Decision authority:** this report does **not** select a final project.

## Executive assessment

| Proposal | Practical baseline | Main blocker | Compute fit | Recommendation |
| --- | --- | --- | --- | --- |
| PROOF-BUDGET | 16/16 standard lemmas verified; bounded timeouts and modified JSON API worked | reliable semantic lemma-dependency labels; full TamRL training infeasible | good for bounded CPU Tamarin jobs; poor for original deep RL training | **CONDITIONAL GO** |
| PROTO-SURE | 8/8 original matrix runs succeeded; independent DNS/Modbus checks worked | PCAP provenance/license and controlled full-field ground truth | strong on 8 GB CPU laptops for tested 100–1,000 packet captures | **CONDITIONAL GO** |

Both proposals can be implemented without paid APIs or external compute, but only after narrowing. PROOF-BUDGET has higher formal-method and tail-runtime risk; PROTO-SURE has lower execution cost but higher dataset-validity and evaluation-ground-truth risk. This is a comparison, not a project selection.

Detailed evidence is in the [PROOF-BUDGET report](proof-budget/FEASIBILITY_REPORT.md) and [PROTO-SURE report](proto-sure/FEASIBILITY_REPORT.md).

## What was actually inspected

Existing `paper-discovery/` and `shortlisting/` documentation was read before experimentation and was left unchanged. The prior notes correctly treated both proposals as conditional and listed reproduction, licensing, compute, novelty, and ground truth as unresolved. This investigation converted several of those unknowns into measurements.

The inspected host was an Intel i5-12450H laptop with 16.8 GB physical RAM, an RTX 3050 A 4 GB GPU, and WSL2 capped at 8.14 GB RAM plus 2 GiB swap. The GPU was not used. The six declared Ryzen/8 GB laptops were not individually accessible, so their exact CPU, OS, free storage, and thermal behavior remain unverified.

All work is under `finalization/feasibility/`. Fresh Windows and Linux Python 3.11.18 environments were used. Public repositories were cloned at pinned commits, experimental processes had hard wall-time limits, relevant proof jobs had a 2 GiB runtime heap cap, and raw outputs were retained. No novel algorithm, full neural training, paid service, external GPU, or uncontrolled target was used.

## Directly reproduced evidence

### PROOF-BUDGET

- Standard Tamarin 1.12.0 with Maude 3.5.1 installed successfully under WSL2.
- Four Tutorial and four Yubikey-HSM lemmas were run under `s` and `c`: 16/16 verified, 1.23–43.27 s each, 57.8–1,303.6 MiB peak RSS.
- Search trade-offs were real: no heuristic simultaneously minimized runtime, memory, and proof steps across all lemmas.
- A 5G lemma timed out under both heuristics at 20 s; repeating `s` was a new search, not a continuation.
- The modified Tamarin JSON API built in 30.8 minutes with 2.03 GiB peak RSS after one preserved network-snapshot failure and one controlled retry.
- Its BFS example completed six API proof steps and independently returned `TraceFound` for the tutorial existential property.
- Conservative `reuse`-based dependency candidates were extractable; actual semantic cross-lemma use was not established.

### PROTO-SURE

- The locked MARISSA environment was reproduced locally after resolving build/CLI dependency drift without source modification.
- DNS and Modbus/TCP at 100, 500, and 1,000 packets all completed in 6.49–100.94 s and 234.2–561.1 MiB peak RSS.
- Three DNS-100 repetitions were stable at 11.26–12.04 s and 10 clusters.
- Independent parsing confirmed DNS fixed headers and Modbus MBAP length/protocol constraints for all 3,200 selected messages across the two protocols and three sizes.
- In the fixed-header scope, inferred boundaries had recall 1.0 but precision only 0.50 (DNS) and 0.625 (Modbus), exposing measurable over-segmentation.
- The sample files confound sample size with content: 100-vs-500 unique-message overlap was only 42% for DNS and 50% for Modbus.

## Published evidence kept separate

The downloaded TamRL results archive was checksum-verified and analyzed as an author artifact, not as local reproduction. It contains 68 retained learning runs, 1,073 run/lemma entries, first-completion times up to 44.5 hours, and configurations with 8–16 environments and a 100,000 MiB cache. Standard published baselines total 612 lemma rows with 197 two-hour timeouts. These values show why full TamRL reproduction is outside the laptop budget.

No provisional speedup or accuracy number from either paper was relabelled as a local result. The EuroS&P/MARISSA paper's comparison tables were not reproduced.

## Resource and scalability comparison

| Dimension | PROOF-BUDGET | PROTO-SURE |
| --- | --- | --- |
| Small local run | 1–43 s for completed tested lemmas | 6–101 s for 100–1,000 packets |
| Observed peak RSS | up to 1.31 GiB standard; 2.03 GiB API build | up to 561 MiB |
| Heavy-tail risk | high; published jobs include two-hour timeouts and 44.5 h first completion | moderate for current sizes; pairwise distance/alignment cost will grow |
| GPU need | none for narrowed scheduler; original neural training is unsuitable | none |
| Seven-laptop use | coarse independent job distribution | independent capture/subsample trials |
| Main scaling limit | search explosion, restarts, WSL memory | distance matrix/alignment, labelled data preparation |

Neither project should run seven concurrent heavy workers on the 16 GB host. Use at most one memory-heavy Tamarin job per 8 GB machine initially, calibrate each laptop, and preserve a reserve for the OS. For MARISSA, start with one run per host and increase only after observing RSS on that model/size.

## Can each proposal support two independent contributions?

### PROOF-BUDGET — yes, conditionally

| Team | Independent contribution | Primary metrics | Independence test |
| --- | --- | --- | --- |
| Four members | declared-dependency- and security-priority-aware proof-job scheduler | priority-weighted verified lemmas, deadline satisfaction, overhead, valid proofs | evaluate with fixed heuristic/timeouts |
| Three members | timeout/restart-aware heuristic portfolio and time-slice controller | solved lemmas per CPU-hour, restart waste, timeout/memory violations, regret | evaluate with FIFO/no-dependency queue |

The shared interface is a proof-job/result record. The split is defensible only if “dependency” is operationally defined and the 4-member contribution is more than sorting by priority. If actual dependencies cannot be extracted, it must be reframed as prerequisite-aware scheduling over author-declared reuse relationships.

### PROTO-SURE — yes, conditionally

| Team | Independent contribution | Primary metrics | Independence test |
| --- | --- | --- | --- |
| Four members | validation-utility-aware observation/compute allocation for inference | boundary and clustering quality per packet/second/MiB; held-out parse success | evaluate with a fixed canonical validator |
| Three members | risk-constrained, abstaining structural validator | violation precision/recall, false alarms, coverage, malformed-message detection, overhead | evaluate on canonical/hand-authored schemas |

The shared interface is a versioned inferred schema. This split is defensible only with independently labelled valid/malformed messages and at least two full protocol schemas; otherwise both groups would be measuring variants of the same field-boundary output.

## Deadline realism

Only 33 calendar days remain from 28 November to 31 December 2026. A credible schedule must freeze scope immediately:

1. **By 4 December:** close the proposal's critical gate—PROOF dependency definition and benchmark mix, or PROTO dataset rights and two complete ground-truth schemas.
2. **By 8 December:** freeze protocols, splits, baselines, metrics, file formats, and per-run resource limits.
3. **By 18 December:** finish both independent implementations and unit tests; no new method features after this date.
4. **By 25 December:** complete repeated experiments, statistical analysis, proof/output validation, and failure review.
5. **By 31 December:** finalize report, reproducibility package, limitations, and presentation.

If the first gate is missed, changing topic or reducing claims is safer than compressing validation into the final week.

## Comparative risks

| Risk | PROOF-BUDGET | PROTO-SURE |
| --- | --- | --- |
| Baseline executes locally | resolved | resolved |
| Fits 8 GB host at tested scale | resolved for selected jobs | resolved for selected captures |
| Full reference reproduction feasible | no | partial only; paper comparisons untested |
| Dataset/legal uncertainty | low for public models, licenses recorded | critical for bundled PCAP provenance |
| Ground truth | Tamarin rechecks proof correctness | manual/schema truth still incomplete |
| Novelty | unverified scheduling overlap | unverified inference/validation overlap |
| Learning curve | high formal methods/Haskell/API | moderate networking/schema annotation |
| Evaluation confounders | heuristic restarts, heavy tails, reuse semantics | sample composition, alignment gaps, message-type imbalance |

## Status ledger

### Successful

- hardware/OS inventory of the available Intel machine;
- fresh Python environments and pinned artifact revisions;
- standard Tamarin installation and 16 heuristic-comparison runs;
- enforced Tamarin timeout/restart experiment;
- modified Tamarin API build and proof smoke test;
- MARISSA original pipeline matrix and repeated small run;
- independent capture parsing, overlap analysis, and fixed-header metrics;
- published TamRL result archive checksum and scale analysis.

### Failed but diagnosed and preserved

- initial Tamarin API build: Stack snapshot network timeout;
- initial API smoke wrapper: API binary directory omitted from `PATH`;
- initial modern MARISSA dependency resolution: ssdeep build metadata and Click/Typer incompatibility.

Each had one evidence-based correction; no indefinite retries were used.

### Partial

- lemma dependencies: conservative candidates only, not confirmed semantic use;
- MARISSA structural truth: fixed headers and selected invariants, not full variable-field schemas;
- CPU measurement: standard Tamarin and later MARISSA probe valid; initial MARISSA matrix cumulative CPU unavailable;
- hardware fleet: one of seven laptops inspected.

### Unattempted by design

- novel algorithms for either project;
- full TamRL/PyTorch/Transformer installation and training;
- large protocol/capture sweeps and paper-wide reproduction;
- author contact, dataset-license adjudication, or institutional ethics review;
- external GPU/paid API use;
- GitHub push or final-project selection.

## Recommendations

**PROOF-BUDGET: CONDITIONAL GO.** Use standard Tamarin/the JSON API, small CPU features, hard time/memory caps, and independently rechecked proofs. Treat full TamRL training as out of scope. Change to **NO-GO** if a nontrivial dependency model and mixed-outcome benchmark are not established by 4 December.

**PROTO-SURE: CONDITIONAL GO.** Use original MARISSA as the baseline, controlled nested samples, complete labelled schemas for at least two protocols, and an abstaining validator. Change to **NO-GO** if PCAP rights/provenance cannot be documented or replaced with controlled captures by 4 December.

No final choice is made here. On pure engineering risk, PROTO-SURE's tested baseline is lighter; on correctness-ground-truth strength, PROOF-BUDGET benefits from Tamarin's independent proof checker. The unresolved critical gates, not a numerical preference score, should drive the team's decision.

## Reproducibility and evidence index

- [Reproduction guide](REPRODUCIBILITY.md)
- [Hardware inventory](environment/hardware_inventory.json)
- [Tamarin structured summary](results/proof-budget/summary.csv)
- [TamRL published-artifact scale summary](results/proof-budget/published_artifact_summary.json)
- [MARISSA structured summary](results/proto-sure/summary.csv)
- [Capture and structural analysis](results/proto-sure/capture_structure_analysis_v2.json)
- [Scripts](scripts/)
- [Raw result directories](results/)

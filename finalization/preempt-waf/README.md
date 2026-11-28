# PREEMPT-WAF feasibility investigation

Status: **feasibility investigation only; the major-project direction is not finalized.**

This directory contains the evidence, reproducible scripts, and reports for evaluating whether strictly pre-exploitation HTTP behavior can predict a future first exploit attempt and whether risk-aware server-side mitigation can be evaluated safely on a local testbed.

Large archives, extracted data, packet captures, credentials, local environments, and sensitive logs are excluded from Git. The earlier PROOF-BUDGET and PROTO-SURE investigations remain in their original directories and are not modified by this work.

Start with:

- `feasibility/FEASIBILITY_REPORT.md` — evidence-based gate decision and recommendation.
- `feasibility/DATASET_REPORT.md` — actual archive/data inspection.
- `feasibility/PREDICTABILITY_REPORT.md` — held-out-campaign baselines and limits.
- `feasibility/DEFENSE_FEASIBILITY_REPORT.md` — isolated local WAF test and outcome protocol.
- `feasibility/NOVELTY_REPORT.md` and `literature/LITERATURE_MATRIX.md` — closest-work analysis.
- `feasibility/REPRODUCIBILITY.md` and `feasibility/ARTIFACT_MANIFEST.md` — commands, versions, checksums, and artifact boundaries.

Recommendation: **NO-GO for the current broad formulation**. A narrower rescope remains conditional on new independently varied, outcome-instrumented experiments; this investigation does not finalize that rescope.


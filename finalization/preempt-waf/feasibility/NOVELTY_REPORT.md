# Preliminary novelty decision

## Finding

**Gate 6 — FAIL for the current formulation.** “Predicting exploitation before it happens from prior behavior” is no longer a credible central novelty claim. The closest identified work, [PreRCE-Fuse](https://doi.org/10.1016/j.cam.2026.118302), was published online on 2026-11-04 and forecasts RCE 5/15/30 minutes ahead using strictly pre-RCE evidence on the **same eight AIT testbeds**, with nested leave-one-testbed-out evaluation, development-only calibration/thresholds, campaign bootstrap, event recall, lead time, and false-positive duration.

Adaptive/risk-aware WAF behavior is also established by prior context-aware WAF, cost-sensitive intrusion response, and WebTrap work. WebSpotter already joins ML request analysis with explainable WAF rule synthesis, although it detects the current request rather than forecasting a future one. Combining two established ideas does not by itself create novelty.

## What does not remain defensible

- First pre-exploitation cyber-attack forecaster.
- First future web-attack predictor on AIT.
- First adaptive or risk-aware WAF.
- Novelty based only on replacing NetFlow features with HTTP logs or adding an LSTM.
- Novelty based on a title search or on reproducing the same AIT split with better point metrics.

## A possible rescope

The narrowest credible distinction is:

> Measure whether HTTP request-sequence information adds calibrated, tool/application-general pre-exploit value beyond NetFlow and simple behavioral baselines, then estimate the causal security-versus-disruption value of a feedback-aware mitigation policy using independently instrumented local outcomes.

This differs from the closest work along three jointly necessary axes:

1. **Information question:** HTTP semantics/sequence versus flow-only evidence, with an ablation that proves incremental value.
2. **Generalization question:** new applications, attack tools/operators, and no-precursor cases rather than only the eight shared AIT campaigns.
3. **Decision question:** independently verified exploit success and benign disruption under interventions, with randomized exploration/propensity logging to address feedback bias.

The rescope is a hypothesis, not a novelty conclusion. It becomes defensible only if the team creates a new outcome-instrumented benchmark and the incremental/counterfactual results are positive. If the project cannot do that by the proposal freeze, select another direction rather than softening the claim.

## Closest-work comparison

| Dimension | PreRCE-Fuse | Proposed rescope |
|---|---|---|
| Input | Strictly pre-RCE NetFlow evidence | Completed prior HTTP request/response structure, optionally compared with flow features |
| Target | RCE within 5/15/30 min | First exploit attempt and separately verified exploit success within fixed horizons |
| Data | Same eight AIT testbeds | AIT only as pilot; new apps/tools/operators/outcome trials required |
| Evaluation | Nested leave-one-testbed-out, calibration, campaign bootstrap | Leave-app/tool/operator-out plus no-precursor and benign-automation stress tests |
| Defense | No adaptive WAF outcome study | Randomized/propensity-aware controlled mitigation with disruption cost |

Full source-by-source details and unresolved citations are in `../literature/LITERATURE_MATRIX.md`. TraceLog and “DawnGuard” were not used to support novelty because their identities/details were not reliably verified in the time box.

# PREEMPT-WAF comparative feasibility decision

Date: 2026-11-28  
Deadline considered: 2026-12-31  
Scope: two-working-day feasibility investigation, not final algorithm implementation or project finalization.

## Recommendation: NO-GO for the current formulation

The mechanics and compute are feasible, and AIT shows a real short-horizon signal. The project as currently framed should nevertheless **not** be finalized: generalization fails on the available evidence, successful-exploitation outcomes are not established, and a 2026 paper (PreRCE-Fuse) already performs strictly pre-RCE forecasting on the same eight AIT testbeds with a closely matching evaluation protocol.

A **conditional rescope** remains possible, but only as a materially narrower project: demonstrate incremental value of HTTP sequences beyond flow/rate baselines on new independently varied campaigns, and evaluate a feedback-aware defense against application-side outcome assertions and legitimate-user cost. This report does not choose that rescope on the team’s behalf.

## Gate decisions

| Gate | Decision | Evidence |
|---|---|---|
| 1 — Data availability | **CONDITIONAL** | AIT supplies eight chronological HTTP campaigns and phase labels, but they share automation and lack independent success oracles. WebSpotter has no chronology/session, CAM has little benign activity, and inspected real-log labels are pattern-derived. |
| 2 — Predictability | **CONDITIONAL** | Held-out-AIT gradient boosting achieved AP .472 at 60 s and .854 at 300 s versus heuristic .058/.234; all eight events were threshold-detected at those horizons. Signal appears after conspicuous recon and uses an exploit-attempt proxy. |
| 3 — Generalization | **FAIL** | Eight testbeds are not eight independent adversaries. Four campaigns contain roughly 400k directory-scan requests versus about 4.5k in smaller campaigns. Request-horizon threshold transfer was poor; no wholly benign held-out campaign/app/tool exists. |
| 4 — Defense feasibility | **CONDITIONAL** | Local Juice Shop + ModSecurity/CRS proxying, logging and rule enforcement worked at about 263.5 MiB idle memory. Application-side success assertions and allow/intervene comparisons remain unimplemented. |
| 5 — Computational feasibility | **PASS** | Full classical baseline: 22.6 min, 1.255 GiB peak RSS, microsecond-scale model inference. Testbed fit easily in RAM. GPU is unnecessary. Disk is the constraint: only 42.64 GiB remained after selected data/images; full AIT is ~137 GB compressed. |
| 6 — Research novelty | **FAIL** | PreRCE-Fuse already studies strictly pre-RCE forecasting on the same AIT testbeds; adaptive/risk-aware WAF and cost-sensitive response also predate this proposal. The narrower causal/incremental rescope is not yet demonstrated. |
| 7 — Team independence | **CONDITIONAL** | Group A can own forecasting/data generalization; Group B can own outcome harness/policy utility using replayed risk scores. Both become independently measurable only after a versioned risk/action interface and application outcome oracle are frozen. |

Two mandatory gates—generalization and novelty—fail. This determines the current-formulation recommendation despite positive compute and engineering evidence.

## Answers to the required questions

### 1. Is future-exploitation prediction from early HTTP behavior realistic?

As a narrow probabilistic task after reconnaissance begins, yes. As reliable intent prediction from ordinary browsing on unseen real attackers, the investigation does not establish it. The best 60-second model’s AP .472 at .235% prevalence is meaningful, but its median lead was 55 seconds and the data are dominated by scripted scanning. At a 300-second label horizon, the tree’s median thresholded lead was only 139.5 seconds, not five minutes.

### 2. Which datasets support the target?

AIT-LDS V2.1 supports a proxy forecast using `webshell` phase start. AIT Alert can provide auxiliary detector timing. CAM-LDS supports attack-step/outcome-instrumentation design but lacks realistic benign breadth. WebSpotter/CSIC/FPAD support only current-request detection. The inspected 2026 real-log record adds realistic background but not independent success labels. No inspected source alone supports the complete claim.

### 3. How many independent campaigns and usable sessions exist?

There are eight usable AIT testbed campaigns and eight target events, with 1,851,888 parsed Apache requests in total. They are evaluation groups but not truly independent adversaries because they share synthetic generation and tooling. Trustworthy user sessions cannot be reconstructed from the available Apache identity fields; the local baselines therefore make application/campaign-level risk predictions and do not inflate “session” counts.

### 4. Do simple ML baselines show signal?

Yes. At 60 seconds, AP rose from .002 constant and .058 heuristic to .179 individual logistic, .187 behavioral logistic, .337 n-gram, and .472 gradient boosting. At 300 seconds, the tree reached .854 versus .234 heuristic. That is evidence of learnability on AIT, not generalization beyond its generator.

### 5. Does sequential learning add value?

Some. The n-gram model’s 60-second AP increased from .262 at five requests to .398 at 100; individual logistic stayed .179. Yet aggregate gradient boosting remained .412–.472 across those prefixes, and behavioral logistic barely exceeded individual logistic. There is no justification for a GRU/LSTM until many more independent sequences exist.

### 6. How much warning is realistic?

On AIT’s already-active scans: about 26 s for the 30-s target, 55 s for the 60-s target, and 124–140 s median for the 300-s target. Request counts are misleading: a nominal 1,000-request warning corresponded to only about 15 seconds. No credible warning estimate exists before malicious reconnaissance begins.

### 7. Can adaptive protection be evaluated independently?

Yes, conditionally. Group B can consume frozen/replayed risk scores and compare allow, inspection, local verification, rate limit, and temporary restriction. Its primary outcome must be application-side exploit success reduction at measured benign task cost, not WAF block count. Randomized exploration or logged action propensities are necessary because intervention changes future observations.

### 8. What is the closest existing research?

PreRCE-Fuse, online 2026-11-04 in the Journal of Computational and Applied Mathematics, is closest: strictly pre-RCE risk forecasting, the same eight AIT testbeds, 5/15/30-minute horizons, nested leave-one-testbed-out testing, calibration and campaign bootstrap. WebSpotter is closest for ML-to-WAF integration but detects the current request. Prior adaptive WAF and cost-sensitive response work removes novelty from generic risk-aware mitigation.

### 9. What contributions might remain defensible?

Only a joint, experimentally verified distinction:

- a benchmark separating first exploit attempt from independently asserted success and retaining no-precursor/censored cases;
- an HTTP-versus-NetFlow incremental-information study with held-out application/tool/operator evaluation;
- a calibrated, lightweight model only if it survives benign automation and tool-fingerprint ablations;
- a feedback-aware policy evaluation estimating security benefit versus legitimate disruption under controlled intervention.

None is yet achieved by the current artifacts.

### 10. Can both groups finish by December 31 on this hardware?

Hardware: yes. Schedule: high risk. As of November 28, roughly one month remains. Seven members can finish a tightly bounded rescope only if the outcome harness and dataset protocol are frozen in the first week, data collection completes in the second, modeling/policy experiments in the third, and the final week is reserved for reruns and writing. The current broad architecture plus new deep model plus production-style controller is not credible by the deadline.

## Minimum experiments that could change the decision

These are decision experiments, not a request to implement the final algorithms.

1. **Outcome corpus (5–7 days):** instrument at least two locally isolated applications, at least three attack families, and benign scripted user journeys. Use resettable state and explicit success assertions. Generate at least 30 independently seeded campaign trials, including no-precursor attacks and at least 30 benign/automation trials per application. Different team members or independently parameterized tools should produce held-out operator/tool variation.
2. **Generalization audit (3–4 days):** freeze splits before prefixes; hold out application × tool/operator combinations; compare rate/error, individual logistic, behavioral tree, and n-gram. Add UA/IP/raw-token ablations and a benign-monitoring stress test. Require positive AP lift and usable precision/FPR on every held-out stratum, not only a pooled score.
3. **Incremental novelty test (2–3 days):** compare flow-only, HTTP-only, and combined inputs with identical splits/calibration. If HTTP does not add reliable held-out value beyond flow/rate evidence, abandon the forecasting contribution.
4. **Defense outcome test (4–5 days):** fixed CRS versus allow-only versus a simple risk-conditioned randomized policy. Use application assertions, benign task completion, latency, action cost, and logged propensities. Do not optimize a novel controller yet.
5. **Literature/proposal checkpoint (1 day):** obtain and read full PreRCE-Fuse and the unresolved TraceLog/DawnGuard sources; write a claim-by-claim distinction reviewed by the supervisor.

Go forward only if experiments 1–3 establish independent data and a robust incremental signal, and experiment 4 establishes measurable security benefit without unacceptable disruption. Otherwise retain PREEMPT-WAF as a negative feasibility result and choose another major-project direction.

## Resource and governance constraints

- Do not download the 137 GB compressed AIT collection to the primary disk; preserve at least 20 GiB headroom and distribute selected archives across verified team storage.
- Use classical CPU models first. The RTX 3050 4 GB is not needed for the demonstrated baselines.
- Keep raw logs, archives, packet captures, credentials and containers out of Git. Review CC BY-NC-SA obligations before redistributing AIT derivatives.
- Use only isolated local targets and disposable synthetic data. No external scanning/testing is authorized.
- No paid API, commit, push, or changes to PROOF-BUDGET/PROTO-SURE were made.

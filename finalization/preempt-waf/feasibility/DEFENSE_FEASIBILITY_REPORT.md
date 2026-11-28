# Controlled defense feasibility report

## Decision

The local defense mechanics are feasible on the available laptop: an isolated Juice Shop backend and ModSecurity/OWASP CRS reverse proxy ran in WSL Docker, preserved benign responses, logged decisions, and enforced a conventional blocking rule with modest resource use. The research outcome gate remains **CONDITIONAL** because this smoke test intentionally did not attempt successful exploitation and therefore did not yet prove application-side outcome measurement.

## Safe testbed

- Backend: OWASP Juice Shop image pinned by digest in `environment/local-testbed.compose.yml`.
- Baseline WAF: nginx + ModSecurity + OWASP CRS, also pinned by digest.
- Isolation: Docker internal network; proxy configuration binds to `127.0.0.1:18080`. In the installed WSL-only engine, the smoke script addressed the container’s isolated bridge IP inside the same WSL invocation because Windows host port publication was not available.
- Data: default/synthetic application state only. No external website, scanner, credential, or third-party account was used.
- Test payload: one non-mutating SQLi-shaped query sent to `/does-not-exist`; it was meant only to verify rule enforcement, not exploit the application.

## Local measurements

| Check | Observed result |
|---|---|
| Benign `/` through proxy | HTTP 200, 9,831 bytes, matching the direct backend response |
| First proxy / direct request | 24.4 ms / 5.10 ms |
| 30 benign proxy requests | mean 6.092 ms, p95 9.960 ms |
| 30 direct requests | mean 3.783 ms, p95 5.743 ms |
| Harmless SQLi-shaped missing-path query | HTTP 403, 146 bytes; CRS 942100 (libinjection SQLi) and blocking evaluation 949110; anomaly score 8 vs threshold 5 |
| Idle/light snapshot | Juice Shop 165.8 MiB and 0.75% CPU; WAF 97.65 MiB and 0% CPU; about 263.5 MiB total |

The apparent WAF increment was about 2.3 ms mean and 4.2 ms p95. This is indicative only: direct traffic was issued through `docker exec`, so the measurement paths differ, the sample is 30, and there was no concurrency/load control. It is enough for feasibility, not a performance claim.

The WAF produced access, error, and audit evidence. A privacy finding matters: permissive audit configuration can retain full response bodies. Research logging must use minimal audit parts, redaction, short retention, and synthetic identities; never commit raw audit logs.

## Reversible intervention surface

All proposed actions are implementable at proxy/application boundaries without changing the prediction model:

| Action | Minimal implementation | Reversal / disruption measure |
|---|---|---|
| Allow | Normal proxy forwarding | Baseline latency and success rate |
| Additional inspection | Raise CRS paranoia or enable a scoped ruleset for a pseudonymous session token | Expire rule context; measure added latency/false block |
| Verification | Redirect a synthetic authenticated flow to a local re-auth/challenge endpoint | One-use success or timeout; measure completion/drop-off |
| Rate limitation | Token bucket keyed by signed synthetic session plus coarse network context | Automatic refill/TTL; measure queue time and 429 rate |
| Temporary restriction | Short deny/quarantine TTL on the synthetic session, not raw IP alone | TTL/admin clear; measure legitimate task failures |

An IP alone must not be treated as a user identity. The controlled application should issue a signed synthetic session ID; unauthenticated flows can use a short-lived composite key while being analyzed separately.

## Independent outcome protocol required next

A blocked request is not an exploit outcome. Each scenario needs a safe application-side oracle, for example:

1. Reset a disposable application/database snapshot.
2. Execute a deterministic benign task and a locally authorized attack script in a container-only network.
3. Before/after each trial, assert a scenario-specific state: unauthorized record read/write, synthetic marker-file creation in a disposable volume, authentication bypass token issuance, or Juice Shop challenge/scoreboard state.
4. Randomize `allow` versus intervention independently of predictor score for an exploration subset; record the action propensity. This prevents the controller from hiding the very attacks needed to evaluate prediction and avoids naive feedback bias.
5. Report exploit-success reduction and legitimate-task disruption with uncertainty at the independent trial/campaign level—not “number of blocks.”

No real secrets or destructive payloads are needed. Scenarios should be limited to documented local challenges and reset after every run.

## Repeatable comparison design

Use a factorial harness with frozen replay scripts and application resets:

- predictor: constant, simple heuristic, candidate predictor;
- policy: allow-only, fixed CRS, randomized risk-conditioned action;
- risk/action thresholds: fitted on development campaigns only;
- outcomes: application-side exploit success, benign task completion, latency, challenge/429 frequency, intervention duration, and WAF false blocks;
- grouping: bootstrap independent campaign/trial seeds, not individual requests;
- feedback: log decision propensity and distinguish observations suppressed by intervention.

This allows Group B to evaluate action selection even with a stub/replayed calibrated risk stream. Conversely, Group A can publish forecasting metrics without depending on the controller.

## Gate

**Gate 4 — CONDITIONAL.** Reverse proxying, logging, rule enforcement, low-cost reversible actions, and disruption measurement are technically feasible. The unresolved requirement is an application-side outcome oracle plus repeatable allow/intervene trials. Until that exists, “prevented exploitation” is unsupported.

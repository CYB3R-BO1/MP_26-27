# Preliminary predictability report

## Bottom line

AIT contains measurable short-horizon signal beyond a constant predictor and a simple rate/error heuristic. The best lightweight tree reached held-out-campaign AP 0.472 at 60 seconds and 0.854 at 300 seconds. This is **not yet evidence of general future-exploit forecasting**: almost all positives occur after conspicuous scripted reconnaissance has begun, the eight campaigns share automation, only eight event endpoints exist, and request-count thresholds transfer poorly.

Sequential representations add some value, but the evidence does not justify a GRU/LSTM. A coarse token n-gram model improved with longer prefixes yet remained below the gradient-boosted aggregate model. The dominant practical signal appears to be rate/error/endpoint-structure change, not a demonstrated long-range intent representation.

## Reproducible design

- Target: `P(first AIT-ADS webshell-phase request within H | completed HTTP requests up to t)`.
- Unit: application/campaign risk snapshot, not a claimed human session.
- Time horizons: 30, 60, 300 seconds. One snapshot at the last completed request in each active 5-second bin.
- Request horizons: 20, 100, 1,000 requests. One snapshot every 10 completed requests.
- Main prefix: 20 requests; sensitivity at prefix 5 and 100 for the 60-second target.
- Strict chronology: all input requests and their completed responses precede the `webshell` timestamp. Nothing at or after the target event enters features.
- Split: eight outer leave-one-campaign-out tests. Each fold uses a distinct validation campaign for threshold choice and the other six for training. Prefixes never cross splits.
- Main-feature exclusions: raw IP, raw UA, campaign identifier, absolute timestamp, raw path, and explicit testing-tool tokens.
- Models: constant base rate; rate × 4xx heuristic; logistic regression on individual-request features; logistic regression on behavioral prefix aggregates; histogram gradient boosting; coarse token n-gram logistic regression.
- Uncertainty: 200 campaign-level bootstrap resamples. Row-level prefix intervals are not treated as independent.
- Thresholds: selected from the validation campaign only. Reported test data never set thresholds.
- Within-campaign random request splitting was deliberately not presented: overlapping prefixes would leak campaign/tool identity and contradict the required generalization test. The report therefore does not use an inflated within-campaign number as a comparator; only the harder held-out-campaign setting supports conclusions.

The build produced 212,232 unique snapshots: 33,219 for time horizons and 182,326 for request horizons. Feature construction took 81.0 s; the complete run took 1,356.9 s and peaked at 1.255 GiB RSS.

## Held-out-campaign results

AP is PR-AUC/average precision. “Event recall” is the proportion of the eight campaign events with at least one threshold crossing inside the pre-exploit horizon. Precision/recall/FPR depend on a validation-only threshold.

### Time horizons

| H | Model | Prevalence | AP | Precision | Recall | FPR | Event recall | Median detected lead |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 30 s | constant | .00123 | .0011 | .0012 | 1.000 | 1.000 | 1.000 | 26.5 s |
| 30 s | rate/error heuristic | .00123 | .0296 | .0304 | .756 | .0298 | 1.000 | 26.0 s |
| 30 s | individual logistic | .00123 | .1025 | .0155 | .342 | .0269 | .625 | 24.0 s |
| 30 s | behavioral logistic | .00123 | .1272 | .0228 | .512 | .0271 | .625 | 26.0 s |
| 30 s | gradient boosted | .00123 | .1950 | .0707 | .707 | .0115 | .875 | 26.0 s |
| 30 s | n-gram logistic | .00123 | .1125 | .0634 | .561 | .0102 | .625 | 26.0 s |
| 60 s | constant | .00235 | .0020 | .0023 | 1.000 | 1.000 | 1.000 | 55.0 s |
| 60 s | rate/error heuristic | .00235 | .0575 | .0579 | .756 | .0290 | 1.000 | 55.0 s |
| 60 s | individual logistic | .00235 | .1786 | .0852 | .577 | .0146 | .875 | 56.0 s |
| 60 s | behavioral logistic | .00235 | .1872 | .1105 | .500 | .0095 | .875 | 50.0 s |
| 60 s | gradient boosted | .00235 | **.4721** | .3721 | .821 | .0033 | 1.000 | 55.0 s |
| 60 s | n-gram logistic | .00235 | .3372 | .2511 | .744 | .0052 | 1.000 | 53.5 s |
| 300 s | rate/error heuristic | .00855 | .2339 | .2453 | .880 | .0233 | 1.000 | 175.0 s |
| 300 s | individual logistic | .00855 | .6400 | .3208 | .659 | .0120 | .875 | 258.0 s |
| 300 s | behavioral logistic | .00855 | .6385 | .3977 | .739 | .0097 | 1.000 | 169.0 s |
| 300 s | gradient boosted | .00855 | **.8539** | .5341 | .771 | .0058 | 1.000 | 139.5 s |
| 300 s | n-gram logistic | .00855 | .8126 | .3958 | .722 | .0095 | 1.000 | 124.5 s |

The 60-second gradient-boosted AP campaign-bootstrap 95% interval is approximately [.362, .723]; at 300 seconds it is [.751, .915]. With only eight correlated campaigns, these are sensitivity ranges, not population-generalization guarantees.

Calibration for the 60-second tree was Brier .001617 and 10-bin ECE .001188, versus prevalence .002348. The apparently small absolute calibration errors reflect the rare target and should not substitute for reliability plots on more campaigns. The 300-second tree had Brier .002706 and ECE .001491.

### Request-count horizons

| H | Model | Prevalence | AP | Precision | Recall | FPR | Event recall | Median lead |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 20 req | gradient boosted | .000088 | .0752 | .0010 | .500 | .0434 | .625 | 14 req / 9 s |
| 100 req | gradient boosted | .000439 | .1769 | .0012 | .663 | .2407 | .750 | 96 req / 12 s |
| 1,000 req | gradient boosted | .004388 | .1367 | .0562 | .569 | .0421 | 1.000 | 994.5 req / 15 s |
| 1,000 req | n-gram logistic | .004388 | .1004 | .0368 | .824 | .0949 | .875 | 997 req / 15 s |

The discrepancy is substantive: thousands of scanner requests can occur in seconds. A “1,000-request warning” was only about 15 seconds in median wall-clock time. Validation thresholds for 20/100-request targets transferred especially poorly; the tree’s 100-request FPR was .241, while logistic models were near .50. Request count is therefore not a stable operational horizon across rates/campaigns.

## Sequential and prefix evidence

At 60 seconds:

| Prefix | Behavioral logistic AP | Gradient-boosted AP | N-gram AP |
|---:|---:|---:|---:|
| 5 | .1653 | .4116 | .2622 |
| 20 | .1872 | .4721 | .3372 |
| 100 | .2008 | .4643 | .3978 |

The individual-request logistic AP remains .1786 because it uses only the latest request. The n-gram trend (.262 → .398) shows incremental sequence information, but aggregate trees remain stronger and cheaper. A neural model would add optimization and calibration risk without enough independent sequences/events. Do not implement one unless a new corpus provides at least dozens of independent attack campaigns per held-out application/tool family.

## Compute and latency

Mean per-snapshot inference on this laptop was roughly 0.2–1.4 μs for logistic models and 1.5–18.8 μs for the tree depending on horizon/data size. Fold training ranged from sub-second to several seconds; n-gram folds were about 1.3 s on time horizons and 8–10 s on request horizons. These measurements exclude HTTP parsing, network, serialization, and controller overhead and are microbenchmark-scale, but they decisively show that classical prediction is not the hardware bottleneck.

## Interpretation limits

1. The model forecasts the transition from already-visible scanning/reconnaissance to the scripted `webshell` phase. It does not show prediction from ordinary browsing before malicious behavior begins.
2. “Webshell phase” is an independently supplied phase timestamp, but not an independently instrumented exploit success.
3. Four campaigns contain roughly 400k directory-scan requests and the others roughly 4.5k. Aggregate features can encode the generator despite identifier removal.
4. Every AIT campaign eventually attacks, so there is no wholly benign held-out campaign and legitimate automated behavior is underrepresented.
5. Eight testbeds do not equal eight independent adversaries. Campaign-level splitting prevents prefix leakage, not shared-script leakage.

## Gates

- **Gate 2 — CONDITIONAL.** There is clear predictive signal beyond simple baselines for 60/300-second proxies, but it begins during overt recon and has not been validated against independently instrumented exploitation.
- **Gate 3 — FAIL.** The current evidence cannot rule out shared tool/rate/application artifacts. Held-out testbeds are necessary but insufficient when generated by the same attack process. Request-horizon transfer failures reinforce this concern.

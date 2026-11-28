# Dataset suitability report

## Decision

No inspected public dataset is sufficient by itself for a defensible, general claim about future web exploitation. AIT-LDS V2.1 is the only inspected source that supports the precise chronological proxy experiment across multiple campaigns, but its eight campaigns share synthetic infrastructure and attack automation, and its `webshell` phase is an exploit-attempt proxy rather than proof of success. WebSpotter is suitable for current-request detection, CAM-LDS for attack-step observability, and the real web-server logs for realism checks; none closes the outcome/generalization gap.

## Prediction target and evidence rules

The feasibility target is:

> Given completed requests observed through time *t*, estimate the probability that the first exploit attempt occurs in `(t, t + H]` (or within the next *K* requests).

The local AIT experiment treats AIT-ADS `webshell` phase start as the first-exploit-attempt proxy. It does **not** call this successful exploitation. Features may use responses only after those prior requests completed. Raw IP, user-agent values, absolute time, campaign ID, raw paths, and obvious tool strings are excluded from the main feature set. Because the extracted Apache logs do not provide a trustworthy authenticated identity, the experiment uses application/campaign risk snapshots rather than pretending that an IP is a person or session.

All AIT events are fully observed, so pre-event snapshots outside the horizon are negatives rather than right-censored observations. This does not solve the broader session-censoring problem: the inspected public data cannot reconstruct reliable user sessions, and future work must retain session endings as censored rather than labeling them benign.

## Comparative evidence

| Dataset | Actual inspected evidence | Chronology / fields | Ground truth and campaigns | Suitability / risks |
|---|---|---|---|---|
| [AIT-LDS V2.1](https://doi.org/10.5281/zenodo.19483937), v2.1, 2026-04-09, CC BY-NC-SA 4.0 | Remote central directories for all eight no-PCAP ZIPs; selected Apache access and line-label files from all eight; Russell-Mitchell attacker `traffic.json`. Record totals 137.09 GB compressed; no-PCAP ZIPs are about 0.52–1.30 GB compressed. The smallest expands to about 6.9 GiB. | Apache time, method, URI, status, size, referer, UA. No reliable session identifier. Attacker trace has packet chronology and HTTP details: 650,398 JSONL rows, 25,325 HTTP-layer packets and 7,850 request-method/URI rows. | Eight named synthetic enterprise testbeds. AIT-ADS phase labels separate scans, `dirb`, `wpscan`, `webshell`, later cracking/reverse shell, but phase start is not independent proof an exploit succeeded. Shared automation/tooling makes the campaigns correlated. | **Best available proxy**, but licenses are non-commercial/share-alike, no wholly benign campaign is present, app-level identity is ambiguous, tool/rate leakage is severe, and eight correlated events cannot establish real-world generalization.
| [AIT Alert Data Set](https://doi.org/10.5281/zenodo.8263181), v1, 2023-08-18, CC BY 4.0 | Metadata and manifest; MD5-verified 3,703-byte `labels.csv`; Russell-Mitchell AMiner (4,056 rows, 3.41 MB) and Wazuh (41,488 rows, 45.28 MB) JSON selected from the 96.20 MB ZIP. | Alert timestamps and detector output can align with AIT phases. It is detector-derived rather than raw user-session HTTP. | 79 labeled phase intervals across the same eight scenarios (header plus 79 rows). | Useful for auxiliary detector comparison and timing, not independent exploit outcome or extra campaign diversity. Alert leakage must be controlled.
| [CAM-LDS](https://doi.org/10.5281/zenodo.18861762), 2026-03-04, CC BY 4.0 | Complete record metadata and remote manifests for scenarios 1 and 7; scenario 1 selected Apache, attackmate, and Suricata event files. Record: 36 files, 7.41 GB. Scenario 1 archive: 165.9 MiB compressed / 963.4 MiB expanded. | Scenario 1 Apache has 24,860 requests but spans only about 06:26:07–06:29:12. Attackmate has 32 ordered attack steps; Suricata adds host/network evidence. | Paper/record describes 7 scenarios, 34 simulations, 243 steps, 81 ATT&CK techniques, 18 sources. The observed scenario is scripted and the idle synthetic network lacks normal human web activity. | Good for attack-step reconstruction and outcome instrumentation patterns. Poor forecasting corpus: too little benign activity, few independent scenarios, and direct attack manifestations dominate.
| [WebSpotter v1.0](https://doi.org/10.5281/zenodo.16978408), 2025-08-28, MIT | Entire 44.33 MB remote ZIP manifest and selected released JSONL: CSIC, CVE, FPAD, FPAD-OOD, PKDD, loader, README, license. 54 members / 128.8 MiB expanded. | Records contain method, URL, body, label and sometimes attack spans. **No timestamp or session field.** Counts: CSIC 25,701 train + 8,576 test; CVE 42,449 + 9,248; FPAD 37,779 + 16,197; FPAD-OOD 21,180 test; PKDD 40,092 + 10,024. | Per-request labels/localizations, no independently ordered future event. | Appropriate for detecting/localizing the current request and possibly pretraining content encoders. It cannot directly test the proposed forecast or lead time. Treating file order as chronology would fabricate evidence.
| CSIC 2010 | Inspected through the WebSpotter-normalized release and source literature. | Method/URL/body and label; no reliable timestamp/session chronology in the inspected release. | Generated normal and anomalous requests, not independently verified outcome sequences. | Current-request anomaly baseline only. Cookie/IP shortcuts and synthetic generation are leakage risks.
| Web Server Log Dataset, [Zenodo 20001206](https://zenodo.org/records/20001206), 2026-05-03, MIT | Metadata, full 2.14 MB Organization-X ZIP manifest, YAML labeling rules, current and prior Apache logs. Org-X archive expands to 6.76 MB; Org-Y archive is 390.77 MB compressed. Two inspected Org-X files contain 3,872 and 17,757 lines and legitimate uptime-monitoring/browser traffic. | Standard Apache chronology, method, URL, status, bytes, referer, UA. Public addresses are anonymized; no stable authenticated identity was found. | Org-X YAML labels are explicitly produced by log2timeline plus case-insensitive string-pattern matching (e.g. `POST` + `python`, `etc/passwd`, SQL tokens). The record says Org-X has attempts but no privilege escalation; Org-Y has a successful privilege escalation but no clear prior reconnaissance. | Adds real operational background, but labels are pattern-derived, not independent outcomes. Org-X lacks success; Org-Y’s success reportedly lacks observable precursor. Useful negative/realism source subject to license/privacy review, not a sufficient forecast benchmark.
| Biblio-US17 | Source literature/metadata only; not downloaded in the time box. Roughly 47 million real HTTP requests over six months. | Chronological web traffic exists. | Labels derive from sanitization/IDS processes rather than verified exploit outcomes. | Potential benign/realistic traffic source. Size, privacy, label reliability, and outcome gap make it secondary.
| DARPA Transparent Computing | Metadata/literature only; not downloaded. Public provenance traces and red-team annotations, very large. | Strong host chronology; HTTP is not the primary representation. | Multi-stage red-team events with annotations. | Could validate outcome causality at host level but requires large storage and complex provenance reconstruction; not a two-day or laptop-first HTTP benchmark.

## AIT chronological reconstruction

The parser sorted Apache records by timestamp and retained all requests strictly before each campaign’s AIT-ADS `webshell` start.

| Campaign | Apache requests | First-exploit proxy (UTC) | Requests from recon start to proxy |
|---|---:|---|---:|
| fox | 422,890 | 2022-01-18 12:38:00 | 410,906 |
| harrison | 440,227 | 2022-02-08 07:55:59 | 415,876 |
| russellmitchell | 11,130 | 2022-01-24 03:58:19 | 7,663 |
| santos | 15,700 | 2022-01-17 11:22:58 | 7,762 |
| shaw | 15,555 | 2022-01-29 14:39:40 | 5,216 |
| wardbeck | 41,894 | 2022-01-23 12:12:17 | 5,284 |
| wheeler | 440,766 | 2022-01-30 07:56:46 | 431,611 |
| wilson | 463,726 | 2022-02-07 11:20:27 | 428,216 |

The striking two-mode volumes are themselves a warning: fox, harrison, wheeler, and wilson contain roughly 400,000 `dirb` requests, while the smaller pattern contains roughly 4,462. A model can recognize shared automation/rate rather than a general intent-to-exploit transition. Santos had no matching extracted Apache line-label rows even though phase timing exists; this is retained as an annotation inconsistency rather than silently repaired.

## Leakage, privacy, and license findings

- Archive/file order is never treated as event order; parsed timestamps define order.
- AIT raw identities, UAs, campaign names, absolute timestamps, raw URLs and obvious scanner tokens are excluded from the main baselines. Aggregate rates, status histories and coarse structural tokens can still encode the shared script.
- Prefixes are split by campaign before training, but that is weaker than independent-adversary splitting because the campaigns share generation machinery.
- WebSpotter’s supplied train/test files are not evidence for temporal generalization.
- Real operational logs may contain personal or security-sensitive data even when addresses are anonymized. Keep raw files Git-excluded; publish only aggregate derived evidence after license/privacy review.
- AIT-LDS V2.1’s CC BY-NC-SA terms differ from the permissive WebSpotter artifact. Any redistributed derivative must be checked against share-alike and attribution requirements.

## Data gate

**Gate 1 — CONDITIONAL.** Chronological HTTP and phase annotations exist for a useful proxy experiment, but independently verified exploit outcomes and independent real campaigns do not exist in sufficient quantity. The minimum repair is controlled, outcome-instrumented local generation across multiple applications and independently randomized attack/benign operators, followed by a real-background robustness test.

# PROTO-SURE feasibility report

**Assessment date:** 28 November 2026 (experiments run 27 November)

**Recommendation:** **CONDITIONAL GO**

**Scope:** preliminary feasibility only; no proposed budget controller or risk validator was implemented.

## Decision

The original MARISSA pipeline is practical on the available CPU laptops for captures of 100–1,000 packets. Eight baseline matrix runs completed without timeout; the largest used 561.1 MiB peak RSS and about 101 s. Known DNS and Modbus/TCP invariants can independently test inferred structures. However, the repository does not document capture provenance or a dataset-specific license, and the supplied 100/500/1,000 captures are not controlled prefixes. The project is viable only after those two validity problems are resolved.

Primary sources are the [EuroS&P paper record](https://doi.org/10.1109/EuroSP68448.2026.00084) and [MARISSA repository](https://github.com/reverseame/MARISSA). Published claims were not treated as locally reproduced results.

## Evidence boundary

- **Locally reproduced:** source installation, original default pipeline on DNS and Modbus captures, sample-size matrix, repeated DNS run, resource usage, capture overlap, and limited fixed-header validation.
- **Independently established locally:** DNS header facts and Modbus/TCP MBAP/function-code constraints parsed directly from the captures with Scapy.
- **Not established:** full-paper accuracy/speed claims, comparison to the paper's other tools, whole-message field ground truth, dataset provenance, or the proposed novel methods.

## Artifacts and execution environment

MARISSA was cloned at commit `adcd5bc3b94b6aff817da9dc613caa3a62a147d6` (GPL-3.0 repository license). Tests ran in the fresh Linux Python 3.11.18 environment documented in [`linux-pip-freeze.txt`](../environment/linux-pip-freeze.txt). Relevant versions include MAFFT 7.526, ssdeep 3.4 with libfuzzy/ssdeep 2.14.1, py-tlsh 4.7.2, Scapy 2.6.0, pandas 2.2.3, NumPy 1.26.4, SciPy 1.13.1, and scikit-learn 1.5.2.

Two reproducibility problems were corrected without changing MARISSA source:

- `ssdeep==3.4` omitted a build dependency on `six` and needed the locally built libfuzzy headers/library.
- unconstrained modern Click 8.5.1 was incompatible with Typer 0.9.4; installing the exact versions from the repository's Poetry lock (`click==8.1.7` and associated pins) restored the CLI.

`pip check` reports no broken requirements. The source also declares `-l` for two CLI options, an ambiguity that should be fixed upstream before extending the interface.

## Baseline configuration

Every matrix run used the repository's original CLI with:

```text
marissa --input <capture> --output <directory> --remove-headers \
  --distance-algorithm ssdeep --cluster-algorithm optics \
  --align-algorithm mafft
```

OpenMP/BLAS threads were capped at four, the external timeout was 300 s, and stdout, stderr, metadata, inferred CSV/PCAP files, exact command, and resource measurements were retained per run.

## Sample-size and resource results

| Protocol | Packets | Status | Wall time | Peak RSS | Final clusters | Tool-reported core runtime |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| DNS | 100 | success | 12.04 s | 242.7 MiB | 10 | 7.25 s |
| DNS | 500 | success | 51.87 s | 458.0 MiB | 11 | 46.37 s |
| DNS | 1,000 | success | 100.94 s | 561.1 MiB | 14 | 92.94 s |
| Modbus/TCP | 100 | success | 6.49 s | 234.2 MiB | 2 | 3.47 s |
| Modbus/TCP | 500 | success | 19.28 s | 248.1 MiB | 7 | 15.50 s |
| Modbus/TCP | 1,000 | success | 38.43 s | 260.0 MiB | 4 | 34.38 s |

All six primary runs succeeded and none approached the timeout or an 8 GB RAM limit. DNS memory increased materially with sample size; Modbus memory was nearly flat. Cluster count was not monotonic for Modbus, showing that “more observations” does not simply refine a fixed partition.

Three clean DNS-100 repetitions took 11.26–12.04 s (mean 11.74 s, sample standard deviation 0.42 s), each producing 10 clusters. A later isolated CPU probe took 14.55 s, peaked at 242.7 MiB, consumed 5.94 observed CPU-seconds (40.8% of one core averaged over total wall time), and briefly sampled 296.9% during parallel stages. The initial matrix was recorded before the monitor's cumulative CPU accounting fix; its runtime/RSS are valid, but its average CPU fields are unavailable and the DNS-1000 sampled CPU spike is invalid. This limitation is explicit rather than back-filled.

Structured results are in [`summary.csv`](../results/proto-sure/summary.csv); the corrected CPU sample is in [`cpu_probe_dns_100/`](../results/proto-sure/cpu_probe_dns_100/).

## Capture composition and overlap

The repository contains 27 PCAPs: nine protocols at nominal sizes 100, 500, and 1,000. All selected DNS and Modbus application messages were unique within each capture.

The 100- and 500-packet files are **not sequence prefixes** of the 1,000-packet files. Their unique-message overlap was:

| Protocol | 100 contained in 500 | 100 contained in 1,000 | 500 contained in 1,000 |
| --- | ---: | ---: | ---: |
| DNS | 42% | 100% | 100% |
| Modbus/TCP | 50% | 100% | 100% |

Thus the 100 and 500 samples differ in both size and composition. The observed cluster changes cannot be causally attributed to sample count. A valid final study must derive stratified/nested subsets from a common capture and repeat multiple seeds/subsamples.

Hashes and full overlap measurements are in [`capture_structure_analysis_v2.json`](../results/proto-sure/capture_structure_analysis_v2.json).

## Independent structural ground truth

The validator did not use MARISSA's inferred fields to define truth.

**DNS.** All 1,600 inspected DNS messages had at least the standard 12-byte header and `QDCOUNT=1`. Query/response counts were 48/52, 250/250, and 482/518 for the three sizes. Fixed two-byte header field boundaries were taken as bytes 2, 4, 6, 8, 10, and 12.

**Modbus/TCP.** All 1,600 messages had a parsable seven-byte MBAP header plus function code, protocol identifier zero, and a length field consistent with the captured application payload. Function codes were independently enumerated; codes 3 and 4 dominated, with rare additional values.

Within only these known fixed-header regions, every MARISSA cluster recovered every true boundary (recall 1.0), but it placed a boundary after every byte. Precision was therefore 0.50 for DNS (F1 0.667) and 0.625 for Modbus (F1 0.769). This is evidence of measurable over-segmentation in the narrow evaluated region, not a whole-message accuracy score. Variable DNS names, alignment gaps, and inferred variable fields require a richer labelled schema before publication.

## Measurable inference error under limited diversity

The feasibility test establishes that errors are measurable, but not yet that low sample size alone causes them:

- fixed-header over-segmentation persisted at 100, 500, and 1,000 packets;
- DNS cluster count increased from 10 to 11 to 14;
- Modbus cluster count changed from 2 to 7 to 4;
- 100-vs-500 capture overlap was only 42–50%, confounding size and traffic diversity.

The final design should independently vary observation count, message-type coverage, and capture source. At minimum use nested stratified subsets, several random repetitions, held-out messages, and a protocol-aware field annotation. Suitable metrics are boundary precision/recall/F1, cluster ARI/NMI against message types, schema violation rate, held-out parse success, runtime, and abstention coverage.

## Observable constraints for security validation

The following constraints can be checked from network observations without firmware/binary access:

- DNS fixed-header length; flag bit ranges and reserved bits; count/section consistency; query/response transaction matching; encoded-name and RDATA bounds.
- Modbus/TCP protocol identifier equals zero; MBAP length equals remaining bytes; valid unit identifier; request/response function-code consistency; exception-code form; per-function length/value constraints.
- Cross-protocol generic constraints: minimum/maximum field length, constant-field stability, inferred length/checksum relations, message-type-specific mandatory fields, and temporal request/response pairing.

These should be used as an independent validator with explicit **valid / invalid / abstain** output. They should not be marketed as vulnerability detection unless an experiment links violations to controlled malformed or risky messages.

## Dataset and licensing risk

The repository root is GPL-3.0 and the PCAPs are publicly downloadable with the code. No dataset README, capture-generation procedure, source URL, consent statement, or dataset-specific license was found. A software license in the repository does not by itself prove the provenance or redistribution rights of captured traffic.

Before a final project, obtain written clarification from the authors or replace the research dataset with reproducibly generated controlled captures. Store only public or locally generated traffic, strip identifiers, document commands/topology/tool versions, and publish hashes and per-capture protocol/message-type distributions.

## Two independently measurable contributions

The proposal supports the required 4+3 split if the two contributions have separate hypotheses and metrics.

**Group of four — validation-utility-aware budgeted inference.** Allocate observation and compute budgets across message types/clusters using inexpensive features. Independently evaluate field-boundary/cluster quality and held-out parse success per packet, second, and MiB against original MARISSA, uniform sampling, and random sampling.

**Group of three — risk-constrained structural validation.** Build protocol-independent constraints plus two documented protocol profiles and an abstaining risk score. Independently evaluate constraint precision/recall, false-alarm rate, malformed-message detection, coverage, and validation overhead against labelled valid and synthetically malformed controlled messages.

Integration is one versioned inferred-schema format consumed by the validator. The inference contribution remains testable with a fixed validator, and the validator remains testable on hand-authored/canonical schemas.

## Remaining risks and mandatory gates

| Risk | Severity | Required mitigation |
| --- | --- | --- |
| PCAP provenance/license unclear | Critical | author clarification or replace with controlled captures |
| Existing samples confound count and diversity | High | nested stratified subsampling with repeated trials |
| Limited fixed-header “ground truth” | High | annotate full fields for at least two protocols and publish rules |
| Novelty versus recent protocol-inference work unresolved | High | focused systematic comparison before implementation |
| Classical pipeline may not satisfy an “AI” requirement | Medium | justify unsupervised decision component; do not add gratuitous deep learning |
| CLI/dependency drift | Medium | keep lock-derived pins and environment manifest |
| Encrypted, fragmented, or reassembled traffic | Medium | exclude explicitly or add controlled preprocessing tests |

## Final recommendation

**CONDITIONAL GO.** Local compute feasibility is strong, and two independently measurable contributions are possible. Convert to **NO-GO** if dataset rights/provenance cannot be resolved or if a full-field ground truth cannot be produced for at least two representative protocols during the first week. Do not claim that sample size causes inference error until a controlled nested-sample experiment is run.

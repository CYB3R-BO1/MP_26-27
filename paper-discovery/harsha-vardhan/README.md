# Harsha Vardhan — NDSS 2026 paper discovery

> **Status:** Individual paper-discovery submission. These are two candidate references, not a finalized project proposal or team assignment.

## Submitted papers

1. **[WebSpotter: Achieving Interpretable DL-based Web Attack Detection through Malicious Payload Localization](01-webspotter.md)** — NDSS 2026. First preference. Deep-learning interpretability for web attack payload localization and WAF rule generation. Public code and datasets are documented in the paper/artifact.
2. **[ProtocolGuard: Detecting Protocol Non-compliance Bugs via LLM-guided Static Analysis and Dynamic Verification](02-protocolguard.md)** — NDSS 2026. Second preference. LLM-guided static analysis and fuzzing-based verification of network protocol implementation bugs. Public repository and Zenodo artifact are available; local reproduction has not been attempted.

## Why these two

- Both address meaningful cybersecurity problems using AI techniques.
- They are distinct from the previous FedShield-CTI direction: neither is federated intrusion detection, continual learning or conventional graph-based traffic IDS.
- WebSpotter has a comparatively reproducible artifact and a manageable extension around localization confidence and WAF false-positive validation.
- ProtocolGuard has explicit author-acknowledged limitations around program slicing, assertion generation and fuzzing, but has higher setup and schedule risk.
- The two papers offer complementary domains: web application defense and network protocol implementation security.

## Provisional comparison

| Paper | Preference | Feasibility by 2026-12-31 | Main risk | Provisional rubric |
| --- | --- | --- | --- | ---: |
| WebSpotter | First | Conditional / relatively strong | Need benign traffic, license review and novelty validation | 42/45 |
| ProtocolGuard | Second | Conditional / higher effort | Complex LLVM/SVF/AFLNet + LLM setup; overlap with stated future work | 40/45 |

Scores are individual provisional discussion scores using the shared nine-criterion rubric. They are not a team ranking.

## Important research discipline

- Reported paper results are author-reported; neither paper has been reproduced by this submission.
- Candidate gaps are hypotheses, not established novelty.
- WebSpotter already evaluates OOD and poisoning; proposed work must extend those evaluations.
- ProtocolGuard's authors already suggest runtime execution context and protocol-aware mutation; simply implementing these suggestions is not automatically novel.
- Check code/data licenses, reproduce a baseline and conduct a 2024–2026 related-work search before fixing a proposal.

## Next actions

- [ ] Read both papers in full and verify all dataset/table details.
- [ ] Check licenses and current dependency compatibility.
- [ ] Reproduce WebSpotter's FPAD baseline.
- [ ] Build a minimal ProtocolGuard workflow for one supported C-based protocol implementation.
- [ ] Search related work for each proposed extension.
- [ ] Revise feasibility scores based on actual setup results.
- [ ] Submit findings for the seven-member review of all 14 candidate papers.

Template followed: [paper-discovery/TEMPLATE.md](../TEMPLATE.md).

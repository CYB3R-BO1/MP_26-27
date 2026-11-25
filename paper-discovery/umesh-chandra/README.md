# Umesh Chandra — Paper discovery (ACM CCS 2026)

**Status:** Two candidate references submitted for group review. This is not a final major-project selection.

## Submitted papers

1. **[MirrorGuard](01-mirrorguard.md)** — first preference. AI-agent/GUI security; reasoning correction against unsafe computer-use actions.
2. **[PBFuzz](02-pbfuzz.md)** — second preference. Agentic software vulnerability discovery; semantic constraint reasoning and PoV generation.

## Why these two

Both differ from federated intrusion detection, continual learning and conventional graph-based NIDS. They apply AI to concrete security problems, expose measurable outcomes and have public research artifacts.

- **MirrorGuard:** Candidate extension is adaptive visual-injection evaluation plus independent action-policy verification. Main feasibility issue: full fine-tuning is reported on four NVIDIA H200 GPUs; a smaller frozen-model/verifier prototype is more realistic.
- **PBFuzz:** Candidate extension is cost-aware hybrid search plus independent PoV validation. Main constraints are Linux/toolchain/API setup and the current repository's PolyForm Noncommercial license.

## Provisional scores

| Criterion | MirrorGuard | PBFuzz |
| --- | ---: | ---: |
| Research quality/relevance | 4 | 5 |
| Feasibility | 3 | 3 |
| Novelty potential | 4 | 4 |
| Different from previous IDS | 5 | 5 |
| Meaningful AI for cybersecurity | 5 | 5 |
| Modernity | 5 | 5 |
| Public resources | 4 | 4 |
| Measurable improvement | 5 | 5 |
| Two complementary contributions | 4 | 5 |
| **Total / 45** | **39** | **41** |

Scores are provisional, not a decision. Critical feasibility blockers and novelty overlap must be reviewed separately.

## Verification notes

- Neither implementation has been independently reproduced.
- MirrorGuard's repository declares MIT; benchmark and model terms still need checking.
- PBFuzz's current repository declares PolyForm Noncommercial 1.0.0. Confirm permitted use with the supervisor; do not redistribute without complying.
- PBFuzz's preprint is dated December 2025; its Zenodo artifact record says accepted to CCS 2026 on 5 June 2026.
- Verify final proceedings/DOI metadata for both papers before the final report.
- Proposed extensions are hypotheses, not established novelty. Review close 2024–2026 work first.

## Potential 4+3 contributions

- **Four-member group:** MirrorGuard extension — adaptive visual-injection evaluation and action-level security verification.
- **Three-member group:** PBFuzz extension — hybrid fuzzing efficiency and independent PoV validation.

These are possible work packages only. The overall project problem and team allocation remain unselected until all seven members' fourteen papers are compared.

Template: [paper-discovery/TEMPLATE.md](../TEMPLATE.md).

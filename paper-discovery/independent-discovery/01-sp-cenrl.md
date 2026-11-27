# CenRL: A Framework for Performing Intelligent Censorship Measurements

> **Status:** Candidate reference — independent discovery review, 27 November 2026. No final project choice implied. Source metadata and abstract/previous discovery evidence are distinguished from proposed hypotheses. Full-text table/figure checks, licenses, reproduction and novelty review are incomplete unless explicitly noted.

## 1. Paper identification

| Field | Value |
| --- | --- |
| Submitted by | Independent discovery (AI-assisted; not attributed to a teammate) |
| Preference | First |
| Assigned source/category | 1 — IEEE S&P |
| Authors | Hieu Le, Armin Huremagic, Kevin Wang, Roya Ensafi, Ram Sundara Raman |
| Conference/journal | IEEE S&P 2026 |
| Publication/acceptance date | May 2026; publisher and conference program |
| Primary paper / DOI | https://ieeexplore.ieee.org/abstract/document/11573591 |
| Source code URL + license | https://levanhieu.com/publication/cenrl_sp_2026/ (author project; artifact https://secartifacts.github.io/sp2026/results; exact code license and execution not checked) |
| Dataset/benchmark URL + license | Historical measurement traces / controlled local network; exact original download, license and sizes not verified |
| Cybersecurity problem/domain | Internet censorship measurement and network availability |
| AI techniques | Multi-armed bandits |

## 2. Problem and motivation

**Exact cybersecurity problem:** Select informative measurements when blocking changes and probe resources are scarce.

**Why it matters:** Static schedules spend scarce probes on uninformative targets and can miss changes in network reachability.

**Prior research limitation:** Publisher abstract motivates efficient active measurements and dynamic blocking; detailed section references pending.

## 3. Methodology

- **Core technical idea:** Learn a probe-selection policy from observed measurement rewards.
- **Input data:** Candidate destinations, probe observations and budget
- **Output:** Budgeted measurement decisions and evidence of reachability change
- **Main components / model / verification:** Bandit agent, observation/reward loop, active measurement backend
- **What AI contributes (and why):** Learning allocates measurement effort instead of applying a fixed schedule.
- **Architecture:** our conceptual schematic (not the authors' original figure):

```text
Candidate probes -> bandit policy -> measurement -> reward -> policy update
```

## 4. Experimental evidence

| Item | Detail and source location |
| --- | --- |
| Datasets and size | Historical censorship measurements; exact splits not verified |
| Baseline systems | Static / existing measurement scheduling approaches; exact configurations pending |
| Evaluation metrics | Blocked-site discovery, measurement count, time to identify change |
| Exact numerical results | Prior discovery reported up to 7x faster change discovery and 75% blocked sites with fewer than half the measurements; exact denominator, comparator and figure not rechecked; treat as provisional. |
| Hardware/compute | Lightweight bandits plausible on CPU; original measurement infrastructure not verified. |
| Known threats to validity | Geographic and temporal sampling bias; ground truth; ethical limitations of real probes. |
| Reproduction status | Not attempted by our team |

Author-reported or previously surfaced numbers are not independent measurements. Statistical significance, table-level comparators and reproducibility are not established by this discovery review. Do not use provisional numerical claims in the final report until verified against the primary paper.

## 5. Candidate research gaps

| Gap | Evidence (section/page) | Author-acknowledged or our inference? | Possible overlap in 2024–2026 work |
| --- | --- | --- | --- |
| Changing reward distributions | test controlled changes in reachability; publisher abstract motivates dynamic settings; proposed extension, overlap with nonstationary bandits unchecked. | Our inference / proposed question | Not systematically checked; see related-work targets below. |
| Budget fairness across destinations | evaluate coverage versus prioritization; inferred; overlap with constrained bandits unchecked. | Our inference / proposed question | Not systematically checked; see related-work targets below. |
| Transfer to unseen network conditions | controlled holdout; inferred; related measurement literature unchecked. | Our inference / proposed question | Not systematically checked; see related-work targets below. |

A perceived gap is **not established novelty** until independently checked.

## 6. Potential methodological improvements

- **Hypothesis A:** Context-aware budget allocation under changing local network conditions.
- **Hypothesis B (alternative or complementary):** Calibrate uncertainty and reserve an exploration budget.
- **Expected security/efficiency benefit:** Faster discovery at fixed measurement cost without sacrificing coverage.
- **Experiment and ablation plan:** Local emulated network or legally usable historical data; compare random, round-robin, standard bandit and proposed policy at fixed budgets; ablate context and exploration; report variance.
- **Risk of failure or overlap:** May be incremental; original method may already cover change adaptation.

Do not finalize a project architecture at discovery stage.

## 7. Implementation feasibility by 2026-12-31

| Requirement | Assessment |
| --- | --- |
| Public code verified and actually tested? | https://levanhieu.com/publication/cenrl_sp_2026/ (author project; artifact https://secartifacts.github.io/sp2026/results; exact code license and execution not checked); not executed. |
| Datasets available and legally usable? | Historical measurement traces / controlled local network; exact original download, license and sizes not verified; confirm terms before use. |
| Models/inference APIs available? | Multi-armed bandits; no paid APIs allowed; local feasibility not demonstrated. |
| Hardware, API cost, and development effort | Lightweight bandits plausible on CPU; original measurement infrastructure not verified. |
| Realistic five-week minimum implementation | CPU simulation on one trace or controlled network; no real-world probing outside authorization. |
| Features deliberately excluded | Global measurement infrastructure and live censorship probing. |
| Top blockers | Original dataset/license, baseline settings, related-work novelty. |
| Verdict | Conditional |

## 8. Two-group potential (7 members)

- **Group A (4 members) — possible independently measurable contribution:** Probe-selection algorithm and controlled evaluation
- **Group B (3 members) — distinct but complementary contribution:** Uncertainty/budget controller and held-out change experiments
- **How the contributions integrate:** Shared observation interface and fixed probe budget
- **How each group demonstrates a result separately:** A reports discovery versus budget; B reports coverage and adaptation delay

Provisional only; no team assignment is implied.

## 9. Consistent selection rubric (1–5 each)

Provisional discovery assessments, not rankings or experimental measurements. Reassess after full text and feasibility checks.

| Criterion | Score / 5 | Evidence |
| --- | --- | --- |
| Research quality and relevance | 5 | IEEE S&P 2026; Internet censorship measurement and network availability |
| Implementation feasibility | 4 | CPU simulation on one trace or controlled network; no real-world probing outside authorization. Blockers: Original dataset/license, baseline settings, related-work novelty. |
| Novelty potential | 3 | May be incremental; original method may already cover change adaptation. |
| Different from previous federated/continual/graph IDS | 5 | Problem: Select informative measurements when blocking changes and probe resources are scarce. |
| Meaningful AI for cybersecurity | 4 | Learning allocates measurement effort instead of applying a fixed schedule. |
| Technically justified modernity | 4 | Multi-armed bandits |
| Public resources/reproducibility | 3 | https://levanhieu.com/publication/cenrl_sp_2026/ (author project; artifact https://secartifacts.github.io/sp2026/results; exact code license and execution not checked); Historical measurement traces / controlled local network; exact original download, license and sizes not verified |
| Measurable improvement | 5 | Blocked-site discovery, measurement count, time to identify change |
| Two complementary contributions | 4 | Probe-selection algorithm and controlled evaluation / Uncertainty/budget controller and held-out change experiments |
| **Total** | **37/45** | Critical blockers outweigh totals. |

## 10. Final assessment

- **Strongest three reasons to shortlist:** Verified venue; lightweight learning; measurable network outcomes.
- **Three weaknesses or risks:** Specialized domain; data access; novelty of adaptation.
- **Unverified claims to investigate:** Original dataset/license, baseline settings, related-work novelty.; exact paper sections/tables, relevant licenses, compute and full related work.
- **Recommendation:** Conditional — discovery candidate only; no shortlisting decision.
- **One-sentence argument versus competing papers:** Less IDS-like than 5GShield; less API-dependent than Incalmo.

## 11. Supporting references

- Primary paper: https://ieeexplore.ieee.org/abstract/document/11573591
- Official venue/record: https://sp2026.ieee-security.org/accepted-papers.html
- Repository/benchmark: https://levanhieu.com/publication/cenrl_sp_2026/ (author project; artifact https://secartifacts.github.io/sp2026/results; exact code license and execution not checked); Historical measurement traces / controlled local network; exact original download, license and sizes not verified
- Closest related 2024–2026 work: Nonstationary and constrained bandits for network measurement (targeted literature review pending).

## Submission checklist

- [x] Bibliographic details verified from primary publication (venue/publisher or accepted listing; see specific caveats)
- [x] Author claims separated from personal hypotheses
- [ ] Actual figures/tables used for quantitative results
- [ ] Code, datasets, licenses and compute availability checked
- [ ] Research gap supported by evidence and related-work review
- [x] December 31 feasibility assessed (provisional)
- [x] Two-group contributions considered
- [x] Nine rubric scores justified (provisional)


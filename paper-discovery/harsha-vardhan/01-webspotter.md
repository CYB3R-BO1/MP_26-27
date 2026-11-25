# Achieving Interpretable DL-based Web Attack Detection through Malicious Payload Localization

> **Status:** Candidate reference — first preference in this individual discovery submission. This is not a final project choice. Claims below distinguish paper-reported evidence from our hypotheses.

## 1. Paper identification

| Field | Value |
| --- | --- |
| Submitted by | Harsha Vardhan |
| Preference | First |
| Assigned source/category | NDSS 2026 |
| Authors | Peiyang Li, Fukun Mei, Ye Wang, Zhuotao Liu, Ke Xu, Chao Shen, Qian Wang, Qi Li |
| Conference/journal | Network and Distributed System Security (NDSS) Symposium 2026 |
| Publication/acceptance date | Presented at NDSS, 23–27 February 2026 |
| Primary paper / DOI | [NDSS PDF](https://www.ndss-symposium.org/wp-content/uploads/2026-s1029-paper.pdf) · [DOI: 10.14722/ndss.2026.231029](https://doi.org/10.14722/ndss.2026.231029) |
| Source code URL + license | [Sec-AI-research/WebSpotter](https://github.com/Sec-AI-research/WebSpotter) — public; license not verified |
| Dataset/benchmark URL + license | [Zenodo artifact, DOI 10.5281/zenodo.16978408](https://doi.org/10.5281/zenodo.16978408) — paper says datasets are public; individual dataset licenses not verified |
| Cybersecurity problem/domain | Interpretable deep-learning-based web attack detection and malicious HTTP payload localization |
| AI techniques | Deep-learning model attribution using gradient analysis; lightweight ML localization model using importance and textual features |

## 2. Problem and motivation

**Exact cybersecurity problem:** Deep-learning web attack detectors can classify HTTP requests but often do not identify the exact request fields or semantic units containing malicious payloads. This limits explainability and makes it harder for operators to investigate alerts and create targeted WAF rules.

**Why it matters:** HTTP attacks such as SQL injection and XSS can place malicious content in different request fields. A useful detector should help an operator understand where the suspicious content is, not only return a benign/malicious label.

**Prior research limitation:** The paper's Introduction (Sections I–II, PDF pp. 1–3) explains that common interpretability techniques overlook HTTP request structure and therefore produce feature-importance explanations that are not directly actionable at the HTTP-field level.

## 3. Methodology

- **Core technical idea:** Use the detection model's embedding-level importance, align that importance with HTTP semantic units, and train a lightweight model to localize malicious payloads.
- **Input data:** HTTP requests and predictions/embeddings from an existing web attack detection model; a small set of attack requests with payload-location labels for localization training.
- **Output:** Locations of malicious payloads within HTTP request semantic units; grouped patterns can also inform WAF rule generation.
- **Main components / model / verification:**
  1. Embedding attribution: gradient analysis with interpolation to estimate embedding importance.
  2. HTTP-structure alignment: aggregate importance from embedding dimensions to tokens and then to minimal semantic units (MSUs).
  3. Malicious payload localization: combine importance features and textual features in a lightweight localization model.
  4. WAF rule generation: group semantically similar attacks and derive common payload patterns.
- **What AI contributes (and why):** The existing DL detector provides prediction-sensitive attribution; ML learns the relationship between importance/textual features and malicious payload locations. This converts a class prediction into a structured explanation.
- **Architecture:** See Fig. 2 in the primary paper (PDF p. 3). The three main modules are embedding attribution, HTTP-structure alignment and malicious payload localization. WAF rule generation is described in Section V.

## 4. Experimental evidence

| Item | Detail and source location |
| --- | --- |
| Datasets and size | Two public datasets plus the authors' newly constructed FPAD dataset and FPAD-OOD test set. Exact sample counts should be transcribed from Section VII.A / dataset tables during the detailed review; not copied here without verification. |
| Baseline systems | Four localization baselines are compared; see Section VII and Table I / Table II. Ablations compare alternative attribution/alignment/localization variants. |
| Evaluation metrics | Precision, recall, F1-score and Jaccard index for localization; WAF attack detection rate for the rule-generation experiment; runtime for computational overhead. |
| Exact numerical results | At 1% location-labeling overhead, Table I reports WebSpotter F1 of 0.972 (CSIC), 0.986 (PKDD), 0.988 (FPAD), and 0.970 (FPAD-OOD). The paper reports at least a 22% improvement in localization accuracy against baselines in the abstract. Real-world attack evaluation reaches F1 up to 0.945 (Introduction). Generated rules improve the evaluated WAF's attack detection rate by 26% (Introduction / Section V). These are author-reported, not reproduced by our team. |
| Hardware/compute | Artifact appendix: at least 16 GB RAM; CPU execution possible; NVIDIA GPU recommended, approximately 12 GB VRAM or more. Authors used RTX 4090 24 GB. Python 3.9. |
| Known threats to validity | Results depend on the datasets, detector, location labels and tested request formats. The paper studies poisoning, but this does not establish robustness to every real-world data or deployment shift. WAF benefit is evaluated in the paper's chosen setting; broader benign-traffic operational impact needs separate measurement. |
| Reproduction status | Not attempted. Artifact is listed as Available, Functional and Reproduced by the NDSS 2026 artifact results page; our team has not independently reproduced it. |

The paper reports an F1-score of 0.970 on FPAD-OOD at 1% labeling overhead (Table I), so unseen-pattern evaluation is already part of the baseline. Any proposed work must improve on or broaden that evaluation rather than claim OOD testing as an untouched gap.

## 5. Candidate research gaps

| Gap | Evidence (section/page) | Author-acknowledged or our inference? | Possible overlap in 2024–2026 work |
| --- | --- | --- | --- |
| Operational validation of generated WAF rules against a broad benign-traffic corpus, including false-positive blocking and rule conflicts | Rule generation is described in Section V; reported WAF detection-rate improvement is 26%. The paper does not establish broad deployment safety across diverse benign traffic in the cited result. | Our inference; not presented as an explicit author-acknowledged limitation | Must compare with WAF rule learning, false-positive reduction and rule validation literature before claiming novelty. |
| Calibration of localization confidence and abstention when the model is uncertain | Localization model and evaluation are described in Sections IV and VII. A confidence-calibration/abstention study is not a principal reported contribution. | Our inference | Must survey explainable web-attack localization and selective prediction. |
| Robustness of the complete localization-to-WAF pipeline under realistic traffic drift and imperfect location labels | Section VII.D studies simulated poisoning; the paper also evaluates FPAD-OOD. More varied drift and label-noise conditions remain possible experiments. | Our inference; the paper does evaluate poisoning and OOD, so this is an extension, not an absent topic | Must compare with robust learning, noisy-label localization and WAF adaptation studies. |

A perceived gap is not established novelty until independently checked.

## 6. Potential methodological improvements

- **Hypothesis A:** Add calibrated confidence and an abstention/review path to payload localization. Low-confidence localizations should not automatically become blocking rules.
- **Hypothesis B (alternative or complementary):** Add a benign-traffic validation loop for candidate WAF rules. Measure false-positive blocking and refine or reject rules that match legitimate requests.
- **Expected security/efficiency benefit:** Reduce unsafe rule deployment and operator workload while retaining attack recall.
- **Experiment and ablation plan:** Reproduce the baseline; compare original localization with calibrated localization; evaluate candidate rules on separate benign and malicious traffic; report localization F1, attack recall, benign false-positive rate, rule precision, latency and calibration error. Perform ablations for confidence thresholding and benign validation.
- **Risk of failure or overlap:** The authors already evaluate OOD and poisoning. Confidence calibration and WAF rule validation may overlap with existing literature. A novelty search and data/license review are mandatory before fixing the proposal.

Do not finalize a project architecture at discovery stage.

## 7. Implementation feasibility by 2026-12-31

| Requirement | Assessment |
| --- | --- |
| Public code verified and actually tested? | Public repository and README verified; reproduction not attempted. |
| Datasets available and legally usable? | Paper and artifact appendix state datasets are public; exact licenses and redistribution terms not verified. |
| Models/inference APIs available? | TextCNN model and reproduction workflow are provided; no external LLM API is required for the core baseline. |
| Hardware, API cost, and development effort | 16 GB RAM minimum; CPU possible; recommended NVIDIA GPU around 12 GB VRAM. Moderate development effort if scope is limited to the supplied FPAD workflow. |
| Realistic five-week minimum implementation | Conditional yes: first reproduce FPAD/FPAD-OOD, then implement confidence reporting and benign-request rule validation. |
| Features deliberately excluded | New detector architecture, production WAF deployment, broad multi-format HTTP parser support, large-scale collection of live traffic. |
| Top blockers | Dataset licensing/terms; compatibility with current Python/PyTorch packages; obtaining representative benign traffic with defensible labels; reproducing the exact baseline. |
| Verdict | **Conditional** — strongest feasibility of the two papers, subject to successful environment setup and baseline reproduction. |

## 8. Two-group potential (7 members)

- **Group A (4 members) — possible independently measurable contribution:** Confidence-aware payload localization and calibration. Evaluate localization precision/recall/F1, calibration and abstention coverage.
- **Group B (3 members) — distinct but complementary contribution:** Benign-traffic validation and false-positive-resistant WAF rule refinement. Evaluate attack recall, benign false-positive rate and rule precision.
- **How the contributions integrate:** Group A supplies localized payloads and confidence values; Group B validates candidate rules before they are considered deployable.
- **How each group demonstrates a result separately:** Group A demonstrates improved localization reliability; Group B demonstrates safer rule generation on a held-out benign/malicious request set.

Provisional only; no team assignment is implied.

## 9. Consistent selection rubric (1–5 each)

5 = excellent; 4 = good; 3 = conditional; 2 = weak; 1 = poor.

| Criterion | Score / 5 | Evidence |
| --- | ---: | --- |
| Research quality and relevance | 5 | NDSS 2026 paper with real-world web security problem and multiple evaluations. |
| Implementation feasibility | 4 | Public code/data and detailed reproduction steps; still requires local testing and license review. |
| Novelty potential | 3 | Several plausible extensions, but related-work search is not complete and OOD/poisoning are already studied. |
| Different from previous federated/continual/graph IDS | 5 | Web request localization and WAF rules are distinct from FedShield-CTI. |
| Meaningful AI for cybersecurity | 5 | Deep-learning attribution and ML localization are central to the method. |
| Technically justified modernity | 5 | Addresses interpretable DL-based web defense and actionable WAF response. |
| Public resources/reproducibility | 5 | Public repository, Zenodo data/artifact, and reproduction instructions; artifact status reported reproduced by evaluators. |
| Measurable improvement | 5 | Localization F1/Jaccard, WAF detection rate, false-positive rate and latency are measurable. |
| Two complementary contributions | 5 | Localization reliability and downstream WAF validation form separable contributions. |
| **Total** | **42/45** | Provisional discussion score; not a team decision. |

Scores support discussion; critical feasibility blockers can outweigh a high total.

## 10. Final assessment

- **Strongest three reasons to shortlist:**
  1. Directly relevant web application security problem with interpretable outputs.
  2. Public source, datasets and detailed artifact instructions.
  3. Strong reported baseline metrics and separable localization/WAF evaluation.
- **Three weaknesses or risks:**
  1. The baseline is already strong, including FPAD-OOD performance.
  2. The proposed confidence and WAF validation extensions need a careful novelty search.
  3. Suitable benign traffic and license-compatible datasets may be difficult to assemble.
- **Unverified claims to investigate:** Dataset licenses; exact dataset sizes and collection details; current dependency compatibility; whether the generated-rule evaluation includes the benign false-positive scenarios needed for our extension.
- **Recommendation:** **Recommend** as a strong candidate, conditional on baseline reproduction and novelty review.
- **One-sentence argument versus competing papers:** WebSpotter offers the most straightforward route to a measurable, artifact-backed web-security extension with clear separation between localization quality and downstream WAF safety.

## 11. Supporting references

- Primary paper: [NDSS 2026 PDF](https://www.ndss-symposium.org/wp-content/uploads/2026-s1029-paper.pdf) · [DOI](https://doi.org/10.14722/ndss.2026.231029)
- Repository/benchmark: [WebSpotter GitHub](https://github.com/Sec-AI-research/WebSpotter) · [Zenodo artifact](https://doi.org/10.5281/zenodo.16978408) · [NDSS 2026 artifact results](https://secartifacts.github.io/ndss2026/results)
- Closest related 2024–2026 work: To be established by a dedicated related-work search before any novelty claim. The paper's own baseline and interpretability comparisons in Sections VII and Appendix F must be included in that review.

## Submission checklist

- [x] Bibliographic details verified from primary publication
- [x] Author claims separated from personal hypotheses
- [x] Actual figures/tables used for quantitative results
- [ ] Code, datasets, licenses and compute availability checked by running the artifact
- [ ] Research gap supported by evidence and related-work review
- [x] December 31 feasibility assessed provisionally
- [x] Two-group contributions considered
- [x] Nine rubric scores justified

# Bhanu Teja — paper discovery

This folder contains two candidate research papers from **IEEE Transactions on Information Forensics and Security (TIFS), 2026**. They address different cybersecurity problems: network traffic classification and insider-threat behavior analytics. These are discovery-stage reviews, not a final project selection.

## Candidate papers at a glance

| | **1. UTFormer** | **2. LLMBA** |
| --- | --- | --- |
| Full title | UTFormer: An Ultra-Lightweight Transformer for Traffic Classification | LLMBA: Efficient Behavior Analytics via Large Pretrained Models in Zero Trust Networks |
| Authors | Dong Wen, Tianyun Li, Zhuochen Fan, Qing Li, Jie Li, Fa Zhu | Senming Yan, Lei Shi, Wei Wang, Jing Ren, Ying Li, Limin Sun |
| Publication | IEEE TIFS, Vol. 21, pp. 7173–7187 (2026) | IEEE TIFS, Vol. 21, pp. 2403–2415 (2026) |
| Published | 9 July 2026 | 19 February 2026 |
| DOI | [10.1109/TIFS.2026.3711855](https://doi.org/10.1109/TIFS.2026.3711855) | [10.1109/TIFS.2026.3666459](https://doi.org/10.1109/TIFS.2026.3666459) |
| Main security task | Network traffic classification | User/entity behavior analytics for Zero Trust and insider-threat detection |
| Main AI approach | Attention-driven payload-byte selection + differentiable Transformer architecture search | Large pretrained language model + multi-level behavior encoding + self-supervised fine-tuning + knowledge distillation |
| Candidate preference | First | Second |

## 1. UTFormer — traffic classification

**Problem addressed:** Transformer-based traffic classifiers can carry redundant packet-payload features and unnecessary model architecture, increasing computational cost and model size.

**What the paper proposes:**
- Dynamic payload distillation uses attention-driven selection to identify critical payload bytes.
- The abstract reports that input features can be reduced by up to **95%**.
- Differentiable architecture search optimizes compact Transformer configurations; the abstract reports searched depth of **4 layers or fewer** and hidden dimensions of **256 or fewer**.

**Reported experimental results (as stated in the paper abstract):**
- Evaluated on **six datasets**.
- Classification accuracy: **87.79%–99.99%**.
- Computational cost reduction: **9.0×–36,398.5×** against Transformer-based baselines.
- Model-size reduction: **44.9×–5,433.9×** against Transformer-based baselines.
- Smallest reported model: **106 KB**.
- Offline throughput: **7.55 million packets per second**.
- Real-deployment throughput: **10 Gbps line rate**.

**Code link:** [UTFormer repository](https://github.com/utformer/UTFormer) (the URL was supplied in the abstract; repository contents, reproducibility and license have not yet been verified).

**Review file:** [01-utformer.md](./01-utformer.md)

## 2. LLMBA — Zero Trust behavior analytics

**Problem addressed:** Zero Trust environments need continuous analysis of user/entity behavior. Audit data can be large and context-rich, while supervised methods may depend on high-quality labels and struggle with previously unseen malicious behavior.

**What the paper proposes:**
- Uses a large language model to analyze sequences of internal-user and entity behavior.
- Introduces multi-level behavior encoding to represent contextual and temporal information from behavior records.
- Uses self-supervised fine-tuning to support detection of unknown malicious behavior.
- Applies knowledge distillation to produce a smaller student model intended to reduce computational and storage overhead.

**Reported experimental evidence (as stated in the supplied abstract):**
- Evaluated on the **CERT Insider Threat dataset**.
- The abstract claims higher detection accuracy than state-of-the-art baselines.
- It also claims that the compressed student model performs better than existing methods under comparable runtime constraints.
- The supplied abstract does **not** provide exact metric values, dataset version/split details, or hardware measurements.

**Code link:** No source-code URL was provided in the supplied abstract; availability has not been verified.

**Review file:** [02-llmba.md](./02-llmba.md)

## Why these two are being considered

The papers offer two distinct cybersecurity directions and different experimental questions:

- **UTFormer:** Can learned payload reduction and compact architecture search retain traffic-classification accuracy while improving model size and throughput?
- **LLMBA:** Can contextual/temporal behavior representations and self-supervised learning detect insider threats with limited labels, while distillation makes the model more efficient?

UTFormer has more numerical performance claims in the supplied abstract. LLMBA has a relevant Zero Trust/insider-threat application, but its abstract provides qualitative rather than numerical performance claims. This is an observation about the abstracts, not a conclusion that one paper is scientifically stronger.

## Evidence and verification status

The summaries and numerical claims above are limited to the supplied paper details/abstracts and bibliographic records. The full papers, result tables, code repositories, dataset versions and licenses, hardware configurations, and closest related 2024–2026 studies have **not yet been independently checked**. Do not treat proposed research gaps or experiments in the individual reviews as claims made by the authors; they are candidate ideas for later investigation.

For detailed methodology, evidence, feasibility assessment, candidate gaps, group-split possibilities and the provisional selection rubric, see the two review files linked above.

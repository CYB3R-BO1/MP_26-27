# Artifact manifest

## External artifacts inspected

| Artifact | Version/date/license | Remote integrity / size | Local inspection |
|---|---|---|---|
| AIT-LDS V2.1, Zenodo 19483937 | v2.1, 2026-04-09, CC BY-NC-SA 4.0 | 16 files / 137,088,718,752 bytes total. Eight no-PCAP MD5s are preserved in metadata; e.g. Russell-Mitchell 522,084,364 bytes, `abb43a46c70939ad9f98669e3510d2b7`. | Remote manifests for all eight no-PCAP ZIPs; selected Apache/labels from all campaigns and Russell-Mitchell attacker trace. Member CRCs/byte counts in extraction receipts. |
| AIT Alert, Zenodo 8263181 | v1, 2023-08-18, CC BY 4.0 | `ait_ads.zip` 96,202,946 bytes, MD5 `43db6b1f0996e0024befd617706c50e9`; `labels.csv` 3,703 bytes, MD5 verified `60ff33796c77fd2136c4d1a4bc841bd9`. | Labels plus Russell-Mitchell AMiner/Wazuh members. |
| CAM-LDS, Zenodo 18861762 | 2026-03-04, CC BY 4.0 | 36 files / 7.41 GB. Scenario-1 pwnkit/localaccount 173,975,360 bytes, MD5 `eaa091433ff9002b6b85bf2fa0080ba7`; scenario 7 160,106,901 bytes, MD5 `88122133a82079e07e7ed1b782bc203f`. | Remote manifests for scenarios 1 and 7; selected scenario-1 Apache, attackmate and Suricata members. |
| WebSpotter release, Zenodo concept 16978408 (resolved record 16978409) | v1.0, 2025-08-28, MIT | 44,332,532 bytes, MD5 `5a7a9cd660eea73469848726cebe13e3`; 54 members / 128.8 MiB expanded. | README/license/loader and all released CSIC, CVE, FPAD, FPAD-OOD, PKDD JSONL. |
| Web Server Log Dataset, Zenodo 20001206 | 2026-05-03, MIT | Org-X 2,135,289 bytes, MD5 `b4bf79effa6f3ee1b9e53f278d916620`; Org-Y 390,765,762 bytes, MD5 `b1925ff7f043c391d501cfd404e0df10`. | Full Org-X manifest; labeling YAML and two Apache logs. Org-Y not downloaded. |
| OWASP Juice Shop image | label 20.4.0-SNAPSHOT; built 2026-11-19 | digest `sha256:adaf6a6ca50f772dff7d2fe56972c659e81a61e0dbbe607c2b39fefd436e6153`; 343,560,349 bytes | Local isolated smoke test. |
| OWASP ModSecurity CRS nginx image | CRS 4.30.0; built 2026-11-27 | digest `sha256:cd1aa84167b5ba42539001c6fedf174484499ad1c37161df9eed1453e64d65e2`; 240,287,107 bytes | Local isolated smoke test; nginx 1.30.8, ModSecurity 3.0.17. |

Complete Zenodo metadata are in `results/zenodo_*_metadata.json`. AIT central-directory manifests prove inspected member names and expanded sizes without retrieving full archives. Extract receipts include member CRC32 verification. Raw/extracted data total approximately 1.351 GiB locally and are Git-excluded.

## Reproducible code artifacts

| File | Purpose |
|---|---|
| `scripts/fetch_zenodo_metadata.py` | Fetch and retain authoritative record metadata. |
| `scripts/remote_zip_manifest.py` | Parse a remote ZIP central directory with range requests. |
| `scripts/remote_zip_extract.py` | Range-extract selected members with traversal protection and CRC verification. |
| `scripts/profile_datasets.py` | Parse/profile AIT Apache/labels, CAM and WebSpotter releases. |
| `scripts/profile_jsonl_trace.py` | Streaming profile of the large AIT attacker packet JSONL. |
| `scripts/run_ait_baselines.py` | Build strict pre-event snapshots; campaign-held-out baselines, calibration, event metrics, campaign bootstrap and resource timing. |
| `scripts/test_local_defense.sh` | Isolated benign/WAF smoke test and lightweight measurements. |
| `environment/local-testbed.compose.yml` | Digest-pinned isolated Juice Shop + CRS topology. |

## Key derived results and SHA-256

| Result | SHA-256 |
|---|---|
| `results/ait_baselines_full.json` | `6c4c1e58d0ac43ac427690868d801fdc060c33ec227d710aeb65d491c4ac36b6` |
| `results/dataset_profile.json` | `12856bec020a8e366f29853127b3bae0f8c49ea51543502542acdb937449f621` |
| `results/ait_attacker_trace_profile.json` | `f0a7352aa500f9b124efef9c9ea09743738c1d908818a3bdb4438db0b746118` |
| `results/ait_prefix5_time60.json` | `1e880d0ac4a3c888e5e90f33e528a1a13846a5e69aa1f62cbc09170203ea18eb` |
| `results/ait_prefix100_time60.json` | `bcf2ac1a92a653c5f7cefd98884ac9b29d9a1184060c795948854a19c5167a6` |
| `results/defense_smoke_test.json` | `12b5cc5dd0dce5510d3d93020c179c18436223855af9e30dfd9eed6bd0bcc656` |

The JSON results are local measurements except `crossref_prerce_fuse.json`, which is publication metadata. Published claims in the literature matrix are explicitly marked and are never presented as local reproduction.

## Deliberately absent artifacts

- No final PREEMPT-WAF algorithm, trained neural model, exploit kit, live-target scan, paid API output, credential, packet capture, or production deployment.
- No raw WAF audit log because it can contain response bodies.
- No full AIT, CAM, or Org-Y download due disk/time limits.
- No changes to the earlier PROOF-BUDGET or PROTO-SURE work.
- No Git commit or push.

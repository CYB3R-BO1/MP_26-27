# External artifact manifest

Large public source checkouts, downloaded archives, local Python environments, and compiler/prover binaries are retained locally but deliberately excluded from Git. They are reproducible from the following pinned sources.

| Artifact | Source | Revision/version | Local use |
| --- | --- | --- | --- |
| TamRL | https://github.com/MatCos/TamRL | `f82e5914e23e3f1d3623d4aeaa0fb503f3ce410b` | protocol models, documentation, baseline definitions |
| Tamarin-ML-API | https://github.com/niklasmedinger/Tamarin-ML-API | `b3a20fc880404ef110a5ea083730843a2e0f6ba2` | locally built JSON API |
| MARISSA | https://github.com/reverseame/MARISSA | `adcd5bc3b94b6aff817da9dc613caa3a62a147d6` | baseline implementation and public PCAPs |
| TamRL published results | https://zenodo.org/records/22705842 | `results.zip`, 29,662,170 bytes, MD5 `e02ea7ce3c5ac7d7337c87a561a00d52` | scale/cost analysis only; not local reproduction |
| Tamarin | https://github.com/tamarin-prover/tamarin-prover/releases/tag/1.12.0 | 1.12.0, revision `82780bbaf3328a45f624ddb41e51bf75425f851c` | standard proof experiments |
| Maude | https://github.com/maude-lang/Maude/releases | 3.5.1 for Tamarin 1.12.0; 3.5 for the API fork | equational reasoning backend |
| Stack | https://github.com/commercialhaskell/stack/releases | 3.11.1 | API build |
| MAFFT | https://mafft.cbrc.jp/alignment/software/ | 7.526 | MARISSA alignment |
| ssdeep/libfuzzy | https://github.com/ssdeep-project/ssdeep/releases | 2.14.1 | MARISSA similarity digest backend |

Exact package versions and tool outputs are committed under `environment/`. Reproduction commands are in `REPRODUCIBILITY.md`. Excluding the local copies does not remove them from the working directory.

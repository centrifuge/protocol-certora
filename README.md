# Formal Verification Report: Centrifuge

This repository is the `certora/` submodule of [centrifuge/protocol](https://github.com/centrifuge/protocol). The harnesses import the protocol's `src/` through relative paths and the confs resolve `lib/` from the protocol root, so run the prover from a protocol checkout with the submodule initialised, not from this repository alone. The protocol marks it `update = none`, so a plain `--init` skips it; fetch it explicitly with `git submodule update --init --checkout certora`. The links below assume that layout.

- Author: [AlexZoid](https://x.com/alexzoid)

| Report | Scope | Commit | Prover | Date | Properties | Proved ✅ | Timeout ⏱️ | Violations ❌ | Mutants |
|---|---|---|---|---|---|---|---|---|---|
| [CORE-FV](./CORE-FV.md) ([PDF](../docs/audits/2026-09-FV.pdf)) | [`src/core`](../src/core): the hub, the spoke and the messaging layer | `74e16461` | 8.19.2 | September 30th, 2026 | 1589 | 1589 | 0 | 0 | [1445](./CORE-FV.md#mutation-testing) |

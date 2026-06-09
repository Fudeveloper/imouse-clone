# XP Public Source Audit

`imouse.source_audit` is the repeatable source-refresh companion for the GUI `Src Refresh` board. It fetches public iMouse XP, Some3C, and PyPI endpoints, records HTTP status, expected-term matches, PyPI package version metadata, local doc timestamps, SOP owner, and claim boundary.

It is source intelligence only. It does not write JSONL field evidence, does not prove real iPhone response, does not prove broad iOS compatibility, and does not prove XP parity.

## Commands

Offline audit, useful before a field run or when the network is blocked:

```powershell
.\.venv\Scripts\python -m imouse.source_audit --offline --markdown evidence\<run_id>_<stage>_xp_public_source_audit.md
```

Live audit, useful before changing source-derived docs, compatibility wording, package dependencies, roadmap priorities, or demo claims:

```powershell
.\.venv\Scripts\python -m imouse.source_audit --markdown evidence\<run_id>_<stage>_xp_public_source_audit.md --allow-failures
```

JSON audit for automation or diff review:

```powershell
.\.venv\Scripts\python -m imouse.source_audit --json --allow-failures
```

## Row Meaning

- `ok`: the URL fetched and expected terms matched. This means the public source is reachable, not that the local prototype controls an iPhone.
- `warn`: the URL fetched but metadata or expected terms drifted. Review the source manually and update docs/tests/SOP before using the claim.
- `pending`: offline mode or intentionally skipped fetch. Treat it as a task, not a pass.
- `fail`: the fetch or JSON parse failed. Do not update public-source-derived claims until this is resolved or explicitly documented.

## SOP

1. Run `Src Refresh` in the GUI and identify the first source/SOP row that is `fail`, `pending`, or `warn`.
2. Run `python -m imouse.source_audit` and export the Markdown report into `evidence/`.
3. For each `warn` or `fail`, manually open the source and decide whether it is a source drift, network issue, site layout change, package registry drift, or irrelevant noise.
4. Convert every accepted source delta into one of: local doc update, GUI row update, test expectation, route decision field, device/iOS matrix entry, package pin/hash review, or explicit rejection.
5. Rerun `Sources`, `Action Map`, `Snapshot`, `XP Timeline`, `Iter Radar`, and `Pack`.
6. Keep Acceptance and Readiness strict: source freshness never replaces real iPhone screenshot, click, swipe, text, manual observation, component ledger, and JSONL evidence.

## Current Source Set

- `https://www.imouse.cc/`
- `https://www.imouse.cc/python-xp/`
- `https://www.imouse.cc/XP%E7%89%88API%E6%96%87%E6%A1%A3/`
- `https://doc.some3c.com/iphone-farm-setup/imouse-xp-new-version`
- `https://doc.some3c.com/iphone-farm-setup/iphone-farm-settings`
- `https://pypi.org/pypi/imouse-py/json`
- `https://pypi.org/pypi/imouse-xp/json`
- `https://pypi.org/pypi/py-imouse-xp/json`

## Package Namespace Drift Guard

The audit intentionally tracks three PyPI namespaces:

| Package | JSON endpoint | Role in the SOP |
|---|---|---|
| `imouse-py` | `https://pypi.org/pypi/imouse-py/json` | Primary public SDK-shape signal because the Python XP page points to `pip install imouse-py`. |
| `imouse-xp` | `https://pypi.org/pypi/imouse-xp/json` | Similar-name package that must be treated as dependency-confusion and drift risk until reviewed. |
| `py-imouse-xp` | `https://pypi.org/pypi/py-imouse-xp/json` | Similar-name package that must be treated as third-party until maintainer, source, hashes, license, and API behavior are reviewed. |

Adoption rule: do not install any lookalike package on field machines until the exact artifact is version-pinned, hash-pinned, source-reviewed, license-reviewed, covered by local API regressions, and backed by receiver/HID/iPhone evidence for the exact scope being claimed.

Package metadata can guide SDK comparison and supply-chain review. It cannot prove screenshot freshness, real iPhone movement, XP hardware authorization, broad iOS compatibility, or XP parity.

## Boundary

The audit can tell the team that a public page or package registry looks reachable and still contains expected keywords. It cannot tell the team that the receiver window is current, the HID command moved the real phone, the SDK works with XP hardware, or a model/iOS pair is locally covered. Those claims still require same-run field evidence, Acceptance PASS, Readiness PASS, and exact device/iOS scope.

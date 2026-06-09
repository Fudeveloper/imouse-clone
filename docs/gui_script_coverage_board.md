# GUI Script Coverage Board

`Script Cov` is the GUI board for XP-style automation/script readiness. It maps stage scenario files, dry-run, real-run guard, metadata records, screenshot probes, HID click/swipe/text lanes, vision/OCR, metrics, group scripts, failure replay, and claim boundaries into one operator table.

Use it before running a real scenario, before scaling from P1 to P3/P4, and before saying a script or queue is XP-like automation.

## GUI Flow

```text
Home -> Snapshot -> Procure -> API Cov -> Script Cov -> Proof Map -> Claim Scope -> Start Pack -> Wizard -> Runner -> Ctrl Ledger -> P1 Trial -> Acceptance/Readiness
```

`Script Cov` exports:

```text
evidence/<run_id>_<stage>_script_coverage.md
```

## What It Checks

| Domain | Purpose | Promotion boundary |
|---|---|---|
| Scenario inventory | Confirms stage scripts parse and the current stage default exists. | A scenario file is a plan, not device evidence. |
| Dry-run contract | Confirms runner dispatch shape before touching hardware. | Dry-run closes only script structure confidence. |
| Real-run guard | Blocks live scripts until route, Doctor, and device count are clean. | Guard allow means "may start", not "phone responded". |
| Component metadata | Ensures receiver, HID, iPhone, hub, cable, and operator are traceable. | Metadata is traceability, not control proof. |
| Screenshot probes | Requires screenshot actions and field screenshot quality gates. | Screenshot proof is not HID proof. |
| HID lanes | Requires click, swipe, and text scripts plus separate Manual observations. | API/HID success is not visible iPhone response. |
| Vision/OCR | Tracks find-image, color, OCR, text, templates, regions, and replay assets. | Helper coverage is not business-flow reliability. |
| Metrics/stability | Tracks repeat and metrics scripts for P2/P3/P4. | Metrics diagnose stability, not manual response. |
| Group batch | Tracks group click/swipe/type and P3/P4 evidence needs. | Local group API or dry-run is not group-control proof. |
| Failure replay | Keeps failures tied to device, category, artifact, and rerun rule. | A rerun plan cannot promote a failed run. |

## Field Rule

Run `Script Cov` after `API Cov` and before disabling Dry Run. If any row is `fail`, `pending`, or unexplained `warn`, use `Run Selected` and fix that lane first.

After `Script Cov`, open `Proof Map` to connect the script/runner surface to the exact Acceptance and Readiness proof rows. Then open `Claim Scope` before handoff so script/API/source progress is not worded as real iPhone control, group control, XP hardware parity, or broad compatibility.

P1 can only be discussed when the same `run_id` has current screenshot quality, lane-separated Manual click/swipe/text observations, no unexplained fail events, Acceptance PASS, Readiness PASS, and exact device/iOS scope.

# GUI Claim Scope

`Claim Scope` is the GUI board for demo, handoff, and acceptance wording. It converts the current Readiness, Acceptance, Proof Map, Evidence Pack, API/Core coverage, compatibility, and XP gap signals into exact allowed claims and forbidden claims.

Use it immediately before any user demo, release note, field handoff, or acceptance summary.

## GUI Flow

```text
Home -> API Cov -> Script Cov -> Proof Map -> Claim Scope -> Start Pack -> Wizard -> Runner -> Acceptance/Readiness
```

`Claim Scope` exports:

```text
evidence/<run_id>_<stage>_claim_scope.md
```

## Claim Rows

| Claim row | What it protects | Closure boundary |
|---|---|---|
| P0 offline assets | Local GUI/API/SOP/source work | Readiness P0 PASS only. It is not field control. |
| P1 single-iPhone control | Real iPhone response wording | Same-run JSONL, screenshot quality, click/swipe/text Manual observations, Acceptance PASS, Readiness PASS, and exact device/iOS/receiver/HID scope. |
| P2 single-device stability | Stability wording | Repeated evidence, metrics, logs, recovery notes, P2 Acceptance/Readiness, and no unresolved fail events. |
| P3/P4 iOS group control | Group-control wording | Per-device lane evidence, Matrix, metrics, artifacts, recovery/triage, and P3/P4 Readiness. |
| XP API/SDK compatibility | XP-style helper/API claims | Only tested local endpoints; hardware-backed claims need receiver/HID/iPhone evidence. |
| XP hardware/wired/firmware/decode parity | XP dedicated hardware parity | Side-by-side hardware or equivalent bench evidence, firmware/binding logs, decode metrics, and field artifacts. |
| Device and iOS compatibility | Supported model/iOS wording | Exact model/iOS/orientation tuple evidence only. Do not generalize from one phone. |
| Docs and SOP handoff wording | Final handoff scope | Evidence Pack, Start Pack, Proof Map, Goal Gate, Readiness, Acceptance, transcript/worksheet, and blocker list. |

## Operator Rule

`Claim Scope` writes wording guidance only. It does not write JSONL evidence and does not prove real iPhone response.

Allowed wording is limited to rows with `pass`. Rows with `ready`, `warn`, `pending`, or `fail` must be presented as open work with the listed forbidden wording excluded.

Do not claim iOS perfect control, XP-equivalent control, group control, hardware parity, or broad iPhone/iOS compatibility until the same run has the field evidence and gate results named in the row.

# GUI Control Evidence Ledger

Use `Ctrl Ledger` during P1 real-iPhone testing, after Route/Doctor/Screenshot are ready and before Acceptance/Readiness handoff.

## Purpose

`Ctrl Ledger` is the lane-separated proof board for real iPhone control. It reads the same `evidence/<run_id>.jsonl` as Control Bench, but it makes the operator close these lanes separately:

| Lane | Minimum proof | Stop line |
|---|---|---|
| HID click | A Manual pass whose step/note names `HID click`, with target, before state, after state, visible pointer/click behavior, and artifact path when useful. | Stop on missing click, wrong target, stuck press, pointer drift, or capture mismatch. |
| HID swipe | A Manual pass whose step/note names `HID swipe`, with direction, distance, release, before/after screen movement, and artifact path. | Stop on inverted direction, wrong distance, no release, stuck press, or calibration drift. |
| Keyboard input | A Manual pass whose step/note names `Keyboard input`, with focused field, expected text, actual visible text, input method state, and artifact path. | Stop on wrong focus, missing/duplicated text, keyboard language/input-method mismatch, or HID binding failure. |

## Operator Flow

1. Run `Prepare`, fill Route Decision, run Doctor, and take a current screenshot.
2. Open `P1 Trial` for the physical action sequence.
3. Open `Ctrl Ledger`.
4. Select `HID click`, `HID swipe`, or `Keyboard input`.
5. Click `Record Pass` only after watching the physical iPhone respond.
6. Click `Record Fail` when the visible result is wrong, then keep category and artifact/log path.
7. Refresh `Ctrl Ledger`, then run Acceptance and Readiness for the same `run_id`.

## Generic Manual Rule

A broad Manual row such as "control smoke looked ok" is context only. It cannot close click, swipe, and text at the same time.

If `Generic Manual quarantine` is fail or warn, rewrite the field observation into three explicit Manual rows:

- `Control ledger - HID click`
- `Control ledger - HID swipe`
- `Control ledger - Keyboard input`

Each row should describe the physical iPhone before/after state. API success, SDK success, exported Markdown, public-source research, or dry-run output cannot replace this.

## Failure SOP

When one lane fails:

| Failure category | First check | Evidence to keep | Rerun rule |
|---|---|---|---|
| `hid` | HID serial, firmware, Hub power, cable, AssistiveTouch pointer state. | HID id, COM/USB log, before/after screen artifact. | Rerun only the affected lane after rebinding HID. |
| `calibration` | Active area, orientation, safe point, coordinate transform. | Screenshot with point, calibration profile, observed offset. | Redo calibration, then rerun click/swipe before scripts. |
| `capture` | Receiver window, stale/black frame, orientation, wrong device. | Current screenshot, receiver log, window/display id. | Rerun Shot Bench before HID lanes. |
| `business_state` | App/page focus, popup, keyboard/input state. | Page screenshot and operator note. | Reset page state, then rerun only the affected lane. |
| `claim_boundary` | Acceptance, Readiness, exact device/iOS scope. | Reports and Evidence Pack. | Do not promote; collect missing same-run evidence. |

## Claim Boundary

`Ctrl Ledger` can make evidence review stricter, but it does not prove real iOS control by itself. P1 remains unverified until the same run has current screenshot quality, lane-specific Manual click/swipe/text passes, no unexplained fail events, Acceptance PASS, Readiness PASS, and exact device/iOS scope.

# GUI Verification Walkthrough

`Verify` is the GUI step-by-step verification walkthrough for one `run_id` and one stage. It is the operator-facing bridge between the long follow-along SOP and the current GUI state.

It does not execute commands, does not write JSONL evidence, and does not prove real iPhone response. It tells the operator what to run next, what result to expect, what evidence to keep, and where to stop.

## When To Open

Open `Verify` after setting the `Evidence run_id` and before claiming any P1/P2/P3/P4 result.

Use it together with:

- `Local` for copy-ready PowerShell command replay.
- `Coach`, `Transcript`, `Wizard`, and `Runner` for field execution.
- `Proof Map`, `Claim Scope`, `Acceptance`, `Readiness`, and `Pack` before handoff.

## Rows

Each row contains:

| Column | Meaning |
|---|---|
| `Phase` | The verification phase, such as offline self-check, run identity, route decision, Doctor, receiver capture, HID manual control, Acceptance/Readiness, stability, group scale, XP parity review, or handoff pack. |
| `Scope` | The stage or operating scope affected by the row. |
| `Status` | `pass`, `ready`, `warn`, `fail`, or `pending`; later rows cannot override an earlier `fail`. |
| `Current` | What the GUI currently knows from route reports, Doctor, JSONL summary, Acceptance, Readiness, and artifact inventory. |
| `Command / GUI path` | The exact command or GUI path to replay. Commands include the current `run_id` and stage. |
| `Expected result` | What must be true before moving forward. |
| `Evidence to keep` | The artifact, JSONL event, report, screenshot, log, or manual observation needed for handoff. |
| `Stop rule` | The condition that blocks promotion or forces rerun. |
| `GUI action` | The panel opened by `Run Selected`. |

## P1 Order

Run the P1 walkthrough top to bottom:

1. Offline self-check: unit tests, compileall, dependency check.
2. Run identity: stable `run_id`, exact device id, stage, operator.
3. Route decision: receiver, capture, HID, iPhone, iOS, Hub, cable, and blockers are real values.
4. Doctor: no `fail`, or a route-aware non-UxPlay receiver decision explains the warning.
5. Receiver capture: current screenshot is not black, stale, cropped, wrong-window, or wrong-device.
6. HID manual control: click, swipe release, and text input each have lane-separated Manual pass/fail observation.
7. Acceptance and Readiness: both pass for the same evidence JSONL and current stage.
8. Handoff pack: required artifacts are present, recommended gaps are acknowledged, and claim wording follows `Claim Scope`.

## Stop Lines

- Stop before HID if route, Doctor, receiver identity, capture binding, iPhone settings, or screenshot quality is not clean.
- Stop if API/HID command success is not matched by visible real-iPhone behavior.
- Stop if a generic Manual note is being used to close click, swipe, and text lanes at once.
- Stop if Acceptance or Readiness fails.
- Stop if `real_ios_verified=False`.
- Stop XP parity wording unless XP dedicated hardware/receiver/firmware/binding evidence exists for the same claim scope.

## Export

Click `Export` in `Verify` to write:

```text
evidence/<run_id>_<stage>_verification_walkthrough.md
```

The export is a test guide and handoff checklist. It is useful only when paired with the actual JSONL evidence, screenshots, manual observations, Doctor, Acceptance, Readiness, and exact device/iOS scope.

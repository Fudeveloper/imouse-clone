# GUI Real-run Guard

`Real-run Guard` is the last GUI stop line before a non-dry-run scenario or command queue can touch hardware. It protects the field run from unverified route, Doctor, or device-scope state.

It does not run the scenario, does not write success evidence, and does not prove real iPhone response. It only decides whether the GUI is allowed to attempt a real run.

## When It Runs

The guard is checked automatically when:

- `Dry Run` is disabled and the operator clicks `Run` for a scenario.
- `Dry Run` is disabled and the operator runs the command queue.

If blocked, the GUI exports:

```text
evidence/<run_id>_<stage>_real_run_guard.md
```

and does not start the real action.

## Checks

| Check | Required before real run | First fix path |
|---|---|---|
| `device_scope` | The selected physical device count meets the current stage requirement. | Select device ids, then refresh Live Probe and Runner. |
| `route_decision` | Route Decision is loaded, valid, ready, and free of placeholders/open blockers. | Route Edit, Receiver, Rx Score, Rx Bootstrap, Rx Setup. |
| `doctor` | Doctor has no hard fail. Route-aware non-UxPlay warnings can be allowed only when the alternate receiver route is explicit. | Doctor, Local, Receiver, Rx Setup. |

## Status Meaning

- `blocked`: do not run real hardware actions. Fix the blocker first.
- `allow`: the GUI may attempt the real run. This is not a pass.

An allowed guard report only proves that the pre-run stop line is clear enough to try. The actual run still needs JSONL events, screenshot artifacts, lane-separated Manual observations, Acceptance, Readiness, and exact device/iOS/receiver/HID scope.

## Required Operator Behavior

1. Keep `Dry Run` enabled until `Route Decision`, `Doctor`, and selected devices are correct.
2. If the guard blocks, open the exported guard report and follow `Next Actions`.
3. After changing receiver, HID, iPhone, Hub, cable, route, or a previously recorded fail, start a fresh `run_id`.
4. After a guard allow, run the scenario once, inspect Timeline/Triage, then run Acceptance and Readiness.
5. Never use `guard ok` as demo wording for iOS control.

## Stop Lines

- Stop if route placeholders remain.
- Stop if `allowed_to_run_p1` is false.
- Stop if Doctor has any hard fail.
- Stop if the selected device list does not match the physical bench.
- Stop if the operator cannot name the exact receiver, HID, Hub port, cable, iPhone model, and iOS version.
- Stop if the team is trying to bypass the GUI guard by calling lower-level APIs directly.

## Boundary

Real-run Guard is a pre-run safety gate. It is not evidence of screenshot freshness, HID movement, text input, XP hardware parity, broad iOS compatibility, or iOS perfect control.

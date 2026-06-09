# GUI Receiver Evidence Checklist

`Rx Evidence` is the receiver/capture proof checklist in the Python GUI. Use it after `Rx Setup` and before `P1 Trial`, especially when the default UxPlay route is blocked and the run uses `windows_receiver`, `wired`, or `capture_card`.

This board is an SOP and handoff artifact. The export itself does not write JSONL evidence, does not prove real iPhone response, and does not prove XP parity.

## GUI Flow

Use the Live Probe workflow:

```text
Home -> Action Map -> Src Refresh -> Src Audit -> Pkg Guard -> XP Drill -> XP Timeline -> XP Arch -> XP Lab -> Coach -> Rx Score -> Rx Bootstrap -> Rx Setup -> Rx Evidence -> Transcript -> Start Pack -> Wizard -> Runner -> Ctrl Ledger -> P1 Trial -> Acceptance/Readiness
```

Click `Rx Evidence` when the receiver route is selected and the operator needs a step-by-step capture proof order before HID actions.

## What It Checks

`Rx Evidence` reads the same current state as the rest of the field GUI:

- Route Decision JSON path, receiver route, receiver identity, capture method, window binding, HID id, iPhone model, and iOS version.
- Route validation result and open blockers.
- Receiver provider preflight.
- Route-aware Doctor status, including whether `binary:uxplay` is still a hard fail or a route-specific warning.
- Acceptance screenshot quality, component metadata, and manual observation rows.
- Readiness claim state.
- Evidence JSONL summary, failed event count, and metrics count.

## Checklist Order

The board keeps the receiver route separate from HID and claim wording:

| Order | Meaning | Stop line |
|---|---|---|
| Lock one receiver route | One run_id uses exactly one receiver lane. | Stop on placeholders, mixed routes, open blockers, or a failed route decision already recorded for the run_id. |
| Receiver provider preflight | Provider fields can be evaluated before real capture work. | Stop if path, AirPlay name, capture method, or window binding is missing. |
| Route-aware Doctor | Doctor is run with the Route Decision path. | Stop on any fail; do not bypass Real-run Guard. |
| Bind receiver identity | The iPhone, receiver window/source, capture method, HID, and device_id are traceable together. | Stop if the visible receiver window cannot be tied to a code-captured frame. |
| Baseline screenshot proof | One current, non-black screenshot exists before HID. | Stop on black, stale, wrong-window, wrong-device, cropped, or manual-only frames. |
| Receiver capture probe set | Repeated screenshots, artifacts, metrics, and logs are collected. | Stop if placeholder metadata is recorded as pass or receiver failures are hidden. |
| Reconnect and log triage | Failed discovery/stream/capture/binding/performance paths have logs and rerun decisions. | Stop scaling if failures cannot be isolated to device, receiver, route, window, cable, or log line. |
| HID handoff stop line | Only clean receiver proof moves to P1 Trial. | Stop if Manual observation is generic or screenshot proof is missing. |
| Acceptance and claim closure | Acceptance and Readiness decide claim wording. | Stop all perfect-control, group-control, broad-compatibility, or XP-parity wording until both pass for the same run_id. |

## Copy-Ready Commands

The export includes commands for:

```powershell
.\.venv\Scripts\python -m imouse.route_decision validate evidence\<run_id>_route_decision.json --require-ready --markdown evidence\<run_id>_route_decision.md
.\.venv\Scripts\python -m imouse.doctor --route-decision evidence\<run_id>_route_decision.json --markdown evidence\<run_id>_doctor.md
.\.venv\Scripts\python -m imouse.script_runner scripts\p1_receiver_capture_probe.json --run-id <run_id> --dry-run
.\.venv\Scripts\python -m imouse.script_runner scripts\p1_receiver_capture_probe.json --run-id <run_id>
.\.venv\Scripts\python -m imouse.acceptance evidence\<run_id>.jsonl --gate p1 --markdown evidence\<run_id>_p1_acceptance.md --gap-markdown evidence\<run_id>_p1_acceptance_gap.md
.\.venv\Scripts\python -m imouse.readiness --target p1 --evidence evidence\<run_id>.jsonl --markdown evidence\<run_id>_p1_readiness.md
```

The script runner commands can write field evidence when run against a real service and edited with real metadata. The GUI export does not run them by itself.

## Boundary

- `Rx Evidence` does not install, start, or validate a receiver by itself.
- `Rx Evidence` does not replace `Shot Bench`, `P1 Trial`, `Ctrl Ledger`, `Acceptance`, or `Readiness`.
- A clean receiver checklist is not an iOS control pass.
- A Windows/wired/capture-card alternate route can remove the local UxPlay blocker only when route-aware Doctor has no fail checks.
- XP parity still requires XP hardware/firmware/wired/hard-decode evidence and side-by-side artifacts.


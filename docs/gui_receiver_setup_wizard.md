# GUI Receiver Setup Wizard

`Rx Setup` is the route-aware receiver setup guide in the Python GUI. It turns the current Route Decision into an operator checklist for installing, starting, binding, and triaging the selected receiver lane.

It is a guide only. It does not install software, start a receiver, write JSONL evidence, or prove real iPhone control.

## GUI Path

Open the Live Probe workflow:

```text
Home -> Action Map -> Src Refresh -> Src Audit -> XP Drill -> XP Timeline -> XP Arch -> XP Lab -> Coach -> Rx Score -> Rx Bootstrap -> Rx Setup -> Rx Evidence -> Transcript -> Route/Kit -> Local -> Screenshot -> P1 Trial -> Events/Problems -> Acceptance/Readiness
```

Click `Rx Score` after `Coach`, use `Rx Bootstrap` when an alternate receiver route needs a route-decision draft, click `Rx Setup` for route install/binding, then click `Rx Evidence` before HID control tests. Select the first row that is not `pass`, then use `Run Selected` or the command shown in that row.

## What It Checks

The wizard reads the same state as the rest of the field GUI:

- Route Decision JSON path, run_id, receiver route, receiver name, version, path, start command, AirPlay name, capture method, window binding, license/status, and any `Rx Bootstrap` draft values.
- Route validation report and open blockers.
- Doctor checks for `receiver_provider` and `binary:uxplay`.
- Acceptance rows for screenshot quality and manual real-iPhone observation.
- Readiness claim `real_ios_control_verified`.
- Evidence summary counts and failed event count.

## Route Lanes

The selected route must be exactly one of these:

| Route | Main use | P1 gate |
|---|---|---|
| `uxplay` | Open-source AirPlay receiver prototype | `binary:uxplay` is pass, unique AirPlay name is visible, screenshot quality passes |
| `windows_receiver` | Windows product-like receiver fallback | provider preflight passes, license/version/path are recorded, window binding is stable |
| `wired` | Wired projection or vendor SDK path | driver/device/cable identity is recorded and frames are captured automatically |
| `capture_card` | HDMI/capture-card diagnostic or fallback path | card/input/resolution are recorded and artifacts map to the selected device_id |

Do not mix routes inside one run. If a failed route decision or failed real-device evidence has already been recorded, fix the setup under a fresh run_id.

## Stop Rules

- Stop if the route file cannot be identified for the run_id.
- Stop if Route Decision validation fails or still has placeholders.
- Stop if the selected `uxplay` lane has `binary:uxplay=fail`.
- Stop if an alternate receiver route still leaves Doctor with `binary:uxplay=fail`; Doctor must be run with the Route Decision path so the missing UxPlay dependency becomes a route-specific warning.
- Stop if capture can point to the wrong window, stale display, hidden window, or manual-only screenshot.
- Stop HID tests until screenshot quality is pass.
- Stop any perfect-control, broad iOS compatibility, or XP parity claim until JSONL evidence, Manual observation, Acceptance, and Readiness all pass.

## Export

`Export` writes:

```text
evidence/<run_id>_<stage>_receiver_setup_wizard.md
```

The export includes a setup table and a `Copy-Ready Commands` block for route init, route validation, Doctor, and the selected receiver lane. This file is an operator guide and handoff artifact, not evidence of real iPhone response.

## Follow-Up Test

After a clean setup lane:

1. Run `Receiver` to confirm route gate status.
2. Run `Rx Evidence` to lock receiver/capture proof commands, artifacts, and stop lines.
3. Run `Doctor` with the Route Decision path.
4. Run `Shot Bench` and keep frame artifacts.
5. Run `P1 Trial` for click, swipe, and text input.
6. Attach receiver/HID logs for every failure.
7. Run Acceptance.
8. Run Readiness.

Only the final evidence, Acceptance, and Readiness reports can support a P1 control claim.

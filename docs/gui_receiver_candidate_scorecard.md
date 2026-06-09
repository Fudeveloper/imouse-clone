# GUI Receiver Candidate Scorecard

`Rx Score` is the receiver-route selection scorecard in the Python GUI. It compares `uxplay`, `windows_receiver`, `wired`, and `capture_card` before the operator locks the receiver lane for a field run.

Use the Live Probe workflow:

```text
Home -> Action Map -> Src Refresh -> Src Audit -> XP Drill -> XP Timeline -> XP Arch -> XP Lab -> Coach -> Rx Score -> Rx Bootstrap -> Rx Setup -> Rx Evidence -> Transcript -> Route/Kit -> Local -> Screenshot -> P1 Trial -> Events/Problems -> Acceptance/Readiness
```

Open `Rx Score` after `Coach` and before `Rx Bootstrap` / `Rx Setup` when:

- `uxplay` is missing or unstable.
- a commercial Windows receiver is available but needs license/window-binding review.
- a wired route or capture card may be more stable for the first real-iPhone proof.
- the team needs a written reason for why one receiver route was selected.

The scorecard reads current GUI state and cached reports:

- Route Decision JSON and route validation report.
- Doctor report, especially `binary:uxplay` and `receiver_provider`.
- Acceptance screenshot/manual rows when evidence exists.
- Readiness preview or final Readiness report.
- Evidence summary counts and failure counts.

## Columns

- `Candidate`: receiver lane being compared.
- `Status`: `fail`, `pending`, `warn`, `ready`, or `pass`.
- `Recommendation`: `recommended`, `blocked`, `route-needed`, `selected-needs-proof`, or `backup`.
- `Selected`: whether the current Route Decision selects this lane.
- `Score`: explainable score from source, route, install, binding, screenshot, logs, Python integration, license/product risk, and XP alignment.
- `Current signal`: current route/provider/doctor/screenshot/manual/evidence state.
- `Strengths`: why the candidate is attractive for the current run.
- `Gaps`: what still blocks or weakens the candidate.
- `Next action`: the next GUI step.
- `Stop rule`: when to stop and avoid mixing receiver evidence.

## Route Selection SOP

1. Click `Rx Score`.
2. Start from any `fail` row, especially selected-route failures.
3. If no route file exists, click `Edit Route` and fill real receiver/HID/iPhone values.
4. If `UxPlay open receiver` is blocked by `binary:uxplay=fail`, either install UxPlay or select a valid alternate route under a fresh run_id.
5. If `Windows AirPlay receiver` is recommended, click `Rx Bootstrap` and fill version/license, path, start command, AirPlay name, capture method, and window binding before setup.
6. If `wired` or `capture_card` is recommended, click `Rx Bootstrap`, label cable/card/driver/input, and prove automatic frame capture before HID.
7. Click `Rx Setup` for the selected route.
8. Click `Rx Evidence` to organize receiver/capture proof commands, artifacts, and stop lines.
9. Run Doctor with the same Route Decision path.
10. Run Screenshot / Shot Bench before P1 Trial.
11. Use Acceptance and Readiness after JSONL evidence exists.

## Boundary

- `Rx Score` does not write JSONL evidence.
- `Rx Score` does not start or install a receiver.
- `Rx Bootstrap` may create a Route Decision draft for an alternate receiver, but it still keeps P1 blocked.
- A `recommended` row is not a real-iPhone pass.
- A `ready` row is not iOS perfect control.
- XP parity still requires side-by-side capability evidence, API behavior, receiver/capture/HID proof, SOP coverage, and field stability evidence.

Export path:

```text
evidence/<run_id>_<stage>_receiver_candidate_scorecard.md
```

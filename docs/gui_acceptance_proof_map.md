# GUI Acceptance Proof Map

`Proof Map` is the GUI board that links each Acceptance and Readiness gate to the exact field evidence, GUI action, artifact, command, and stop rule that can close it.

Use it after `Script Cov` and before `Claim Scope`. It is meant for operators who need to know which missing evidence blocks P1/P2/P3/P4 and which GUI button to use next.

## GUI Flow

```text
Home -> Snapshot -> Procure -> API Cov -> Script Cov -> Proof Map -> Claim Scope -> Start Pack -> Wizard -> Runner -> Ctrl Ledger -> P1 Trial -> Acceptance/Readiness
```

`Proof Map` exports:

```text
evidence/<run_id>_<stage>_proof_map.md
```

## What It Maps

| Proof row | Closes | Required evidence |
|---|---|---|
| Run scope | Field evidence starting point | Same run_id, selected physical devices, stage target, JSONL path. |
| Route and Doctor | Route/doctor readiness | Route Decision, component metadata, route-aware Doctor report. |
| Evidence exists | Acceptance `evidence_exists` | Current JSONL with field events. |
| No fail events | Acceptance `no_fail_events` | Fresh run with zero unresolved fail events. |
| Device traceability | Acceptance `device_traceability` | Device ids matching P1/P2/P3/P4 stage count. |
| Component traceability | Acceptance `component_traceability` | Receiver, capture, HID, iPhone identity, iOS version, no placeholders. |
| Screenshot quality | Acceptance `screenshot_quality` | Current, correctly bound, nonblank screenshots and artifacts. |
| Manual observation | Acceptance `manual_observation` | Real iPhone response observed by the operator. |
| Lane separation | Local P1 control boundary | Separate Manual pass rows for HID click, HID swipe, and keyboard input. |
| Metrics | P2/P3/P4 stability | Metrics samples, repeated screenshots, logs, recovery notes. |
| Acceptance gate | Stage acceptance | Acceptance PASS and Gap export when it fails. |
| Readiness gate | Stage readiness | Readiness PASS with closed doctor/evidence/acceptance blockers. |
| Claim boundary | Handoff wording | Exact device/iOS/receiver/HID scope supported by the same run. |

## Field Rule

`Proof Map` does not write evidence and does not prove real iPhone response. It only tells the operator where the missing proof belongs.

After `Proof Map`, open `Claim Scope` before demo or handoff. `Claim Scope` converts the current proof state into allowed and forbidden wording, but it also does not write JSONL evidence or prove real iPhone response.

Do not claim iOS perfect control, XP parity, or broad compatibility unless the same `run_id` has current screenshot quality, lane-separated Manual click/swipe/text observations, no unresolved fail events, Acceptance PASS, Readiness PASS, and exact device/iOS/receiver/HID scope.

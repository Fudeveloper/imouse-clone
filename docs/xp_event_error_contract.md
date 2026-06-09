# XP Event/Error Contract

Updated: 2026-06-09

This document defines the GUI/SOP contract for XP-style API events, callbacks, logs, and errors. It is an implementation guide and audit checklist. It is not field evidence, and it does not prove XP parity or real iOS control.

## Contract Goals

The XP edition benchmark is not only a click API. The product contract needs these layers to stay aligned:

- API envelope: HTTP and WebSocket `/api` calls use `fun`, echo `msgid`, and return `status`, `message`, and `data.code`.
- Request transport: GET, POST JSON, POST form, multipart screenshot, and WebSocket requests must be replayable outside the GUI.
- Callback lifecycle: callbacks/events are debug and ops signals until paired with JSONL evidence.
- Field event sources: receiver, capture, HID, device, group, and ops events must carry device/component context.
- Error taxonomy: receiver/capture/HID, vision/OCR/script, group, and ops errors must stay explicit.
- Log ingestion: raw receiver/HID logs should be attached, classified, and linked to rerun decisions.
- Claim boundary: API success, callbacks, logs, or markdown exports never prove real iPhone response by themselves.

## GUI Entry

Use the Live Probe `Events` button to open the event/error contract board. Export creates:

```text
evidence/<run_id>_<stage>_xp_event_error_contract.md
```

The board reads the current Route Decision state, Doctor result, Acceptance/Readiness preview, evidence JSONL summary, XP Gap audit, and callback rows. It does not write JSONL evidence.

## Status Meanings

| Status | Meaning |
|---|---|
| `pass` | The contract is backed by the current stage gates and real evidence. This is rare and still scoped to the same run_id. |
| `ready` | The local implementation or supporting evidence is ready for field use, but it is not a product claim. |
| `warn` | The layer exists but has a proof boundary, callback/log warning, partial XP gap, or real_ios_verified is false. |
| `pending` | Required route, callback, evidence, or gate data has not been produced yet. |
| `fail` | A hard blocker exists, such as Doctor fail, route fail, missing required docs, or failed gate. |

## Error Taxonomy

Use these categories consistently in JSONL evidence, Attach Log triage, Problems, Rerun, and Recovery:

| Category | Meaning | First GUI action |
|---|---|---|
| `airplay_discovery` | iPhone cannot find or keep the receiver identity. | Receiver, Doctor, Route Edit |
| `airplay_stream` | AirPlay connects but frames are black, stale, wrong, or unstable. | Shot Bench, Attach Log |
| `capture` | Screenshot capture, window binding, crop, orientation, or artifact failure. | Shot Bench, Receiver |
| `hid` | Mouse/keyboard command is sent but real iPhone response is missing or wrong. | Control Bench, P1 Trial |
| `calibration` | Coordinate mapping, orientation, active area, or safe-point drift. | P1 Trial, calibration |
| `vision_template` | Template matching miss or false positive. | Assets, Scenario Library |
| `vision_color` | Color or multi-color match drift. | Assets, Scenario Library |
| `ocr` | OCR/text recognition miss, model issue, or crop drift. | Assets, Scenario Library |
| `group_dispatch` | Batch/group result hides per-device failure. | Matrix, Rerun |
| `performance` | Latency, reconnect, fps, resource, or long-run instability. | Dashboard, Recovery |
| `business_state` | Page, keyboard, popup, login, language, or app state drift. | Timeline, Triage |
| `route_decision` | Route/bench metadata missing, placeholder-shaped, or blocked. | Route Edit, Doctor |
| `uncategorized` | Failure cannot yet be tied to a known lane. | Triage, Problems |

## SOP

1. Run `Local` commands after code changes.
2. Validate Route Decision and Doctor before any real HID action.
3. Use `Events` before rerun to review API envelope, callback state, error taxonomy, and claim boundary.
4. Use `Callback` and `Attach Log` to inspect or ingest raw event/log context.
5. Use `Timeline`, `Matrix`, and `Triage` to connect each failure to device id, step, category, and artifact.
6. Use `Problems`, `Rerun`, and `Recovery` to decide the smallest replay path and whether a fresh run_id is required.
7. Run Acceptance and Readiness only after the same run_id has screenshot quality, manual observation, and component metadata.

## Boundaries

- Callback rows are diagnostic context, not control proof.
- Attach Log can write log-triage JSONL evidence, but logs still do not replace screenshot quality or Manual observation.
- Local config/user/shortcut helpers are compatibility scaffolding only.
- CH9329/general HID evidence does not prove XP dedicated hardware, 4.4 firmware, wired projection, auto-binding, or licensing parity.
- Public XP API and help pages are backlog inputs until converted into local evidence and stage gates.

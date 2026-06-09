# GUI XP Hardware Lab

`XP Lab` is the GUI board for hardware procurement and lab validation. It turns the XP-style public hardware, receiver, projection, HID, and group-control signals into practical buying decisions, bench tests, required evidence, and stop rules.

It is intentionally not a success screen. A `ready` row means the lab lane is reviewable for the current run; it does not prove real iPhone response, broad compatibility, or XP dedicated-hardware parity.

## Operator Path

Home -> Action Map -> Src Refresh -> Src Audit -> XP Drill -> XP Timeline -> XP Arch -> XP Lab -> Coach -> Rx Score -> Rx Bootstrap -> Rx Setup -> Transcript -> Route/Kit -> Local -> Screenshot -> P1 Trial -> Events/Problems -> Acceptance/Readiness

Open `XP Lab` before buying receiver/HID hardware, before changing Route Decision, and before making XP parity claims.

## Lanes

| Lane | Purpose | Evidence gate |
|---|---|---|
| Route and procurement ledger | Locks one receiver, one HID lane, one iPhone, one hub/cable path, and one operator. | Route Decision JSON/report and Doctor. |
| Receiver/capture rig | Compares UxPlay, Windows receiver, wired projection, and capture-card fallback. | Receiver metadata, screenshot artifacts, window/device binding, logs. |
| Windows/wired/decode lane | Separates product receiver work from the UxPlay prototype. | fps/latency/reconnect notes and screenshot stability samples. |
| HID controller rig | Separates generic CH9329/self-built proof from XP dedicated hardware. | HID identity, firmware, serial, manual click/swipe/type observations. |
| XP dedicated hardware parity | Keeps XP hardware, firmware, and auto-binding claims separate. | Legal side-by-side XP hardware artifacts. |
| iPhone settings fixture | Makes iPhone settings reproducible. | model/iOS, AssistiveTouch, pointer profile, baseline screenshot. |
| Hub, cable, and power map | Prevents physical drift from being misdiagnosed as script failure. | hub id, port, cable id, power path, operator note. |
| Capture stability and metrics | Moves from first screenshot to repeatable product evidence. | screenshot samples, metrics, reconnect timing, dashboard. |
| Logs and recovery bridge | Keeps receiver/HID/script failures explainable. | raw logs, parsed callbacks, triage, recovery, rerun decision. |
| Scale procurement boundary | Blocks premature group buying and group claims. | P2/P3/P4 per-device artifacts, metrics, logs, readiness. |

## Follow-Along Test

1. Click `Route Init` or `Route Edit`; replace every placeholder with real bench values.
2. Click `Validate`, then `Doctor`.
3. Open `XP Lab` and start from the first `fail`, `pending`, or `warn` row.
4. Use `Run Selected` to open the owning board, such as `Rx Score`, `Rx Bootstrap`, `Bench`, `Control Bench`, `iOS SOP`, `Shot Bench`, `Attach Log`, or `Dashboard`.
5. Export `XP Lab` to `evidence/<run_id>_<stage>_xp_hardware_lab.md`.
6. Continue only when the current row has the required artifacts for the same `run_id`.

## Boundaries

- `XP Lab` is a procurement and lab validation board; it does not write JSONL field evidence.
- CH9329 or self-built HID success is generic HID proof only.
- XP dedicated hardware parity needs legal side-by-side hardware evidence.
- Windows receiver, wired projection, hardware decode, and auto-binding claims need measured local artifacts.
- No row can override Acceptance, Readiness, manual observation, screenshot quality, or same-run evidence.

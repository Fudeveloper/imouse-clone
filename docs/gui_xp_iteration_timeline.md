# GUI XP Iteration Timeline

`XP Timeline` is the GUI board for reviewing the inferred iMouse XP product iteration path. It turns public XP signals into chronological R&D lessons, common pitfalls, SOP gates, required evidence, and stop rules.

It sits between source refresh and implementation planning:

```text
Sources -> Src Refresh -> Action Map -> XP Timeline -> Iter Radar -> XP Drill -> XP Arch -> XP Lab -> Roadmap
```

## Operator Path

Home -> Action Map -> Src Refresh -> Src Audit -> XP Drill -> XP Timeline -> XP Arch -> XP Lab -> Coach -> Rx Score -> Rx Bootstrap -> Rx Setup -> Transcript -> Route/Kit -> Local -> Screenshot -> P1 Trial -> Events/Problems -> Acceptance/Readiness

Open `XP Timeline` after `Src Refresh` and `Action Map`, before changing roadmap priorities, hardware procurement, or parity wording.

## Timeline Phases

| # | Phase | Why it matters |
|---|---|---|
| 01 | No-app black-box control | Separates real iPhone response from API/HID success. |
| 02 | Kernel/API and Console split | Keeps GUI, scripts, callbacks, client helpers, and evidence on one service boundary. |
| 03 | Receiver/projection productization | Makes AirPlay/wired receiver, window binding, decode, reconnect, and logs a product lane. |
| 04 | Firmware, wired projection, and binding | Prevents CH9329 proof from becoming XP hardware or 4.4 firmware parity wording. |
| 05 | Vision, OCR, and script assets | Turns OpenCV/OCR calls into replayable assets, regions, thresholds, and artifacts. |
| 06 | Logs, recovery, and group scale | Blocks group claims until failures are isolated by device, component, log, and metrics. |
| 07 | Source refresh and claim governance | Keeps public claims, package signals, and GUI exports out of acceptance wording. |

## Follow-Along Test

1. Run `Sources` and `Src Refresh`.
2. Run `Action Map`.
3. Click `XP Timeline`.
4. Start from the first `fail`, `pending`, or `warn` row.
5. Use `Run Selected` to open the owning GUI board.
6. Export `XP Timeline` to `evidence/<run_id>_<stage>_xp_iteration_timeline.md`.
7. Re-open `Iter Radar`, `XP Drill`, `XP Arch`, `XP Lab`, and `Roadmap` after the row has enough same-run evidence.

## Boundaries

- `XP Timeline` is product-iteration intelligence, not JSONL evidence.
- A public XP signal never proves our receiver, HID, screenshot, OCR, group, or parity behavior.
- A `ready` row is reviewable only for the current stage and evidence scope.
- Perfect-control, broad iOS compatibility, and XP parity wording still require same-run field evidence, Acceptance, Readiness, and exact device/iOS coverage.

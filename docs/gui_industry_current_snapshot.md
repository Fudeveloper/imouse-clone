# GUI Industry Current Snapshot

`Snapshot` is the Live Probe board for current industry/source/SOP state. It turns `docs/industry_current_state_snapshot_2026.md` into operator rows for procurement, route choice, receiver setup, HID proof, iPhone settings, API/Console boundaries, vision replay, group isolation, and claim wording.

Use it before `Routes`, `Kit Gate`, `iOS SOP`, `Start Pack`, procurement review, or demo wording.

## Operator Path

```text
Home -> Snapshot -> Procure -> Action Map -> Src Refresh -> Src Audit -> XP Drill -> XP Timeline -> XP Arch -> XP Lab -> Coach -> Rx Score -> Rx Bootstrap -> Rx Setup -> Transcript -> Route/Kit -> Local -> Screenshot -> Wizard -> Runner -> Ctrl Ledger -> P1 Trial -> Events/Problems -> Acceptance/Readiness
```

## Follow-Along Test

1. Start the GUI with `python -m imouse.gui`.
2. Set `Evidence` and `Stage`.
3. Click `Snapshot`.
4. Confirm offline rows do not claim receiver, HID, iOS settings, group scale, or XP parity as proven.
5. Select the first `fail`, `pending`, or `warn` row and click `Run Selected`.
6. Export the board to `evidence/<run_id>_<stage>_industry_current_snapshot.md`.
7. Continue through `Procure`, `Routes`, `Kit Gate`, `iOS SOP`, `Rx Bootstrap`, `Rx Setup`, `Shot Bench`, `P1 Trial`, `Acceptance`, and `Readiness`.

## Boundaries

- `Snapshot` is a current-state/SOP map, not JSONL evidence.
- It does not browse automatically, install receiver software, connect HID hardware, or prove real iPhone response.
- It can identify the next action, but only same-run field evidence, saved screenshots, Manual/P1 Trial observations, Acceptance, Readiness, logs, and exact device/iOS scope can support a claim.
- Public iMouse/XP/Apple/Some3C signals are inputs to testing, not local compatibility or parity proof.
- When website compatibility wording changes, update `docs/industry_current_state_snapshot_2026.md` first, then use `Snapshot` to convert it into test rows.

# GUI P1 Test Coach

Updated: 2026-06-09

`Coach` is the operator-facing real-device P1 test guide in the Python GUI. It turns the first iPhone run into a fixed sequence with current status, GUI entry, command, pass criteria, failure handling, evidence to keep, and stop rule.

It is not evidence. It does not execute commands by itself, does not write JSONL evidence, and does not prove real iPhone control.

## GUI Path

Start the GUI:

```powershell
cd D:\codex-projects\imouse-clone
.\.venv\Scripts\python -m imouse.gui
```

Use the Live Probe workflow:

```text
Home -> Action Map -> Src Refresh -> Src Audit -> XP Drill -> XP Timeline -> XP Arch -> XP Lab -> Coach -> Rx Score -> Rx Bootstrap -> Rx Setup -> Transcript -> Route/Kit -> Local -> Screenshot -> P1 Trial -> Events/Problems -> Acceptance/Readiness
```

Click `Coach`, select the first `fail`, `pending`, or `warn` row, then click `Run Selected`.

## Export

`Export` writes:

```text
evidence/<run_id>_<stage>_p1_test_coach.md
```

The export is included in the GUI Evidence Pack as `P1 Test Coach`.

## Step Order

1. Run identity and device scope.
2. Source-derived SOP gates.
3. Route Decision.
4. Local command replay.
5. Preflight Doctor.
6. Field kit and iOS settings.
7. Receiver screenshot and Shot Bench.
8. Coordinate calibration.
9. HID click.
10. HID swipe.
11. Keyboard input.
12. Replayable script and logs.
13. Acceptance.
14. Readiness and handoff.

`Coach` owns the end-to-end P1 run. `Src Refresh` owns public-source freshness before route or claim changes. `XP Lab` owns hardware procurement and lab validation boundaries before buying or claiming parity. `Rx Score` owns receiver candidate selection when the operator must choose between `uxplay`, `windows_receiver`, `wired`, and `capture_card`. `Rx Bootstrap` owns the route-decision draft for alternate receiver lanes while keeping P1 blocked. `Rx Setup` owns the route-specific receiver install/binding split before Step 7. `Transcript` owns the fillable human observation log; it still does not replace JSONL Manual evidence.

## Pass Rule

The P1 run is not complete until the same `run_id` has:

- Route Decision ready.
- Doctor without fail.
- Current nonblank screenshot evidence.
- Manual pass observations for click, swipe, and text input.
- Acceptance PASS.
- Readiness PASS with real iOS control verified.
- No unexplained fail events.

## Failure Rule

Work from the first non-pass Coach row. If receiver, HID, cable, Hub, iPhone settings, selected device, or route identity changes, start a fresh `run_id` after fixing the blocker.

API/HID command success is not a pass unless the operator sees the real iPhone respond and records Manual evidence for the same run.

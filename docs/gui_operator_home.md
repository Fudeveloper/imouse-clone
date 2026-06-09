# GUI Operator Home

Updated: 2026-06-09

`Home` is the operator-facing workflow map in the Python GUI. It groups the crowded Live Probe buttons into one ordered board:

1. Operator intake.
2. Knowledge and acceptance boundary.
3. Route, kit, and iPhone settings.
4. Local reproducibility.
5. Receiver screenshot proof.
6. HID click, swipe, and text proof.
7. Repeatable script path.
8. Acceptance proof map.
9. Claim scope and handoff wording.
10. XP core, API coverage, and event contract.
11. Problem ledger and rerun path.
12. Evidence pack, acceptance, and handoff.

It is a navigation and audit board. It does not write JSONL evidence and does not prove real iPhone response.

## GUI Path

Start the GUI:

```powershell
cd D:\codex-projects\imouse-clone
.\.venv\Scripts\python -m imouse.gui
```

In the bottom `Live Probe` area, use the compact workflow row:

```text
Home -> Snapshot -> Procure -> API Cov -> Script Cov -> Proof Map -> Claim Scope -> Action Map -> Src Refresh -> Src Audit -> XP Drill -> XP Timeline -> XP Arch -> XP Lab -> Coach -> Rx Score -> Rx Bootstrap -> Rx Setup -> Transcript -> Route/Kit -> Local -> Screenshot -> Wizard -> Runner -> Ctrl Ledger -> P1 Trial -> Events/Problems -> Acceptance/Readiness
```

Click `Home` to open the board. Select the first `fail`, `pending`, or `warn` row, then click `Run Selected` to jump to the primary GUI action. After creating an artifact or recording evidence, click `Refresh`.

## Export

The `Export` button writes:

```text
evidence/<run_id>_<stage>_operator_home.md
```

The export is included in the Evidence Pack as `GUI Operator Home`.

## Step-By-Step Use

1. Set `Evidence` run id and select the physical device rows.
2. Click `Prepare`.
3. Click `Home`.
4. Click `Action Map` and resolve the first source-derived SOP gate before changing hardware scope.
5. Click `Coach` and follow the first non-pass P1 testing row.
6. Resolve the first non-pass Home row.
7. When `Route, kit, and iPhone settings` is blocked, fill Route Decision, run Doctor, open Receiver, Kit Gate, and iOS SOP.
8. When `Local reproducibility` is blocked, open `Local` and replay the listed PowerShell commands.
9. When `Receiver screenshot proof` is blocked, run Screenshot, Shot Bench, calibration, Wizard, and Runner.
10. When `HID click, swipe, and text proof` is blocked, use Ctrl Ledger, P1 Trial, and Control Bench while watching the real iPhone, then record lane-specific Manual pass/fail.
11. When `Repeatable script path` is blocked, open Script Cov, Scenario Library, Dry Run, Runner, and Real-run Guard before disabling dry-run.
12. When `Acceptance proof map` is blocked, open Proof Map and follow the first failed evidence gate before handoff.
13. When `Claim scope and handoff wording` is blocked, open Claim Scope and remove any wording that turns P0/GUI/API/source progress into real iPhone control, group control, XP hardware parity, or broad compatibility.
14. When `XP core, API coverage, and event contract` is blocked, open Core, API Cov, Events, Callback, Attach Log, and XP Gap before making API/SDK parity claims.
15. When failures exist, open Problems, Triage, Rerun, Recovery, Timeline, and Review before changing scripts or expanding devices.
16. Finish with Pack, Dashboard, Acceptance, Gap if needed, Readiness, and Session.

## Local Verification

Use these commands after exporting Home and before a real P1 run:

```powershell
.\.venv\Scripts\python -m unittest discover -s tests -v
.\.venv\Scripts\python -m compileall -q imouse tests
.\.venv\Scripts\python -m imouse.main --check
.\.venv\Scripts\python -m imouse.doctor --json
.\.venv\Scripts\python -m imouse.doctor --route-decision evidence\<run_id>_route_decision.json --json
.\.venv\Scripts\python -m imouse.script_runner scripts\p1_single_device_control_probe.json --dry-run --run-id <run_id>
.\.venv\Scripts\python -m imouse.readiness --target <stage> --evidence evidence\<run_id>.jsonl
```

Expected offline result on the current prototype: unit tests and compileall can pass, but `main --check`, Doctor, and Readiness can still fail or warn when `uxplay`, real receiver/HID, and real evidence are missing.

## Claim Boundary

Do not use Home, Procure, Pack, Dashboard, Start Pack, Runner, Ctrl Ledger export, API Cov, Script Cov, Proof Map, Claim Scope, Events, Core, Roadmap, or XP Gap as real-control proof.

Real iOS control requires all of these for the same `run_id`:

- current screenshot quality evidence;
- visible click, swipe release, and text input on the real iPhone;
- Manual pass/fail records with device id, category, note, and artifact when needed;
- Acceptance PASS;
- Readiness PASS with `real_ios_control_verified=true`;
- no unresolved fail events, or a documented Rerun/Recovery decision.

XP parity claims require a separate hardware/receiver comparison. A CH9329 or prototype receiver pass does not prove iMouse XP dedicated hardware, firmware 4.4, wired projection, auto-binding, licensing, or broad compatibility.

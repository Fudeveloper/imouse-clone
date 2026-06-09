# GUI XP Iteration Drill Board

`XP Drill` 是 Live Probe 里的 XP 迭代细节验证板。它把公开的 iMouse XP 迭代/帮助/API/package 信号拆成可执行 drill：

- Windows Core/Kernel service and Console split.
- iOS settings, mouse parameter profile, QR policy, orientation, calibration context.
- Receiver/projection/window binding, wired route, hard decode, screenshot stability.
- XP dedicated hardware, 4.4 firmware, wired projection auto-binding, release behavior.
- Python/package namespace drift and SDK adoption boundary.
- Restart/recovery/log ingestion and rerun discipline.
- P3/P4 multi-device projection and per-device failure isolation.
- Claim boundary before demo, handoff, compatibility, or XP parity wording.

## GUI Entry

Use the Live Probe workflow:

Home -> Action Map -> Src Refresh -> Src Audit -> XP Drill -> XP Timeline -> XP Arch -> XP Lab -> Coach -> Rx Score -> Rx Bootstrap -> Rx Setup -> Transcript -> Route/Kit -> Local -> Screenshot -> P1 Trial -> Events/Problems -> Acceptance/Readiness

Open `XP Drill` after `Src Refresh`, `XP Timeline`, and `Iter Radar`, before changing route, package dependencies, hardware claims, or demo wording.

Export creates:

```text
evidence/<run_id>_<stage>_xp_iteration_drill.md
```

## Row Meaning

Each row shows:

- `Signal`: public XP/source signal being translated.
- `Stage`: where the drill belongs.
- `Current gap`: route, doctor, JSONL, metrics, failure category, and real_ios_verified state.
- `Validation drill`: what the operator/dev should run next.
- `Required evidence`: the exact artifacts needed before a claim can move.
- `Failure category`: the category to use in JSONL/problem triage.
- `Stop rule`: when to stop and avoid promotion wording.
- `GUI action`: the next panel opened by `Run Selected`.

## Boundary

`XP Drill` is a validation checklist. It does not browse automatically, does not install packages, does not connect receiver/HID, does not write JSONL evidence, does not prove real iPhone response, and does not prove XP parity.

Real control claims still require same-run JSONL evidence, screenshot quality, visible click/swipe/text response on the physical iPhone, manual observation, Acceptance PASS, Readiness PASS, logs where relevant, and exact device/iOS coverage.

## Offline Smoke

1. Start the GUI.
2. Set `Stage` to `p1`.
3. Click `XP Drill`.
4. Confirm offline rows stay `pending`, `warn`, or `fail`.
5. Click `Export`.
6. Confirm the markdown says `Real iOS control verified: False` and includes the no-evidence/no-parity boundary.
7. Click `Pack` and confirm `XP Iteration Drill Board` appears as a recommended artifact, not as required field evidence.

## Field Use

Start from the first `fail`, `pending`, or `warn` row. Run its GUI action, create or attach the required evidence, then refresh `XP Drill`. Do not move to the next XP parity or scale claim until the current drill has evidence strong enough for the same run_id.

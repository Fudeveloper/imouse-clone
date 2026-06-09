# Receiver Route Bootstrap

`imouse.receiver_bootstrap` creates a route-decision draft for the receiver/capture lane. It is useful when the default UxPlay route is blocked and the field team wants to test a Windows Receiver, wired projection, or capture-card route first.

It is not a P1 pass. It only fills the receiver fields enough for provider preflight and Doctor routing. HID, iPhone, bench ledger, screenshot quality, manual observation, Acceptance, and Readiness still decide whether P1 can run or pass.

## Command

```powershell
.\.venv\Scripts\python -m imouse.receiver_bootstrap `
  --run-id p1_dev1_YYYYMMDD `
  --route windows_receiver `
  --receiver-path "C:\Program Files\ReceiverX\receiverx.exe" `
  --receiver-name ReceiverX `
  --version 1.2.3 `
  --airplay-name imouse-dev-01 `
  --window-title imouse-dev-01 `
  --window-process receiverx.exe `
  --output evidence\p1_dev1_YYYYMMDD_route_decision.json `
  --markdown evidence\p1_dev1_YYYYMMDD_receiver_bootstrap.md
```

Then run:

```powershell
.\.venv\Scripts\python -m imouse.doctor --route-decision evidence\p1_dev1_YYYYMMDD_route_decision.json --markdown evidence\p1_dev1_YYYYMMDD_doctor.md
```

If the receiver path and required receiver fields are real, Doctor can downgrade missing `uxplay` from hard `fail` to route-specific `warn`. That only means the selected route does not need UxPlay; it does not prove frames are capturable.

## GUI Path

```text
Rx Score -> Rx Bootstrap -> Rx Setup -> Doctor -> Receiver -> Shot Bench -> P1 Trial -> Acceptance -> Readiness
```

Use `Rx Bootstrap` when:

- `uxplay` is missing on the Windows machine;
- a commercial Windows Receiver, wired projection tool, or capture-card app is installed;
- the operator can provide real path, receiver name, version, AirPlay/display name, capture method, and window title/process.

## Stop Rules

- Stop if `receiver.path` does not exist.
- Stop if the route-decision JSON still contains receiver placeholders.
- Stop before HID actions if screenshots are black, stale, wrong-window, cropped, or not tied to the selected iPhone.
- Stop any iOS perfect-control, broad-compatibility, or XP-parity wording until same-run JSONL evidence, screenshot quality, manual observations, Acceptance PASS, and Readiness PASS agree.

## What It Proves

| It can prove | It cannot prove |
|---|---|
| Receiver route fields are concrete enough for provider preflight | The receiver is showing the real iPhone |
| The selected route can avoid default UxPlay hard fail | Screenshot quality or frame freshness |
| The route-decision file is ready for Doctor routing | Click, swipe, text input, HID response, or XP hardware parity |

Use this as a bridge from receiver selection to real P1 evidence, not as evidence itself.

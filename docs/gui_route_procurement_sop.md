# GUI Route Procurement SOP

`Procure` is the Live Probe board for route choice, supplier questions, buying stop lines, and lab SOP. It sits between `Snapshot` and `Routes` so public XP and industry signals become concrete procurement checks before hardware, receiver software, SDKs, or device batches are purchased.

Use it before:

- buying receiver, HID, XP comparison hardware, Hub, cable, or extra iPhones;
- switching from UxPlay to Windows receiver, wired projection, or capture card lanes;
- installing SDK/package candidates on a field machine;
- wording any XP parity, broad iOS compatibility, perfect-control, or group-scale claim.

## Operator Path

```text
Home -> Snapshot -> Procure -> Routes -> Rx Score -> Rx Bootstrap -> Rx Setup -> XP Lab -> Kit Gate -> iOS SOP -> Start Pack -> Wizard -> Runner -> Ctrl Ledger -> P1 Trial -> Acceptance/Readiness
```

## Follow-Along Test

1. Start the GUI with `python -m imouse.gui`.
2. Set `Evidence`, `Stage`, and the selected device list.
3. Click `Snapshot`, then click `Procure`.
4. Select the first `fail`, `pending`, or `warn` row and click `Run Selected`.
5. Fill Route Decision, receiver, HID, iPhone, Hub, cable, operator, and evidence fields with real bench values.
6. Export `evidence/<run_id>_<stage>_route_procurement_sop.md`.
7. Continue through `Routes`, `Rx Score`, `XP Lab`, `Kit Gate`, `iOS SOP`, `Start Pack`, `Runner`, `P1 Trial`, `Acceptance`, and `Readiness`.

## What The Board Checks

- Mainstream route lock: one receiver lane, one HID lane, one iPhone scope, and no auxiliary-only route counted as XP-style control.
- Receiver procurement: version, path, AirPlay/window identity, capture method, screenshot quality, logs, licensing, and reconnect behavior.
- HID procurement: chipset/provider, firmware, serial/API protocol, baudrate, Hub/cable binding, manual click/swipe/type behavior, and release timing.
- XP parity purchase: legal XP hardware, firmware, authorization, side-by-side artifacts, wired/auto-binding evidence, and parity stop rules.
- iPhone fixture matrix: exact model, iOS version, settings profile, orientation, baseline screenshot, and local compatibility evidence.
- Bench materials: Hub, port, cable, power, receiver PC, network, operator, logs, replacement policy, and recovery notes.
- Source/package hygiene: source refresh, package identity, hashes, license, docs drift, and install boundaries.
- Claim/spend stop line: same-run evidence, Acceptance, Readiness, metrics, logs, and exact device/iOS scope before scale spend.

## Boundaries

- `Procure` does not write JSONL evidence, buy hardware, install packages, browse automatically, or prove real iPhone response.
- A `ready` procurement row only means the lane is reviewable for the current run; it is not a control claim.
- XP hardware parity still requires legal side-by-side XP hardware artifacts even when generic HID P1 works.
- Public source and vendor claims are test inputs. Local claims require same-run screenshot quality, manual real-iPhone click/swipe/text observation, Acceptance PASS, Readiness PASS, logs, and exact device/iOS scope.

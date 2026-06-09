# iMouse XP Architecture Map

This document is the architecture-level decomposition of the iMouse XP benchmark. It is based on public signals from:

- https://www.imouse.cc/
- https://www.imouse.cc/python-xp/
- https://www.imouse.cc/XP%E7%89%88API%E6%96%87%E6%A1%A3/
- https://www.imouse.cc/XP%E7%89%88%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3/

It is not evidence that our prototype controls a real iPhone. It is a design and verification map.

## Inferred XP Stack

| Layer | Inferred implementation principle | Local prototype surface | Proof gate |
|---|---|---|---|
| Product boundary | No iPhone app and no jailbreak; black-box iPhone control through projection plus hardware input. | Sources, Industry, Routes, Core, XP Gap, Goals. | Same-run receiver, HID, screenshot, manual observation, Acceptance, Readiness. |
| Hardware and USB/HID | Dedicated virtual mouse/keyboard hardware is the input authority. | CH9329/general HID prototype, Hardware Bench, Control Bench, P1 Trial. | HID identity, firmware, Hub/cable, click/swipe/type Manual pass; XP parity needs side-by-side XP hardware. |
| Projection and receiver | AirPlay/projection receiver must be stable, bindable, capturable, and observable. | UxPlay/Windows/wired/capture-card routes, Rx Score, Rx Bootstrap, Rx Setup, Receiver Gate, Shot Bench. | Route metadata, Doctor/provider check, non-black fresh screenshots, window/device binding, logs. |
| Capture, vision, OCR | Automation reads current screenshots, image/color/OCR regions, and replayable artifacts. | Screenshot API, GUI preview, Template Asset Index, find-image/color/OCR, Scenario Library. | Saved screenshot artifacts, regions, thresholds, real recognition events, replayable failures. |
| Kernel/API service | Console, scripts, GUI, and helpers cross the same local service contract. | FastAPI XP-compatible service, `/api + fun`, WebSocket, XpApiClient, Events. | API/client/WebSocket tests plus field errors that preserve receiver/HID/capture truth. |
| Python helper/script runtime | SDK shape is an integration contract, not hardware proof. | XpApiClient, JSON runner, dry-run guard, batch helpers, metrics/artifacts. | Pinned helper behavior, local tests, then real-run JSONL using the same helpers. |
| Console/GUI operator layer | GUI is an operator console and SOP surface, not a proof generator. | Tkinter GUI, Live Probe, Home, Verify, Local, Coach, Transcript, Pack. | A second operator can reproduce the run from exported artifacts and the same run_id. |
| Evidence and readiness | Claims are derived from append-only evidence and stage gates. | JSONL evidence, Acceptance, Readiness, Timeline, Matrix, Triage, Recovery. | Component metadata, screenshot quality, Manual observation, no unexplained fails, Acceptance PASS, Readiness PASS. |
| Group control and ops | Scale only after single-device proof; failures stay per-device and explainable. | Groups, Matrix, Stage Dashboard, metrics, callback/log ingestion, P2/P3/P4 runbooks. | P2 stability, P3 pilot_4, P4 stable_10, per-device artifacts, metrics, logs, recovery notes. |

## GUI Entry

In the Python GUI, click:

```text
Live Probe -> XP Arch
```

Export creates:

```text
evidence/<run_id>_<stage>_xp_architecture.md
```

Use `XP Arch` before `Core`, `Roadmap`, and `XP Gap` reviews.

## Status Interpretation

- `ready` on API/SDK or GUI layers means local structure is usable for the current stage.
- `ready` does not mean receiver, HID, iPhone, XP hardware, wired projection, or hard decode is proven.
- `fail` on hardware/evidence layers is expected until real iPhone JSONL evidence exists.
- `pass` is only valid for the exact stage and run_id whose evidence supports it.

## R&D Guidance

1. Keep WDA/Appium/MDM/Shortcuts outside the XP-style main claim.
2. Treat receiver/capture and HID as separate product lanes with separate evidence.
3. Treat XP dedicated hardware, 4.4 firmware, wired projection, auto-binding, and hardware decode as side-by-side parity lanes.
4. Make every GUI shortcut go through evidence-aware service paths.
5. Do not scale beyond one iPhone until receiver, screenshot, HID, calibration, manual observation, Acceptance, and Readiness close for P1.

## Claim Boundary

Do not claim iOS perfect control, broad compatibility, or XP parity from this document. Those claims require same-run field evidence, exact device/iOS coverage, Acceptance, Readiness, and no unexplained failures.

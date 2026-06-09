# XP Public Source Action Map

Last checked: 2026-06-09 Asia/Shanghai.

This document turns public iMouse XP and industry signals into R&D actions, SOP gates, and GUI ownership. It is source intelligence only. It does not write JSONL evidence, does not prove real iPhone control, and does not prove XP parity.

## Current Position

The iMouse XP benchmark is still a black-box iOS control product shape:

```text
iPhone zero-install and non-jailbreak
-> AirPlay or wired projection receiver
-> screenshot/capture pipeline
-> image/OCR recognition
-> USB HID mouse/keyboard injection
-> local Kernel/Core API
-> Console, SDK, scripts, GUI
-> evidence, Acceptance, Readiness, SOP review
```

WDA, Appium, XCUITest, MDM, Apple Configurator, and Shortcuts remain useful auxiliary lanes, but they do not replace the XP-style receiver plus HID mainline when the product goal is cross-app, system-level, pixel-driven group control without an iPhone-side app.

## Action Map

| Public Signal | Source | R&D Decision | SOP Gate | Stop Rule | GUI Owner |
|---|---|---|---|---|---|
| iMouse publicly describes dedicated virtual mouse/keyboard hardware, AirPlay mirroring, no iPhone app, Kernel/Core service, Console, HTTP/WebSocket API, OpenCV image matching, and OCR. | `https://www.imouse.cc/` | Keep receiver/capture, HID, vision, API, and evidence as separate lanes. Do not pivot the mainline to WDA/Appium. | P1 must prove one real iPhone can be seen, clicked, swiped, typed into, and manually observed. | Stop all "perfect iOS control" language until screenshot, HID response, manual observation, Acceptance, and Readiness pass in the same run. | `Home -> Route/Kit -> Local -> Screenshot -> P1 Trial -> Acceptance/Readiness` |
| The homepage advertises broad iPhone/iOS compatibility, including current high-end model and iOS generation claims. | `https://www.imouse.cc/` | Treat compatibility claims as a test-matrix input only. Build our own model/iOS coverage table. | Every claimed model plus iOS pair needs local evidence. | Stop broad compatibility claims when the exact model/iOS/orientation tuple is missing from evidence. | `Compat`, `Bench`, `Goals` |
| Python XP material says the client is XP-only and needs dedicated iMouse hardware. | `https://www.imouse.cc/python-xp/` and `https://pypi.org/project/imouse-py/` | Use the SDK shape to design client helpers, but do not treat install/import success as hardware proof. | Before SDK parity claims, pin package version/hash and pass API tests plus real receiver/HID/iPhone evidence for used domains. | Stop SDK parity claims if helper calls pass locally but no hardware-backed action is observed on iPhone. | `Sources`, `Events`, `XP Gap`, `Core` |
| Public Python helper domains include console-level device, AirPlay, USB, group, config, user and device-level image, keyboard, mouse, shortcut, events, and logging. | `https://www.imouse.cc/python-xp/` | Backlog must be domain-based, not button-based. Implement helpers only when their evidence gate is known. | XP Gap rows must show implemented, tested, and evidence-backed status for the current stage. | Stop "core function complete" if config/user/group/callback/log gaps are hidden behind click/screenshot demos. | `Core`, `XP Gap`, `Events`, `Roadmap` |
| XP API uses local port `9911`, `/api`, HTTP/WebSocket, `msgid`, `status/message/data`, and device execution codes. | `https://www.imouse.cc/XP%E7%89%88API%E6%96%87%E6%A1%A3/` | Keep `/api + fun` compatibility, WebSocket echo behavior, and structured error taxonomy. | API tests must cover success, device not found, hardware not bound, capture fail, timeout, and callback/log paths. | Stop integration if HTTP 200 hides device, capture, HID, or callback failure. | `Events`, `Attach Log`, `XP Gap`, `Verify` |
| XP new-version material emphasizes Windows service split, Console/Core restart, wired projection, 4.4 firmware, auto binding, fast projection, hardware decode, logs, cloud groups, subaccounts, LAN visibility, and custom shortcuts. | XP help mirrors and official help pages | Plan service/process/log/recovery work after P1, instead of adding more decorative GUI. | P2/P3 must collect metrics, logs, restart notes, receiver/HID recovery records, and per-device failure isolation. | Stop P3/P4 promotion if one device failure cannot be isolated to receiver, capture, HID, calibration, vision, script, or ops. | `Recovery`, `Rerun`, `Dashboard`, `Matrix`, `Roadmap` |
| Apple supports pointer devices through AssistiveTouch and exposes pointer style, tracking speed, button assignment, Mouse Keys, and onscreen keyboard settings. | `https://support.apple.com/en-us/111775` | iOS setup is a product lane, not a note. Record AssistiveTouch, pointer speed, mouse profile, keyboard behavior, lock/rotation state, and baseline screenshots. | P1 cannot start until iOS SOP fields are filled and a baseline screenshot proves the intended phone state. | Stop HID testing when the iPhone settings profile is unknown or not tied to evidence. | `iOS SOP`, `Kit Gate`, `P1 Trial`, `Control Bench` |
| Apple AirPlay screen mirroring is a user-level screen output path, not a receiver implementation guarantee. | Apple AirPlay support docs plus local receiver tests | Receiver selection must be tested locally: UxPlay, Windows receiver, wired projection, or capture-card fallback. | Doctor must pass receiver checks and screenshot quality must be nonblank and repeatable before HID control tests. | Stop real-run control when capture is black, stale, wrong-window, cropped, or not tied to one device id. | `Receiver`, `Shot Bench`, `Local`, `Doctor` |
| PyPI also contains `imouse-xp 0.0.7` and `py-imouse-xp 1.0.1`, separate from `imouse-py 0.0.4`. | `https://pypi.org/project/imouse-xp/`, `https://pypi.org/project/py-imouse-xp/`, `https://pypi.org/project/imouse-py/` | Treat package names as drift and supply-chain signals. Review namespace, maintainer, source, hashes, API shape, and license before using any package. | Package adoption needs a frozen version, hash, source review, local API regression tests, and hardware-backed smoke evidence. | Stop dependency adoption if package identity, source, or API shape is unclear. Do not install packages on field machines without a pinned artifact. | `Sources`, `XP Gap`, `Local`, `Verify` |
| XP value moves from single command success to group operation, logging, recovery, account/permission, and repeatable SOP. | iMouse public docs, XP help mirrors, and local SOP docs | Make P1/P2/P3/P4 stage gates explicit. Productization comes after evidence, not before it. | P3 requires 4-device per-device evidence and failure isolation. P4 requires longer stability metrics and recovery logs. | Stop group-control claims when one-device evidence is being extrapolated to multiple devices. | `Dashboard`, `Matrix`, `SOP`, `Pack`, `Goals` |
| Public API/source docs can be stale or promotional. | All public sources | Keep source claims in ledgers, and keep acceptance claims in JSONL evidence. | Every public claim must map to route fields, tests, artifacts, and stop rules before it can affect scope. | Stop R&D decisions when source-only claims have no local validation path. | `Sources`, `Operator Home`, `Goal Gate` |

## Field SOP Conversion

Before a P1 real-device run:

1. Open `Home` and confirm the operator workflow starts at Route/Kit, not at "run everything".
2. Open `Sources` and confirm every public signal has a verification gap or an evidence-backed status.
3. Open `Kit Gate` and fill receiver, HID, iPhone, hub, cable, network, and backup hardware fields.
4. Open `iOS SOP` and record AssistiveTouch, pointer speed, keyboard behavior, rotation lock, screen lock policy, QR scan policy, and baseline screenshot expectations.
5. Open `Receiver` and `Shot Bench`; do not test HID until screenshots are current, nonblank, and tied to the right device.
6. Open `P1 Trial`; click, swipe, and type only after route and doctor pass.
7. Record manual observations after every HID action. API success without visible iPhone response is a failure category.
8. Run `Acceptance` and `Readiness`; only those gates can move the run toward P2.

## Package Registry Boundary

Package registry data is useful for API drift and namespace risk:

| Package | Public Signal | R&D Use | Boundary |
|---|---|---|---|
| `imouse-py` | Public version signal `0.0.4`, released 2025-11-16; XP-only hardware-backed positioning. | Primary SDK-shape reference. | Import/install does not prove hardware, receiver, HID, or iPhone response. |
| `imouse-xp` | Public version signal `0.0.7`, released 2025-08-10. | Compare package namespace and API shape if source review is needed. | Not a proof source unless pinned, reviewed, tested, and hardware-backed. |
| `py-imouse-xp` | Public version signal `1.0.1`, released 2025-09-05; client library positioning with HTTP/WebSocket-style control language. | Watch for naming/API drift and dependency confusion risk. | Treat as third-party until source, maintainer, hashes, and behavior are reviewed. |

## R&D Priority

1. P1 proof: one real iPhone, one receiver route, one HID route, screenshot, click, swipe, text input, manual observation, Acceptance, Readiness.
2. XP comparison hardware: buy or borrow one XP hardware set; record model, firmware, authorization, binding flow, mouse profile, and logs.
3. Receiver/capture bench: compare UxPlay, Windows receiver, wired projection, and capture-card fallback by screenshot stability and device binding.
4. HID bench: compare CH9329, XP hardware, and future self-developed HID by release behavior, coordinate error, input method behavior, and recovery.
5. Observability: preserve request/response, callback, receiver, HID, capture, screenshot, and manual observation artifacts by device id.
6. P3/P4 group control: scale only after P1/P2 evidence is repeatable; every failure must isolate device plus component.

## Non-Evidence Boundary

This map is a required planning asset. It can block readiness if missing, but it cannot pass readiness by itself. The only valid proof path for real iOS control is a real-device run with JSONL evidence, artifacts, manual observation, Acceptance, and Readiness.

## Source Links

- https://www.imouse.cc/
- https://www.imouse.cc/python-xp/
- https://www.imouse.cc/XP%E7%89%88API%E6%96%87%E6%A1%A3/
- https://pypi.org/project/imouse-py/
- https://pypi.org/project/imouse-xp/
- https://pypi.org/project/py-imouse-xp/
- https://support.apple.com/en-us/111775
- https://support.apple.com/en-us/102661

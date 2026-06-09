# GUI XP API Coverage Board

Updated: 2026-06-09

The GUI `API Cov` board maps iMouse XP-style API and Python helper domains to local implementation, local tests, runtime gates, field evidence and claim boundaries.

It is an operator and R&D planning surface. It does not record JSONL evidence, does not prove real iPhone response, and does not prove XP dedicated-hardware parity.

## What It Covers

The board separates these lanes:

- API envelope and transport: local 9911 `/api`, HTTP/WebSocket, `fun`, `msgid`, `status`, `message`, `data`, `data.code`.
- Device registry and profile: device list/register/remove, profile and metadata helpers.
- AirPlay/receiver/capture: projection startup, capture startup and screenshot freshness gates.
- USB/HID binding: hardware scan, bind/unbind, HID identity and physical route proof.
- Mouse click/swipe: click and swipe API coverage plus lane-separated Manual evidence.
- Keyboard text/key input: text/key/combo API coverage plus visible physical iPhone input.
- Picture/image/color: screenshot, image and color matching tied to replayable artifacts.
- OCR/find text: OCR and text matching tied to cropped real screenshots and false-positive review.
- Group and batch control: local group/batch API coverage versus P3/P4 per-device proof.
- Config/user/shortcut: local runtime scaffolding only.
- Callback/event channel: diagnostic callback rows, not control proof.
- Logs and failure triage: receiver/HID/script logs tied to failure categories and rerun decisions.
- Cloud/LAN/account ops: backlog only until core control and group evidence are stable.

## Status Semantics

- `p0_api_covered`: local compatibility can be reviewed from tests and source, but it closes only P0 API shape.
- `local_api_covered`: local fun/helper routes exist, but field proof may still be missing.
- `field_blocked`: a receiver, HID, screenshot or manual real-iPhone gate is still open.
- `lane_manual_required`: click, swipe or text still needs its own Manual observation lane.
- `scaffolding_only`: local state exists only to keep compatibility shape visible.
- `backlog_only`: product scope exists as roadmap/backlog, not implementation or proof.

## Operator SOP

1. Open `API Cov` from Live Probe, Home, Core or Events.
2. Start from the first `fail`, `pending` or `warn` row.
3. Use `Run Selected` to jump to the owning GUI panel.
4. Export the board into `evidence/<run_id>_<stage>_xp_api_coverage.md`.
5. Keep local API tests separate from field evidence in review notes.

## Claim Boundary

Local API or SDK helper success is not real iOS control. Receiver, HID, mouse, keyboard, screenshot, vision and group rows need same-run JSONL evidence, saved artifacts, lane-separated Manual observations, Acceptance PASS and Readiness PASS before any control claim. Config/user/shortcut and cloud/account rows require separate product validation after core control is proven.

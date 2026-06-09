# GUI Field Evidence Runner

`Runner` is the live field checklist for one `run_id`. Use it after `Wizard` is built and before any P1 claim.

It checks the same-run path for:

| Gate | What it proves | Stop line |
|---|---|---|
| Run scope | Selected devices and evidence path are known. | Stop if the physical iPhone, HID, receiver, Hub port, cable, or run_id cannot be traced. |
| Route decision | Receiver, capture, HID, iPhone, iOS, bench, and blockers are recorded. | Stop if validation fails or placeholders remain. |
| Route-aware Doctor | Local dependencies and the selected receiver route are preflighted. | Stop on any Doctor fail; warn needs an operator note. |
| Screenshot quality | A current, usable frame is captured from the target iPhone. | Stop if the frame is black, stale, cropped, wrong-window, or wrong-orientation. |
| HID click/swipe/text | Each control lane has its own Manual pass/fail observation. | Stop if API success is not matched by visible real-iPhone behavior. |
| Acceptance and Readiness | The JSONL evidence passes machine gates for the same run_id. | Stop if command output differs from GUI state. |

Runner exports `evidence/<run_id>_<stage>_field_runner.md` with copy-ready PowerShell commands:

```powershell
.\.venv\Scripts\python -m imouse.route_decision validate evidence\<run_id>_route_decision.json --require-ready --markdown evidence\<run_id>_<stage>_route_decision.md --record-evidence evidence\<run_id>.jsonl
.\.venv\Scripts\python -m imouse.doctor --route-decision evidence\<run_id>_route_decision.json --markdown evidence\<run_id>_<stage>_doctor.md
.\.venv\Scripts\python -m imouse.acceptance evidence\<run_id>.jsonl --gate <stage> --markdown evidence\<run_id>_<stage>_acceptance.md
.\.venv\Scripts\python -m imouse.acceptance evidence\<run_id>.jsonl --gate <stage> --gap-markdown evidence\<run_id>_<stage>_gap.md
.\.venv\Scripts\python -m imouse.readiness --target <stage> --evidence evidence\<run_id>.jsonl --markdown evidence\<run_id>_readiness.md
```

Runner is not evidence by itself. Real iOS control still requires JSONL events, screenshot artifacts, separate Manual observations for click/swipe/text, Acceptance PASS, Readiness PASS, and the exact device/iOS scope.

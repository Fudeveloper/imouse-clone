# GUI P1 Field Transcript

`Transcript` is the fillable field log for the first real-iPhone P1 run. It turns `Coach`, `Rx Bootstrap`, and `Rx Setup` state into one operator transcript with observation prompts, expected results, failure categories, artifact paths, rerun rules, and stop rules.

It is not JSONL evidence. It does not record Manual pass by itself and does not prove real iPhone control.

## GUI Path

Use the Live Probe workflow:

```text
Home -> Action Map -> Src Refresh -> Src Audit -> XP Drill -> XP Timeline -> XP Arch -> XP Lab -> Coach -> Rx Score -> Rx Bootstrap -> Rx Setup -> Transcript -> Route/Kit -> Local -> Screenshot -> P1 Trial -> Events/Problems -> Acceptance/Readiness
```

Open `Transcript` after `Src Refresh`, `Coach`, `Rx Score`, any needed `Rx Bootstrap`, and `Rx Setup`, then export it before the first real HID action. Keep it open or printed while the operator watches the physical iPhone.

The dialog also has `Prefill Manual`, `Record Pass`, and `Record Fail` helpers. They copy the selected transcript row into the bottom Manual controls. `Record Pass` is intentionally limited to click, swipe, and keyboard-input checkpoints; setup or route rows are prefilled as `info` so they cannot accidentally satisfy the Manual control gate.

## What The Operator Fills

Each row includes:

- checkpoint and current status;
- what to observe on the physical iPhone;
- expected result;
- likely failure categories;
- artifact/log path to attach;
- operator fill-in slot;
- rerun rule;
- stop rule;
- GUI action for the next probe.

The operator should write what the physical iPhone did, not only what the API returned.

## Required Field Discipline

- A pass row must mention the visible iPhone response.
- A fail row must include one failure category and one artifact/log path.
- Screenshot rows must name whether the frame was current, nonblank, correct-window, correct-device, and correct-orientation.
- Click/swipe/type rows must mention visible response, focus, pointer behavior, release behavior, and text result.
- Any route, receiver, HID, cable, Hub port, iPhone, selected device, or iOS-settings change after failed evidence requires a fresh run_id.
- Use `P1 Trial` or the Manual control to write real Manual observations into JSONL.
- Use `Prefill Manual` when the operator wants to edit the note before recording.
- Use `Record Pass` only after the physical iPhone visibly responded to click, swipe, or keyboard input.
- Use `Record Fail` for any row that needs a categorized failure and artifact/log path.

## Export

`Export` writes:

```text
evidence/<run_id>_<stage>_p1_field_transcript.md
```

This export is a field transcript and handoff aid. It supports review, but Acceptance and Readiness still decide the claim boundary.

## Pass Boundary

The transcript can only support a P1 claim when the same run_id has:

- Route Decision ready;
- alternate receiver bootstrap documented when the run does not use UxPlay;
- receiver setup lane documented;
- Doctor without fail;
- screenshot quality evidence;
- Manual click, swipe, and text observations in JSONL;
- no unexplained fail events;
- Acceptance PASS;
- Readiness PASS with `real_ios_control_verified=true`.

Without those, the transcript should point to the first missing or failed row, not promote the run.

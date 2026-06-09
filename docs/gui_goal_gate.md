# GUI Goal Gate

`Goals` is the GUI acceptance board for the four user goals:

1. iOS perfect control.
2. iOS group-control SOP and issue log.
3. iMouse XP core functions and docs.
4. XP iteration lessons and pitfalls.

It exports:

```text
evidence/<run_id>_<stage>_gui_goal_gate.md
```

## Closure Inputs

Goal Gate reads the current evidence state and the surrounding GUI boards:

| Input | Why it matters |
|---|---|
| Acceptance and Readiness | Stage gate results and `real_ios_control_verified`. |
| Proof Map | Exact evidence rows still blocking iOS control claims. |
| Claim Scope | Allowed and forbidden demo/handoff wording. |
| Evidence Pack | Required and recommended artifacts for the same `run_id`. |
| XP Gap Audit | XP core domains still blocked, partial, or unstarted. |
| SOP artifacts | Runbook, worksheet, SOP board, issue triage, rerun, recovery, matrix, and gap report. |

## Operator Rule

Use `Goals` near the end of a field session, after `Proof Map` and `Claim Scope`, and before any completion summary.

The iOS control row cannot pass unless the same run has real-device evidence, Proof Map closure, Claim Scope pass wording, Acceptance PASS, Readiness PASS, and no unexplained fail events.

Goal Gate is an acceptance map, not evidence. It does not write JSONL evidence and does not prove real iPhone response by itself.

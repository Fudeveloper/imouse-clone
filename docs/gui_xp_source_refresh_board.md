# GUI XP Source Refresh Board

`Src Refresh` is the public-source refresh SOP board in the Python GUI. It helps the team decide when public iMouse XP, package registry, Apple/iOS, and industry-route signals must be refreshed before route, roadmap, dependency, compatibility, or demo claims.

Use the Live Probe workflow:

```text
Home -> Action Map -> Src Refresh -> Src Audit -> Pkg Guard -> XP Drill -> XP Timeline -> XP Arch -> XP Lab -> Coach -> Rx Score -> Rx Bootstrap -> Rx Setup -> Transcript -> Route/Kit -> Local -> Screenshot -> P1 Trial -> Events/Problems -> Acceptance/Readiness
```

Open `Src Refresh` after `Action Map` and before changing hardware scope, adopting a Python package, updating iOS compatibility wording, or presenting XP-parity progress.

## Rows

- `official_homepage_refresh`: recheck homepage product model, compatibility wording, no-app/no-jailbreak positioning, hardware, and API claims.
- `official_api_refresh`: recheck XP API envelope, `/api`, `fun`, `msgid`, WebSocket, callbacks, and error shape.
- `official_help_iteration_refresh`: recheck help/new-version lessons such as Windows 10+, Core/Console split, 4.4 firmware, wired projection, hard decode, logs, cloud/groups, subaccounts, LAN rules, and shortcuts.
- `package_registry_refresh`: recheck `imouse-py`, `imouse-xp`, and `py-imouse-xp` before any package install or SDK comparison.
- `apple_ios_pointer_refresh`: recheck iOS pointer/AssistiveTouch/mouse/keyboard setup before adding a model/iOS compatibility claim.
- `industry_route_refresh`: recheck mainstream receiver/capture/HID route choices before procurement or route switching.
- `source_to_sop_commit`: map every source delta to a GUI owner, test, artifact, or explicit reject.
- `source_claim_boundary_refresh`: downgrade any source-only claim that lacks JSONL field evidence, Acceptance, and Readiness.

## SOP

1. Click `Src Refresh`.
2. Start from the first `fail`, `pending`, or `warn` row.
3. Open the listed source manually in a browser and compare it with the local doc.
4. If wording, version, API shape, help-page behavior, package metadata, or iOS guidance changed, update the local doc and tests/SOP rows affected by that change.
5. Click `Run Selected` to land the source delta in Sources, Action Map, XP Timeline, Iter Radar, Events, Local, iOS SOP, Rx Score, or Goals.
6. Click `Src Audit`; keep the offline report when no network is available, or click `Run Live` to fetch URL/PyPI status.
7. Click `Pkg Guard` before any dependency adoption or SDK-parity wording.
8. Export `Src Refresh`, `Src Audit`, `Pkg Guard`, `Sources`, `Action Map`, `XP Timeline`, `Iter Radar`, and `Pack` for the run handoff.
9. Rerun Acceptance and Readiness only after real-device evidence exists.

## Package Namespace Guard

`package_registry_refresh` must treat `imouse-py`, `imouse-xp`, and `py-imouse-xp` as separate namespaces. Similar package names are dependency-confusion and SDK-drift signals, not interchangeable install targets.

Do not install lookalike packages on field machines until the exact version and hashes are pinned, source/maintainer/license/API behavior are reviewed, local API regression tests pass, and the exact receiver/HID/iPhone scope has hardware-backed evidence.

## Boundary

- `Src Refresh` does not browse automatically.
- `Src Refresh` does not write JSONL evidence.
- `Src Audit` can fetch public URLs, but it still records source freshness only.
- A fresh public source does not prove real iPhone response.
- A fresh package version does not prove SDK parity or hardware control.
- A fresh iOS/Apple support page does not prove local compatibility.
- XP parity still requires local API behavior, receiver/capture proof, HID proof, SOP coverage, side-by-side hardware evidence where claimed, Acceptance, and Readiness.

Export path:

```text
evidence/<run_id>_<stage>_xp_source_refresh.md
```

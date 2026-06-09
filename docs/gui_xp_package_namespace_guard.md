# GUI XP Package Namespace Guard

`Pkg Guard` is the GUI supply-chain and SDK-drift board for iMouse XP package names. It is paired with `Src Refresh` and `Src Audit`, but it keeps package adoption separate from real-device evidence.

## Scope

The board tracks three PyPI namespaces as separate package identities:

| Package | Public source | GUI meaning |
|---|---|---|
| `imouse-py` | `https://pypi.org/project/imouse-py/` | Primary SDK-shape clue because the public Python XP material points to `pip install imouse-py`. |
| `imouse-xp` | `https://pypi.org/project/imouse-xp/` | Similar-name namespace; review as dependency-confusion risk. |
| `py-imouse-xp` | `https://pypi.org/project/py-imouse-xp/` | Similar-name namespace; review as SDK-drift and third-party risk. |

## GUI Workflow

1. Open `Pkg Guard` from the main toolbar, `Src Refresh`, or `Src Audit`.
2. Keep `Run Offline` as the default in a field environment when network access is unstable.
3. Click `Run Live` only when the operator is allowed to fetch public PyPI/source metadata.
4. Export `evidence/<run_id>_<stage>_xp_package_namespace_guard.md` before adopting a package, changing SDK docs, or making XP SDK parity wording.
5. Use `Src Audit` to keep the raw URL/PyPI report and `Action Map` to land accepted source deltas into tests, docs, SOP, or explicit rejection.

## Status Rules

- `fail`: the audit row is missing or the public source fetch/parse failed. Stop dependency adoption.
- `pending`: offline mode or intentionally skipped fetch. Treat it as a review task, not a pass.
- `warn`: the package source may be reachable, but adoption is still blocked until review and field proof are complete.

`ok` source metadata is deliberately downgraded to `warn` in `Pkg Guard` because package availability does not prove receiver, HID, iPhone response, XP hardware authorization, or broad compatibility.

## Adoption SOP

Before any package touches a field machine:

1. Pin exact package name, version, and hashes.
2. Review maintainer, source repository, license, release history, and API surface.
3. Compare helper domains against the local XP API/client tests.
4. Run local API regression tests in an isolated environment.
5. Require hardware-backed receiver/HID/iPhone evidence for the exact device/iOS/receiver/HID scope before using package behavior in parity wording.

## Boundary

`Pkg Guard` does not install packages, does not write JSONL evidence, does not prove screenshot freshness, does not prove real iPhone movement, does not prove XP hardware parity, and does not prove iOS compatibility. It is a package-risk SOP board.

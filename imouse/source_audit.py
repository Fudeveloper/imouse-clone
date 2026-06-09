"""Repeatable public-source audit for iMouse XP benchmarking.

This module records public source freshness and package metadata. It is
research support only: a green source audit never proves real iPhone control,
XP parity, or broad iOS compatibility.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable
from urllib import error, request


FetchResult = dict[str, Any]
Fetcher = Callable[[str, float], FetchResult]


@dataclass(frozen=True)
class SourceSpec:
    key: str
    url: str
    source_type: str
    local_doc: str
    expected_terms: tuple[str, ...]
    source_signal: str
    sop_owner: str
    claim_boundary: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


DEFAULT_SOURCE_SPECS: tuple[SourceSpec, ...] = (
    SourceSpec(
        key="imouse_homepage",
        url="https://www.imouse.cc/",
        source_type="html",
        local_doc="docs/industry_current_state_snapshot_2026.md",
        expected_terms=("AirPlay", "OpenCV", "OCR"),
        source_signal="Homepage product model, compatibility wording, hardware, API, and vision claims.",
        sop_owner="Snapshot, Sources, Action Map, Compat, Goals",
        claim_boundary="Homepage claims are test inputs only; local compatibility needs same-run evidence.",
    ),
    SourceSpec(
        key="python_xp",
        url="https://www.imouse.cc/python-xp/",
        source_type="html",
        local_doc="docs/xp_public_source_refresh.md",
        expected_terms=("XP", "Device", "Mouse"),
        source_signal="Python XP helper/package shape and XP-only hardware-backed positioning.",
        sop_owner="Sources, Events, XP Gap, Local",
        claim_boundary="SDK install/import does not prove receiver, HID, hardware authorization, or iPhone response.",
    ),
    SourceSpec(
        key="xp_api",
        url="https://www.imouse.cc/XP%E7%89%88API%E6%96%87%E6%A1%A3/",
        source_type="html",
        local_doc="docs/xp_api_compat.md",
        expected_terms=("9911", "api", "msgid"),
        source_signal="XP HTTP/WebSocket API envelope, msgid, fun domains, callbacks, and errors.",
        sop_owner="Events, Attach Log, XP Gap, API tests",
        claim_boundary="API compatibility does not prove screenshot freshness or physical iPhone control.",
    ),
    SourceSpec(
        key="some3c_xp_new_version",
        url="https://doc.some3c.com/iphone-farm-setup/imouse-xp-new-version",
        source_type="html",
        local_doc="docs/imouse_xp_iteration_lessons.md",
        expected_terms=("Windows", "Console", "Kernel"),
        source_signal="Third-party XP setup lessons around service split, Windows route, operations, and recovery.",
        sop_owner="XP Timeline, Iter Radar, Recovery, Roadmap",
        claim_boundary="Third-party setup notes shape SOP only; they are not XP parity or hardware proof.",
    ),
    SourceSpec(
        key="some3c_iphone_settings",
        url="https://doc.some3c.com/iphone-farm-setup/iphone-farm-settings",
        source_type="html",
        local_doc="docs/ios_field_settings_sop.md",
        expected_terms=("AssistiveTouch", "Keyboard", "Mouse"),
        source_signal="iPhone settings, pointer, keyboard, lock/brightness, network, receiver, and hardware setup.",
        sop_owner="iOS SOP, Kit Gate, Transcript, Control Bench",
        claim_boundary="Settings readiness only opens testing; it does not prove click/swipe/text response.",
    ),
    SourceSpec(
        key="pypi_imouse_py",
        url="https://pypi.org/pypi/imouse-py/json",
        source_type="pypi",
        local_doc="docs/xp_public_source_action_map.md",
        expected_terms=("imouse", "xp"),
        source_signal="Package version, summary, project URLs, and SDK drift signal for imouse-py.",
        sop_owner="Sources, Local, XP Gap, dependency review",
        claim_boundary="Package metadata is supply-chain intelligence, not hardware-backed control evidence.",
    ),
    SourceSpec(
        key="pypi_imouse_xp",
        url="https://pypi.org/pypi/imouse-xp/json",
        source_type="pypi",
        local_doc="docs/xp_public_source_action_map.md",
        expected_terms=("imouse",),
        source_signal="Similar package namespace used as dependency-confusion and drift signal.",
        sop_owner="Sources, Local, dependency review",
        claim_boundary="Do not adopt similar package names without pinning, hashes, source review, and field proof.",
    ),
    SourceSpec(
        key="pypi_py_imouse_xp",
        url="https://pypi.org/pypi/py-imouse-xp/json",
        source_type="pypi",
        local_doc="docs/xp_public_source_action_map.md",
        expected_terms=("imouse",),
        source_signal="Similar package namespace used as dependency-confusion and drift signal.",
        sop_owner="Sources, Local, dependency review",
        claim_boundary="Do not adopt similar package names without pinning, hashes, source review, and field proof.",
    ),
)


PACKAGE_NAMESPACE_KEYS: tuple[str, ...] = (
    "pypi_imouse_py",
    "pypi_imouse_xp",
    "pypi_py_imouse_xp",
)


def default_fetcher(url: str, timeout: float) -> FetchResult:
    headers = {
        "User-Agent": "imouse-clone-source-audit/1.0",
        "Accept": "application/json,text/html,application/xhtml+xml,text/plain;q=0.9,*/*;q=0.8",
    }
    req = request.Request(url, headers=headers)
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            charset = resp.headers.get_content_charset() or "utf-8"
            return {
                "ok": 200 <= int(resp.status) < 400,
                "status_code": int(resp.status),
                "body": body.decode(charset, errors="replace"),
                "content_type": resp.headers.get("content-type", ""),
                "error": "",
            }
    except error.HTTPError as exc:
        try:
            body = exc.read().decode("utf-8", errors="replace")
        except Exception:
            body = ""
        return {
            "ok": False,
            "status_code": int(exc.code),
            "body": body,
            "content_type": "",
            "error": str(exc),
        }
    except OSError as exc:
        return {
            "ok": False,
            "status_code": 0,
            "body": "",
            "content_type": "",
            "error": str(exc),
        }


def _doc_stamp(path: Path) -> str:
    try:
        if not path.exists():
            return "missing"
        return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).strftime("%Y-%m-%d")
    except OSError:
        return "unreadable"


def _term_hits(text: str, terms: Iterable[str]) -> tuple[list[str], list[str]]:
    lowered = text.lower()
    hits: list[str] = []
    missing: list[str] = []
    for term in terms:
        if term.lower() in lowered:
            hits.append(term)
        else:
            missing.append(term)
    return hits, missing


def _parse_pypi_payload(body: str) -> tuple[str, str, str]:
    payload = json.loads(body)
    info = payload.get("info") if isinstance(payload, dict) else {}
    if not isinstance(info, dict):
        return "", "", ""
    version = str(info.get("version", "") or "")
    summary = str(info.get("summary", "") or "")
    project_urls = info.get("project_urls", {})
    if isinstance(project_urls, dict):
        project_url_text = "; ".join(
            f"{key}={value}" for key, value in sorted(project_urls.items()) if value
        )
    else:
        project_url_text = ""
    return version, summary, project_url_text


def audit_source(
    spec: SourceSpec,
    *,
    root: str | Path = ".",
    timeout: float = 8.0,
    offline: bool = False,
    fetcher: Fetcher = default_fetcher,
) -> dict[str, Any]:
    doc_path = Path(root) / spec.local_doc
    base = {
        "key": spec.key,
        "url": spec.url,
        "source_type": spec.source_type,
        "local_doc": spec.local_doc,
        "doc_stamp": _doc_stamp(doc_path),
        "source_signal": spec.source_signal,
        "sop_owner": spec.sop_owner,
        "claim_boundary": spec.claim_boundary,
        "proves_real_ios_control": False,
        "proves_xp_parity": False,
        "expected_terms": list(spec.expected_terms),
        "matched_terms": [],
        "missing_terms": list(spec.expected_terms),
        "status_code": 0,
        "version": "",
        "summary": "",
        "project_urls": "",
    }
    if offline:
        return {
            **base,
            "status": "pending",
            "message": "offline mode; source was not fetched",
        }

    fetched = fetcher(spec.url, timeout)
    body = str(fetched.get("body", "") or "")
    status_code = int(fetched.get("status_code", 0) or 0)
    base["status_code"] = status_code
    if not fetched.get("ok"):
        return {
            **base,
            "status": "fail",
            "message": f"fetch failed: {fetched.get('error') or status_code or 'unknown error'}",
        }

    search_text = body
    if spec.source_type == "pypi":
        try:
            version, summary, project_urls = _parse_pypi_payload(body)
        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            return {
                **base,
                "status": "fail",
                "message": f"invalid PyPI JSON: {exc}",
            }
        search_text = " ".join([spec.key, version, summary, project_urls, body])
        base["version"] = version
        base["summary"] = summary
        base["project_urls"] = project_urls
        if not version:
            return {
                **base,
                "status": "warn",
                "message": "PyPI JSON fetched but no version was found",
            }

    hits, missing = _term_hits(search_text, spec.expected_terms)
    base["matched_terms"] = hits
    base["missing_terms"] = missing
    if missing:
        return {
            **base,
            "status": "warn",
            "message": f"source fetched but expected term(s) missing: {', '.join(missing)}",
        }
    version_note = f"; version={base['version']}" if base["version"] else ""
    return {
        **base,
        "status": "ok",
        "message": f"source fetched and expected terms matched{version_note}",
    }


def run_source_audit(
    *,
    root: str | Path = ".",
    timeout: float = 8.0,
    offline: bool = False,
    specs: Iterable[SourceSpec] = DEFAULT_SOURCE_SPECS,
    fetcher: Fetcher = default_fetcher,
    generated_at: str | None = None,
) -> dict[str, Any]:
    rows = [
        audit_source(spec, root=root, timeout=timeout, offline=offline, fetcher=fetcher)
        for spec in specs
    ]
    counts = {"ok": 0, "warn": 0, "fail": 0, "pending": 0}
    for row in rows:
        status = str(row.get("status", "pending") or "pending")
        counts[status] = counts.get(status, 0) + 1
    overall = "fail" if counts.get("fail") else "warn" if (counts.get("warn") or counts.get("pending")) else "ok"
    return {
        "overall": overall,
        "counts": counts,
        "offline": offline,
        "generated_at": generated_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "claim_boundary": (
            "Source audit records public-source freshness only; it does not write JSONL evidence, "
            "does not prove real iPhone response, and does not prove XP parity."
        ),
        "rows": rows,
    }


def source_audit_brief(report: dict[str, Any]) -> str:
    counts = report.get("counts", {}) if isinstance(report.get("counts"), dict) else {}
    rows = report.get("rows", []) if isinstance(report.get("rows"), list) else []
    first_focus = "none"
    for row in rows:
        if not isinstance(row, dict):
            continue
        status = str(row.get("status", "") or "")
        if status in {"fail", "warn", "pending"}:
            first_focus = str(row.get("key", "") or "unknown")
            break
    return (
        f"XP source audit: overall={report.get('overall', '')}; "
        f"ok={counts.get('ok', 0)}, warn={counts.get('warn', 0)}, "
        f"fail={counts.get('fail', 0)}, pending={counts.get('pending', 0)}; "
        f"offline={report.get('offline', False)}; first_focus={first_focus}"
    )


def package_namespace_drift_rows(report: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract PyPI package rows used for dependency-confusion review."""
    rows = report.get("rows", []) if isinstance(report.get("rows"), list) else []
    package_rows: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        if str(row.get("key", "") or "") not in PACKAGE_NAMESPACE_KEYS:
            continue
        package_rows.append({
            "key": str(row.get("key", "") or ""),
            "status": str(row.get("status", "") or "pending"),
            "url": str(row.get("url", "") or ""),
            "version": str(row.get("version", "") or ""),
            "summary": str(row.get("summary", "") or ""),
            "project_urls": str(row.get("project_urls", "") or ""),
            "claim_boundary": str(row.get("claim_boundary", "") or ""),
            "review_rule": (
                "Pin exact version and hashes, review maintainer/source/API surface/license, "
                "then require local API regression tests plus hardware-backed field evidence."
            ),
        })
    return package_rows


def write_source_audit_markdown(report: dict[str, Any], path: str | Path) -> Path:
    out_path = Path(path)
    lines = [
        "# XP Public Source Audit",
        "",
        f"- Generated at: `{report.get('generated_at', '')}`",
        f"- Overall: `{report.get('overall', '')}`",
        f"- Offline mode: `{report.get('offline', False)}`",
        f"- Claim boundary: {report.get('claim_boundary', '')}",
        "",
        "## Rows",
        "",
        "| Key | Status | URL | HTTP | Version | Local doc | Doc stamp | Matched | Missing | SOP owner | Message | Claim boundary |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for row in report.get("rows", []):
        lines.append(
            "| {key} | `{status}` | {url} | {http} | {version} | `{doc}` | {stamp} | {matched} | {missing} | {owner} | {message} | {boundary} |".format(
                key=_md_cell(str(row.get("key", ""))),
                status=_md_cell(str(row.get("status", ""))),
                url=_md_cell(str(row.get("url", ""))),
                http=_md_cell(str(row.get("status_code", ""))),
                version=_md_cell(str(row.get("version", ""))),
                doc=_md_cell(str(row.get("local_doc", ""))),
                stamp=_md_cell(str(row.get("doc_stamp", ""))),
                matched=_md_cell(", ".join(row.get("matched_terms", []) or [])),
                missing=_md_cell(", ".join(row.get("missing_terms", []) or [])),
                owner=_md_cell(str(row.get("sop_owner", ""))),
                message=_md_cell(str(row.get("message", ""))),
                boundary=_md_cell(str(row.get("claim_boundary", ""))),
            )
        )
    if not report.get("rows"):
        lines.append("| none | `pending` | - | - | - | - | - | - | - | - | no rows | Do not promote |")
    lines.extend([
        "",
        "## Use Rule",
        "",
        "Run this audit before changing source-derived docs, package dependencies, compatibility wording, roadmap priority, or demo claims. Treat `warn`, `pending`, and `fail` rows as research/SOP work, not as field evidence. Real iOS control still requires same-run JSONL evidence, screenshot quality, manual observations, Acceptance PASS, and Readiness PASS.",
        "",
    ])
    package_rows = package_namespace_drift_rows(report)
    lines.extend([
        "## Package Namespace Drift",
        "",
        "Track `imouse-py`, `imouse-xp`, and `py-imouse-xp` as separate PyPI namespaces. Similar names are dependency-confusion and SDK-drift signals, not interchangeable install targets.",
        "",
        "| Key | Status | URL | Version | Summary | Project URLs | Review rule | Claim boundary |",
        "|---|---|---|---|---|---|---|---|",
    ])
    if package_rows:
        for row in package_rows:
            lines.append(
                "| {key} | `{status}` | {url} | {version} | {summary} | {project_urls} | {review_rule} | {boundary} |".format(
                    key=_md_cell(row["key"]),
                    status=_md_cell(row["status"]),
                    url=_md_cell(row["url"]),
                    version=_md_cell(row["version"]),
                    summary=_md_cell(row["summary"]),
                    project_urls=_md_cell(row["project_urls"]),
                    review_rule=_md_cell(row["review_rule"]),
                    boundary=_md_cell(row["claim_boundary"]),
                )
            )
    else:
        lines.append(
            "| none | `pending` | - | - | - | - | Rebuild audit with default PyPI specs before dependency review. | Package metadata is not field evidence. |"
        )
    lines.extend([
        "",
        "Do not install any lookalike package on field machines until the artifact is pinned, reviewed, tested, and backed by real receiver/HID/iPhone evidence for the exact scope being claimed.",
        "",
    ])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def _md_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", "<br>")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit public iMouse XP benchmark sources")
    parser.add_argument("--offline", action="store_true", help="Do not fetch; write pending rows")
    parser.add_argument("--timeout", type=float, default=8.0, help="Fetch timeout in seconds")
    parser.add_argument("--markdown", default="", help="Optional Markdown output path")
    parser.add_argument("--json", action="store_true", help="Print audit JSON")
    parser.add_argument("--allow-failures", action="store_true", help="Return 0 even when a source fetch fails")
    args = parser.parse_args(argv)

    report = run_source_audit(timeout=args.timeout, offline=args.offline)
    if args.markdown:
        out_path = write_source_audit_markdown(report, args.markdown)
        if not args.json:
            print(f"Wrote source audit: {out_path}")
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif not args.markdown:
        print(f"XP public source audit: {report['overall']}")
        print(json.dumps(report["counts"], ensure_ascii=False))
    return 0 if args.allow_failures or report["overall"] != "fail" else 1


if __name__ == "__main__":
    raise SystemExit(main())

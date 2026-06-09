import json
import tempfile
import unittest
from pathlib import Path

from imouse.source_audit import (
    DEFAULT_SOURCE_SPECS,
    PACKAGE_NAMESPACE_KEYS,
    SourceSpec,
    audit_source,
    package_namespace_drift_rows,
    run_source_audit,
    source_audit_brief,
    write_source_audit_markdown,
)


def fake_fetcher(payloads):
    def _fetch(url: str, timeout: float):
        payload = payloads[url]
        if isinstance(payload, Exception):
            return {"ok": False, "status_code": 0, "body": "", "error": str(payload)}
        return payload

    return _fetch


class SourceAuditTest(unittest.TestCase):
    def test_default_source_specs_include_all_pypi_package_namespaces(self):
        specs_by_key = {spec.key: spec for spec in DEFAULT_SOURCE_SPECS}

        self.assertEqual(
            set(PACKAGE_NAMESPACE_KEYS),
            {"pypi_imouse_py", "pypi_imouse_xp", "pypi_py_imouse_xp"},
        )
        for key in PACKAGE_NAMESPACE_KEYS:
            self.assertIn(key, specs_by_key)
            self.assertEqual(specs_by_key[key].source_type, "pypi")
            self.assertTrue(specs_by_key[key].url.startswith("https://pypi.org/pypi/"))
            self.assertIn("package", specs_by_key[key].claim_boundary.lower())

        urls = [specs_by_key[key].url for key in PACKAGE_NAMESPACE_KEYS]
        self.assertEqual(len(urls), len(set(urls)))
        self.assertIn("https://pypi.org/pypi/imouse-py/json", urls)
        self.assertIn("https://pypi.org/pypi/imouse-xp/json", urls)
        self.assertIn("https://pypi.org/pypi/py-imouse-xp/json", urls)

    def test_offline_audit_keeps_sources_pending_without_evidence_claim(self):
        spec = SourceSpec(
            key="homepage",
            url="https://example.test/",
            source_type="html",
            local_doc="docs/source.md",
            expected_terms=("AirPlay",),
            source_signal="homepage claims",
            sop_owner="Sources",
            claim_boundary="source only",
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "docs/source.md").write_text("ok", encoding="utf-8")
            report = run_source_audit(
                root=root,
                offline=True,
                specs=(spec,),
                generated_at="2026-06-09T00:00:00Z",
            )
            out = write_source_audit_markdown(report, root / "audit.md")
            text = out.read_text(encoding="utf-8")

        self.assertEqual(report["overall"], "warn")
        self.assertEqual(report["rows"][0]["status"], "pending")
        self.assertFalse(report["rows"][0]["proves_real_ios_control"])
        self.assertFalse(report["rows"][0]["proves_xp_parity"])
        self.assertIn("does not prove real iPhone response", report["claim_boundary"])
        self.assertIn("Offline mode: `True`", text)
        self.assertIn("Real iOS control still requires same-run JSONL evidence", text)

    def test_html_audit_warns_when_expected_terms_drift(self):
        spec = SourceSpec(
            key="homepage",
            url="https://example.test/",
            source_type="html",
            local_doc="docs/source.md",
            expected_terms=("AirPlay", "OpenCV"),
            source_signal="homepage claims",
            sop_owner="Sources",
            claim_boundary="source only",
        )
        row = audit_source(
            spec,
            fetcher=fake_fetcher({
                "https://example.test/": {
                    "ok": True,
                    "status_code": 200,
                    "body": "AirPlay mirror only",
                    "error": "",
                }
            }),
        )

        self.assertEqual(row["status"], "warn")
        self.assertEqual(row["matched_terms"], ["AirPlay"])
        self.assertEqual(row["missing_terms"], ["OpenCV"])
        self.assertIn("expected term", row["message"])

    def test_pypi_audit_extracts_version_and_keeps_boundary(self):
        spec = SourceSpec(
            key="pypi_imouse_py",
            url="https://pypi.org/pypi/imouse-py/json",
            source_type="pypi",
            local_doc="docs/source.md",
            expected_terms=("imouse", "xp"),
            source_signal="package signal",
            sop_owner="Sources",
            claim_boundary="package metadata only",
        )
        payload = {
            "info": {
                "version": "0.0.4",
                "summary": "imouse xp client-server helper",
                "project_urls": {"Homepage": "https://www.imouse.cc/"},
            }
        }
        row = audit_source(
            spec,
            fetcher=fake_fetcher({
                spec.url: {
                    "ok": True,
                    "status_code": 200,
                    "body": json.dumps(payload),
                    "error": "",
                }
            }),
        )

        self.assertEqual(row["status"], "ok")
        self.assertEqual(row["version"], "0.0.4")
        self.assertIn("version=0.0.4", row["message"])
        self.assertFalse(row["proves_real_ios_control"])
        self.assertFalse(row["proves_xp_parity"])

    def test_package_namespace_drift_rows_keep_dependency_boundary(self):
        report = {
            "rows": [
                {
                    "key": "pypi_imouse_py",
                    "status": "ok",
                    "url": "https://pypi.org/pypi/imouse-py/json",
                    "version": "0.0.4",
                    "summary": "imouse xp client-server helper",
                    "project_urls": "Homepage=https://www.imouse.cc/",
                    "claim_boundary": "Package metadata is supply-chain intelligence.",
                },
                {
                    "key": "pypi_imouse_xp",
                    "status": "warn",
                    "url": "https://pypi.org/pypi/imouse-xp/json",
                    "version": "0.0.7",
                    "summary": "similar package namespace",
                    "project_urls": "",
                    "claim_boundary": "Do not adopt similar package names without review.",
                },
                {"key": "homepage", "status": "ok"},
            ],
        }

        rows = package_namespace_drift_rows(report)

        self.assertEqual([row["key"] for row in rows], ["pypi_imouse_py", "pypi_imouse_xp"])
        self.assertIn("Pin exact version and hashes", rows[0]["review_rule"])
        self.assertIn("hardware-backed field evidence", rows[1]["review_rule"])

    def test_fetch_failure_marks_report_fail(self):
        spec = SourceSpec(
            key="homepage",
            url="https://example.test/",
            source_type="html",
            local_doc="docs/source.md",
            expected_terms=("AirPlay",),
            source_signal="homepage claims",
            sop_owner="Sources",
            claim_boundary="source only",
        )
        report = run_source_audit(
            specs=(spec,),
            fetcher=fake_fetcher({"https://example.test/": RuntimeError("timeout")}),
        )

        self.assertEqual(report["overall"], "fail")
        self.assertEqual(report["counts"]["fail"], 1)
        self.assertIn("fetch failed", report["rows"][0]["message"])

    def test_source_audit_brief_points_to_first_attention_row(self):
        report = {
            "overall": "warn",
            "offline": False,
            "counts": {"ok": 1, "warn": 1, "fail": 0, "pending": 0},
            "rows": [
                {"key": "homepage", "status": "ok"},
                {"key": "pypi", "status": "warn"},
            ],
        }

        brief = source_audit_brief(report)

        self.assertIn("overall=warn", brief)
        self.assertIn("first_focus=pypi", brief)

    def test_markdown_includes_package_namespace_drift_guard(self):
        report = {
            "generated_at": "2026-06-09T00:00:00Z",
            "overall": "warn",
            "offline": False,
            "claim_boundary": "source only",
            "rows": [
                {
                    "key": "pypi_imouse_py",
                    "status": "ok",
                    "url": "https://pypi.org/pypi/imouse-py/json",
                    "status_code": 200,
                    "version": "0.0.4",
                    "summary": "imouse xp client-server helper",
                    "project_urls": "Homepage=https://www.imouse.cc/",
                    "local_doc": "docs/xp_public_source_action_map.md",
                    "doc_stamp": "2026-06-09",
                    "matched_terms": ["imouse", "xp"],
                    "missing_terms": [],
                    "sop_owner": "Sources",
                    "message": "source fetched and expected terms matched; version=0.0.4",
                    "claim_boundary": "Package metadata is supply-chain intelligence.",
                },
                {
                    "key": "pypi_imouse_xp",
                    "status": "ok",
                    "url": "https://pypi.org/pypi/imouse-xp/json",
                    "status_code": 200,
                    "version": "0.0.7",
                    "summary": "similar package namespace",
                    "project_urls": "",
                    "local_doc": "docs/xp_public_source_action_map.md",
                    "doc_stamp": "2026-06-09",
                    "matched_terms": ["imouse"],
                    "missing_terms": [],
                    "sop_owner": "Sources",
                    "message": "source fetched and expected terms matched; version=0.0.7",
                    "claim_boundary": "Do not adopt similar package names without review.",
                },
                {
                    "key": "pypi_py_imouse_xp",
                    "status": "ok",
                    "url": "https://pypi.org/pypi/py-imouse-xp/json",
                    "status_code": 200,
                    "version": "1.0.1",
                    "summary": "similar package namespace",
                    "project_urls": "",
                    "local_doc": "docs/xp_public_source_action_map.md",
                    "doc_stamp": "2026-06-09",
                    "matched_terms": ["imouse"],
                    "missing_terms": [],
                    "sop_owner": "Sources",
                    "message": "source fetched and expected terms matched; version=1.0.1",
                    "claim_boundary": "Treat as third-party until reviewed.",
                },
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            out = write_source_audit_markdown(report, Path(tmp) / "audit.md")
            text = out.read_text(encoding="utf-8")

        self.assertIn("Package Namespace Drift", text)
        self.assertIn("dependency-confusion", text)
        self.assertIn("pypi_py_imouse_xp", text)
        self.assertIn("Pin exact version and hashes", text)
        self.assertIn("real receiver/HID/iPhone evidence", text)


if __name__ == "__main__":
    unittest.main()

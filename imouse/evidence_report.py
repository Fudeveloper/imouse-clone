"""Generate Markdown reports from iMouse evidence JSONL files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Optional

from .validation import ValidationRecorder


def recorder_from_jsonl(path: str | Path) -> ValidationRecorder:
    evidence_path = Path(path)
    run_id = evidence_path.stem
    return ValidationRecorder(run_id, evidence_dir=evidence_path.parent)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Generate an iMouse evidence report")
    parser.add_argument("evidence_jsonl", help="Path to evidence/<run_id>.jsonl")
    parser.add_argument("--markdown", default="", help="Optional output Markdown path")
    parser.add_argument("--json", action="store_true", help="Print summary JSON")
    args = parser.parse_args(argv)

    recorder = recorder_from_jsonl(args.evidence_jsonl)
    out_path = recorder.write_summary_markdown(args.markdown or None)
    summary = recorder.summary()
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"Wrote evidence report: {out_path}")
        print(f"Total events: {summary['total']}")
        print(f"Failures: {summary['by_status'].get('fail', 0)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path

# Ensure repo root is on sys.path when run as a script.
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.guardrails.checks.core import run_all

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iac-path", default=os.environ.get("IAC_ROOT"))
    args = ap.parse_args()

    if not args.iac_path:
        print("guardrail unmet")
        print("failed=1 passed=0 skipped=0 stage1_failed=0 stage2_skipped=0")
        print("issues: iac_path_missing=1")
        return 1

    iac = Path(args.iac_path).resolve()
    if not iac.exists():
        print("guardrail unmet")
        print("failed=1 passed=0 skipped=0 stage1_failed=0 stage2_skipped=0")
        print("issues: iac_path_missing=1")
        return 1

    try:
        result = run_all(iac)
    except Exception:
        print("guardrail unmet")
        print("failed=1 passed=0 skipped=0 stage1_failed=0 stage2_skipped=0")
        print("issues: guardrail_runtime_error=1")
        return 1

    if result["failed"] == 0:
        print("guardrail met")
        return 0

    print("guardrail unmet")
    print(
        "failed=%d passed=%d skipped=%d stage1_failed=%d stage2_skipped=%d"
        % (
            result["failed"],
            result["passed"],
            result["skipped"],
            1 if result.get("stage1_failed") else 0,
            1 if result.get("stage2_skipped") else 0,
        )
    )
    for code, count in sorted(result["failures"].items()):
        print(f"- {code}: {count}")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())

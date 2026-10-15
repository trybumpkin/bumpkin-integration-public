"""Build only allowlisted dummy files and emit synthetic build evidence."""

import json
import os
import re
import subprocess
import sys
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build():
    source_sha = os.environ["SOURCE_SHA"]
    fingerprint = os.environ["DRAFT_FINGERPRINT"]
    version = os.environ["RELEASE_VERSION"]
    workflow_sha = os.environ["WORKFLOW_SHA"]
    if not re.fullmatch(r"[0-9a-f]{40}", source_sha):
        raise SystemExit("An exact source SHA is required")
    if not re.fullmatch(r"[0-9a-f]{64}", fingerprint):
        raise SystemExit("A draft fingerprint is required")
    if not re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", version):
        raise SystemExit("A synthetic semantic version is required")
    if not re.fullmatch(r"[0-9a-f]{40}", workflow_sha):
        raise SystemExit("An exact workflow SHA is required")
    actual_sha = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    if actual_sha != source_sha:
        raise SystemExit("Checkout differs from the requested source")
    dirty = subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=no"], cwd=ROOT, text=True
    )
    if dirty:
        raise SystemExit("Tracked source differs from the pinned commit")
    sys.path.insert(0, str(ROOT / "src"))
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful() or result.testsRun < 2 or result.skipped:
        raise SystemExit("Required dummy tests did not pass without skips")
    output = ROOT / "output"
    output.mkdir(exist_ok=False)
    package = ROOT / "src/dummy_release/__init__.py"
    if package.is_symlink() or not package.is_file() or package.stat().st_size > 16384:
        raise SystemExit("Unexpected dummy package input")
    with zipfile.ZipFile(output / "release.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        entry = zipfile.ZipInfo("dummy_release/__init__.py", (2020, 1, 1, 0, 0, 0))
        entry.external_attr = 0o100644 << 16
        archive.writestr(entry, package.read_bytes())
    evidence = {
        "target": "dummy-release",
        "source_sha": source_sha,
        "version": version,
        "draft_fingerprint": fingerprint,
        "build_run_id": int(os.environ["GITHUB_RUN_ID"]),
        "build_run_attempt": int(os.environ["GITHUB_RUN_ATTEMPT"]),
        "workflow_sha": workflow_sha,
        "tests": [{"name": "dummy-tests", "conclusion": "success",
                   "passed": result.testsRun, "failed": 0}],
    }
    (output / "build-evidence.json").write_text(
        json.dumps(evidence, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    build()

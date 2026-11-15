# Tests structurels du blueprint sans photographie réelle.
# SPDX-FileCopyrightText: 2026 PhotoSémantique contributors
# SPDX-License-Identifier: GPL-3.0-only
import json
import subprocess
import sys
from pathlib import Path
from contextlib import closing
import unittest

ROOT = Path(__file__).resolve().parents[1]

class RepositoryPolicyTests(unittest.TestCase):
    def test_structure(self):
        result = subprocess.run([sys.executable, "-X", "utf8", str(ROOT / "scripts/check_repository.py")], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_notice_is_up_to_date(self):
        result = subprocess.run([sys.executable, "-X", "utf8", str(ROOT / "scripts/generate_notice.py"), "--check"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_legal_manifest_has_no_bundled_software(self):
        components = json.loads((ROOT / "third_party/manifest.json").read_text(encoding="utf-8"))["components"]
        self.assertTrue(components)
        self.assertFalse(any(c["bundled"] for c in components if c.get('kind') != 'data'))
        self.assertTrue(all(c['license'] and c['source'] for c in components if c.get('kind') == 'data'))

if __name__ == "__main__": unittest.main()

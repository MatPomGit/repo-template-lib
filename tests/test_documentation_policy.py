"""Unicode documentation character budgets; do not affect code or package archives."""
from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("lib_docs", ROOT / "scripts/validate_documentation.py")
validator = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(validator)


class DocumentationPolicyTests(unittest.TestCase):
    def fixture(self, destination: Path) -> Path:
        shutil.copytree(ROOT, destination, ignore=shutil.ignore_patterns(
            ".git", ".venv", "__pycache__", "site", "outputs"))
        return destination

    def test_scaffold_budgets_pass(self):
        self.assertEqual([], validator.check_documentation(ROOT))

    def test_unicode_codepoints_not_utf8_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            cfg = root / "config/documentation-policy.json"
            obj = json.loads(cfg.read_text())
            obj["exact_limits"]["SUPPORT.md"] = 100
            cfg.write_text(json.dumps(obj), encoding="utf-8")
            (root / "SUPPORT.md").write_text("ą" * 100, encoding="utf-8")
            self.assertEqual([], validator.check_documentation(root))

    def test_overlong_architecture_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            (root / "ARCHITECTURE.md").write_text("x" * 12001, encoding="utf-8")
            self.assertTrue(any("DOC LENGTH EXCEEDED: ARCHITECTURE.md" in e
                                for e in validator.check_documentation(root)))

    def test_new_adr_limit_is_enforced(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            (root / "docs/adr/0004-test.md").write_text("x" * 6501, encoding="utf-8")
            self.assertTrue(any("DOC LENGTH EXCEEDED: docs/adr/0004-test.md" in e
                                for e in validator.check_documentation(root)))

    def test_new_public_page_limit_is_enforced(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            (root / "pages/extra.md").write_text("x" * 6001, encoding="utf-8")
            self.assertTrue(any("DOC LENGTH EXCEEDED: pages/extra.md" in e
                                for e in validator.check_documentation(root)))

    def test_missing_required_governance_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            (root / "GOVERNANCE.md").unlink()
            self.assertIn("DOC MISSING: GOVERNANCE.md",
                          validator.check_documentation(root))

    def test_invalid_schema_version_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            cfg = root / "config/documentation-policy.json"
            obj = json.loads(cfg.read_text())
            obj["schema_version"] = True
            cfg.write_text(json.dumps(obj))
            self.assertIn("DOC POLICY: unsupported schema_version",
                          validator.check_documentation(root))

    def test_invalid_policy_path_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            cfg = root / "config/documentation-policy.json"
            obj = json.loads(cfg.read_text())
            obj["exact_limits"]["../secret.md"] = 300
            cfg.write_text(json.dumps(obj))
            self.assertIn("DOC POLICY: invalid limit or path ../secret.md",
                          validator.check_documentation(root))

    def test_symlink_to_external_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            external = Path(tmp) / "private.md"
            external.write_text("do not publish", encoding="utf-8")
            (root / "SUPPORT.md").unlink()
            (root / "SUPPORT.md").symlink_to(external)
            self.assertIn("DOC SYMLINK: SUPPORT.md",
                          validator.check_documentation(root))


if __name__ == "__main__":
    unittest.main()

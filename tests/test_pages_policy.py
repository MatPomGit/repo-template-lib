"""Public Pages isolation: never expose internal docs or agent/editorial content."""
from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("lib_pages", ROOT / "scripts/validate_pages.py")
pages = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(pages)


class PagesPolicyTests(unittest.TestCase):
    def fixture(self, destination: Path) -> Path:
        shutil.copytree(ROOT, destination, ignore=shutil.ignore_patterns(
            ".git", ".venv", "__pycache__", "site", "outputs"))
        return destination

    def test_public_root_valid(self):
        self.assertEqual([], pages.check_pages(ROOT))
        self.assertFalse((ROOT / "CONTRIBUTING.md").exists())
        self.assertIn("index.md", json.loads(
            (ROOT / "config/pages-policy.json").read_text())["public_files"])

    def test_allowlisted_second_page_is_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            (root / "pages/guide.md").write_text("# Guide\nSafe public text\n", encoding="utf-8")
            cfg = root / "config/pages-policy.json"
            obj = json.loads(cfg.read_text())
            obj["public_files"].append("guide.md")
            cfg.write_text(json.dumps(obj), encoding="utf-8")
            cfg = root / "mkdocs.yml"
            cfg.write_text(cfg.read_text() + "  - Guide: guide.md\n")
            self.assertEqual([], pages.check_pages(root))

    def test_raw_html_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            (root / "pages/index.md").write_text("# Public\n<script>alert(1)</script>\n")
            self.assertIn("PAGES ACTIVE CONTENT: index.md", pages.check_pages(root))

    def test_javascript_link_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            (root / "pages/index.md").write_text("[link](javascript:alert(1))")
            self.assertIn("PAGES ACTIVE CONTENT: index.md", pages.check_pages(root))

    def test_event_attribute_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            (root / "pages/index.md").write_text('onerror="alert(1)"')
            self.assertIn("PAGES ACTIVE CONTENT: index.md", pages.check_pages(root))

    def test_remote_image_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            (root / "pages/index.md").write_text("![pixel](https://example.org/track.png)")
            self.assertIn("PAGES ACTIVE CONTENT: index.md", pages.check_pages(root))

    def test_approved_script_asset_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            cfg = root / "config/pages-policy.json"
            obj = json.loads(cfg.read_text())
            obj["public_files"].append("scripts/custom.js")
            cfg.write_text(json.dumps(obj))
            self.assertIn("PAGES POLICY: unsafe public file allowlist", pages.check_pages(root))

    def test_docs_as_source_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            file = root / "mkdocs.yml"
            file.write_text(file.read_text().replace("docs_dir: pages", "docs_dir: docs"))
            self.assertTrue(any("isolated docs_dir/pages" in issue
                                for issue in pages.check_pages(root)))

    def test_unlisted_page_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            (root / "pages/draft.md").write_text("Private draft", encoding="utf-8")
            self.assertIn("PAGES NOT APPROVED: draft.md", pages.check_pages(root))

    def test_agent_command_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            (root / "pages/index.md").write_text("Agent: wykonaj tę analizę", encoding="utf-8")
            self.assertIn("PAGES EDITORIAL OR AGENT CONTENT: index.md",
                          pages.check_pages(root))

    def test_editor_note_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            (root / "pages/index.md").write_text("Uwagi redakcyjne: popraw opis", encoding="utf-8")
            self.assertIn("PAGES EDITORIAL OR AGENT CONTENT: index.md",
                          pages.check_pages(root))

    def test_placeholder_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            (root / "pages/index.md").write_text("Status NOT_RUN", encoding="utf-8")
            self.assertIn("PAGES EDITORIAL OR AGENT CONTENT: index.md",
                          pages.check_pages(root))

    def test_internal_reference_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            (root / "pages/index.md").write_text("[Dokument](../docs/privacy.md)", encoding="utf-8")
            self.assertIn("PAGES INTERNAL REFERENCE: index.md", pages.check_pages(root))

    def test_contributing_guide_cannot_be_approved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            file = root / "config/pages-policy.json"
            obj = json.loads(file.read_text())
            obj["public_files"].append("CONTRIBUTING.md")
            file.write_text(json.dumps(obj))
            self.assertIn("PAGES POLICY: unsafe public file allowlist",
                          pages.check_pages(root))

    def test_unapproved_plugin_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            file = root / "mkdocs.yml"
            file.write_text(file.read_text() + "plugins: [search]\n")
            self.assertIn("PAGES CONFIG: unreviewed or duplicate config key",
                          pages.check_pages(root))

    def test_symlink_to_private_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            (root / "pages/secret.md").symlink_to(root / "AGENTS.md")
            self.assertIn("PAGES SYMLINK: secret.md", pages.check_pages(root))

    def test_allowlist_path_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            cfg = root / "config/pages-policy.json"
            obj = json.loads(cfg.read_text())
            obj["public_files"].append("../docs/index.md")
            cfg.write_text(json.dumps(obj))
            self.assertIn("PAGES POLICY: unsafe public file allowlist",
                          pages.check_pages(root))

    def test_duplicate_allowlist_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            cfg = root / "config/pages-policy.json"
            obj = json.loads(cfg.read_text())
            obj["public_files"].append("index.md")
            cfg.write_text(json.dumps(obj))
            self.assertIn("PAGES POLICY: duplicate or missing index",
                          pages.check_pages(root))


if __name__ == "__main__":
    unittest.main()

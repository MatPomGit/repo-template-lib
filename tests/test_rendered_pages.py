"""Tests for the generated HTML gate (without MkDocs/network)."""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "lib_render", ROOT / "scripts/validate_rendered_pages.py")
validator = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(validator)
SAFE = '<html><body><div role="main"><p>Visible text</p></div></body></html>'


class RenderedPagesTests(unittest.TestCase):
    def fixture(self, root: Path) -> Path:
        (root / "site").mkdir(parents=True)
        (root / "config").mkdir()
        (root / "config/pages-policy.json").write_text(json.dumps({
            "schema_version": 1, "public_files": ["index.md"]
        }))
        (root / "site/index.html").write_text(SAFE)
        return root

    def test_safe_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual([], validator.check_rendered_pages(self.fixture(Path(tmp) / "lib")))

    def test_detect_script(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            (root / "site/index.html").write_text(SAFE.replace("</p>", "</p><script>x()</script>"))
            self.assertTrue(any("ACTIVE TAG: script" in e for e in validator.check_rendered_pages(root)))

    def test_detect_event_handler(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            (root / "site/index.html").write_text(SAFE.replace("<p>", '<p onerror="x()">'))
            self.assertTrue(any("ACTIVE ATTRIBUTE: onerror" in e for e in validator.check_rendered_pages(root)))

    def test_detect_unsafe_uri(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            (root / "site/index.html").write_text(SAFE.replace("</p>", '</p><a href="javascript:x()">link</a>'))
            self.assertTrue(any("ACTIVE URI" in e for e in validator.check_rendered_pages(root)))

    def test_detect_external_embed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            (root / "site/index.html").write_text(SAFE.replace("</p>", '</p><img src="https://example.org/x.png">'))
            self.assertTrue(any("EXTERNAL EMBED" in e for e in validator.check_rendered_pages(root)))

    def test_missing_main(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            (root / "site/index.html").write_text("<html><body>no main</body></html>")
            self.assertIn("RENDER NO MAIN: index.html", validator.check_rendered_pages(root))

    def test_unapproved_generated_html(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            (root / "site/secret.html").write_text(SAFE)
            self.assertIn("RENDER UNAPPROVED HTML: secret.html", validator.check_rendered_pages(root))

    def test_approved_second_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            cfg = root / "config/pages-policy.json"
            obj = json.loads(cfg.read_text())
            obj["public_files"].append("guide.md")
            cfg.write_text(json.dumps(obj))
            (root / "site/guide").mkdir()
            (root / "site/guide/index.html").write_text(SAFE)
            self.assertEqual([], validator.check_rendered_pages(root))


    def approved_policy(self, root: Path) -> None:
        from shutil import copyfile
        copyfile(ROOT / "config/pages-policy.json", root / "config/pages-policy.json")

    def test_unknown_generated_javascript_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            self.approved_policy(root)
            (root / "site/js").mkdir()
            (root / "site/js/injected.js").write_text("alert(1)", encoding="utf-8")
            self.assertIn("RENDER UNAPPROVED FILE: js/injected.js",
                          validator.check_rendered_pages(root, strict=True))

    def test_pinned_theme_asset_tamper_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            self.approved_policy(root)
            (root / "site/js").mkdir()
            (root / "site/js/base.js").write_text("/* tampered */", encoding="utf-8")
            self.assertIn("RENDER THEME HASH MISMATCH: js/base.js",
                          validator.check_rendered_pages(root, strict=True))

    def test_remote_script_outside_main_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            self.approved_policy(root)
            body = '<html><head><script src="https://cdn.invalid/evil.js"></script></head>'
            (root / "site/index.html").write_text(
                body + '<body><div role="main">Safe</div></body></html>',
                encoding="utf-8")
            self.assertIn("RENDER UNAPPROVED SCRIPT: index.html",
                          validator.check_rendered_pages(root, strict=True))

    def test_inline_script_outside_main_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            self.approved_policy(root)
            body = '<html><head><script>alert(1)</script></head>'
            (root / "site/index.html").write_text(
                body + '<body><div role="main">Safe</div></body></html>',
                encoding="utf-8")
            self.assertIn("RENDER UNAPPROVED INLINE SCRIPT: index.html",
                          validator.check_rendered_pages(root, strict=True))

    def test_remote_stylesheet_outside_main_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            self.approved_policy(root)
            body = '<html><head><link rel="stylesheet" href="https://cdn.invalid/x.css"></head>'
            (root / "site/index.html").write_text(
                body + '<body><div role="main">Safe</div></body></html>',
                encoding="utf-8")
            self.assertIn("RENDER EXTERNAL RESOURCE: index.html",
                          validator.check_rendered_pages(root, strict=True))

    def test_safe_mkdocs_inline_config_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "lib")
            self.approved_policy(root)
            (root / "site/index.html").write_text(
                '<html><head><script>var base_url = "/", shortcuts = '
                '{"help": 191, "next": 78, "previous": 80, "search": 83};'
                '</script></head><body><div role="main">Safe</div></body></html>',
                encoding="utf-8")
            errors = validator.check_rendered_pages(root, strict=True)
            self.assertNotIn("RENDER UNAPPROVED INLINE SCRIPT: index.html", errors)

if __name__ == "__main__":
    unittest.main()

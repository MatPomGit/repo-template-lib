"""Validate the contents of a built MkDocs Pages site before publication.

No network access, deployment or credentials. The source gate (validate_pages)
remains mandatory; output checks provide a second layer, not a sanitizer.
"""
from __future__ import annotations

import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"}
ACTIVE = {"script", "iframe", "object", "embed", "form", "input", "button",
          "video", "audio", "svg", "style", "link", "meta", "base",
          "template", "math", "frame", "frameset"}
DANGEROUS_URI = re.compile(r"^\s*(?:javascript|vbscript|data)\s*:", re.I)


class MainInspector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_main = False
        self.depth = 0
        self.found = False
        self.issues: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        tag = tag.lower()
        attrs_dict = {key.lower(): value or "" for key, value in attrs}
        if not self.in_main:
            if tag == "main" or attrs_dict.get("role", "").lower() == "main":
                self.in_main, self.found, self.depth = True, True, 1
            return
        if tag in ACTIVE:
            self.issues.append("ACTIVE TAG: " + tag)
        for key, value in attrs_dict.items():
            if key.startswith("on") or key in {"srcdoc", "style", "formaction"}:
                self.issues.append("ACTIVE ATTRIBUTE: " + key)
            if key in {"href", "src", "xlink:href"}:
                if DANGEROUS_URI.match(value):
                    self.issues.append("ACTIVE URI: " + key)
                if key == "src" and re.match(r"^\s*https?://", value, re.I):
                    self.issues.append("EXTERNAL EMBED: " + key)
        if tag not in VOID:
            self.depth += 1

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]):
        already_inside = self.in_main
        self.handle_starttag(tag, attrs)
        if already_inside and tag.lower() not in VOID:
            self.depth -= 1

    def handle_endtag(self, tag: str):
        if self.in_main and tag.lower() not in VOID:
            self.depth -= 1
            if self.depth <= 0:
                self.in_main = False
                self.depth = 0


def check_rendered_pages(root: Path = ROOT) -> list[str]:
    root = Path(root).resolve()
    try:
        policy = json.loads((root / "config/pages-policy.json").read_text(encoding="utf-8"))
        approved = policy["public_files"]
        if not isinstance(approved, list) or "index.md" not in approved:
            return ["RENDER POLICY: missing index"]
    except (OSError, UnicodeError, ValueError, TypeError, KeyError):
        return ["RENDER POLICY: unavailable"]
    site = root / "site"
    if not site.is_dir() or site.is_symlink():
        return ["RENDER SITE: missing or unsafe"]

    errors: list[str] = []
    approved_html: set[str] = set()
    for path in approved:
        if not isinstance(path, str) or Path(path).is_absolute() or ".." in Path(path).parts:
            errors.append("RENDER POLICY: unsafe path")
            continue
        src = Path(path)
        if src.suffix.lower() == ".md":
            relative = Path("index.html") if path == "index.md" else src.with_suffix("") / "index.html"
            approved_html.add(relative.as_posix())
        else:
            relative = src
        file = site / relative
        if file.is_symlink() or not file.is_file():
            errors.append("RENDER MISSING: " + relative.as_posix())
            continue
        try:
            if not file.resolve(strict=True).is_relative_to(site) or file.stat().st_size > 2_000_000:
                errors.append("RENDER UNSAFE: " + relative.as_posix())
                continue
            if src.suffix.lower() == ".md":
                inspector = MainInspector()
                inspector.feed(file.read_text(encoding="utf-8"))
                inspector.close()
                if not inspector.found:
                    errors.append("RENDER NO MAIN: " + relative.as_posix())
                errors.extend("RENDER " + issue + " in " + relative.as_posix()
                              for issue in inspector.issues)
        except (OSError, UnicodeError, ValueError):
            errors.append("RENDER UNREADABLE: " + relative.as_posix())

    for file in site.rglob("*.html"):
        path = file.relative_to(site).as_posix()
        if file.is_symlink() or (path not in approved_html and path != "404.html"):
            errors.append("RENDER UNAPPROVED HTML: " + path)
    for file in site.rglob("*"):
        if file.is_symlink():
            errors.append("RENDER SYMLINK: " + file.relative_to(site).as_posix())
        if file.is_file() and file.name.lower() in {
            "agents.md", "agent_workflow.md", "contributing.md", "security.md"
        }:
            errors.append("RENDER INTERNAL DOCUMENT: " + file.relative_to(site).as_posix())
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    errors = check_rendered_pages(args.root)
    for error in errors:
        print("FAIL:", error)
    print("lib-rendered-pages:", "FAIL" if errors else "PASS")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

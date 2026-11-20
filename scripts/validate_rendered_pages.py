"""Validate the contents of a built MkDocs Pages site before publication.

No network access, deployment or credentials. The source gate (validate_pages)
remains mandatory; output checks provide a second layer, not a sanitizer.
"""
from __future__ import annotations

import argparse
import hashlib
import posixpath
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


# The full-site gate is independent from the existing per-content MainInspector.
# Only the fixed, inspected MkDocs inline configuration is allowed to execute.
THEME_INLINE = re.compile(
    r'^\s*var\s+base_url\s*=\s*"(?:/|\.{1,2}(?:/\.\.)*)"\s*,\s*'
    r'shortcuts\s*=\s*\{\s*"help":\s*191,\s*"next":\s*78,\s*'
    r'"previous":\s*80,\s*"search":\s*83\s*\}\s*;\s*
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
    if strict:
        errors.extend(_strict_assets(root, policy, approved))
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    errors = check_rendered_pages(args.root, strict=args.strict)
    for error in errors:
        print("FAIL:", error)
    print("lib-rendered-pages:", "FAIL" if errors else "PASS")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

)
GENERATED = {"sitemap.xml", "sitemap.xml.gz", "search/search_index.json"}
SENSITIVE = {"docs", "profiles", "contracts", "config", "research", "data",
             "manuscripts", "results", "equipment", "private", "raw", "secrets"}
INTERNAL = re.compile(
    r"(?i)(?:\.\./docs/|/\.github/|/AGENTS\.md|/CONTRIBUTING\.md|"
    r"/research/|/private/|/profiles/|file://)"
)


class FullPageInspector(HTMLParser):
    """Reject active/external resources anywhere, not only inside <main>."""

    def __init__(self, name: str, scripts: set[str]):
        super().__init__(convert_charrefs=True)
        self.name = name
        self.scripts = scripts
        self.issues: list[str] = []
        self.refs: list[str] = []
        self.script_open = False
        self.script_fragments: list[str] = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        data = {key.lower(): val or "" for key, val in attrs}
        if tag in {"iframe", "object", "embed", "base"} or (tag == "form" and data):
            self.issues.append("RENDER ACTIVE TAG: " + self.name)
        if any(key.startswith("on") for key in data):
            self.issues.append("RENDER ACTIVE HANDLER: " + self.name)
        if any(DANGEROUS_URI.match(value) for value in data.values()):
            self.issues.append("RENDER ACTIVE URL: " + self.name)
        if tag == "meta" and data.get("http-equiv", "").lower() == "refresh":
            self.issues.append("RENDER META REFRESH: " + self.name)
        for key, value in data.items():
            if key in {"href", "src", "action", "formaction"} and value:
                self.refs.append(value)
        if tag == "script":
            if "src" not in data:
                self.script_open = True
                self.script_fragments = []
            else:
                url = data["src"]
                if url.startswith("/") and not url.startswith("//"):
                    target = url.lstrip("/")
                elif re.match(r"^[a-zA-Z][\w+.-]*:|^//", url):
                    target = ""
                else:
                    target = posixpath.normpath(posixpath.join(
                        posixpath.dirname(self.name), url
                    ))
                if target not in self.scripts:
                    self.issues.append("RENDER UNAPPROVED SCRIPT: " + self.name)
        if tag in {"link", "img", "source"}:
            value = data.get("href", data.get("src", ""))
            if re.match(r"(?i)^https?://|^//", value):
                self.issues.append("RENDER EXTERNAL RESOURCE: " + self.name)

    def handle_data(self, data):
        if self.script_open:
            self.script_fragments.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "script" and self.script_open:
            self.script_open = False
            if not THEME_INLINE.fullmatch("".join(self.script_fragments)):
                self.issues.append("RENDER UNAPPROVED INLINE SCRIPT: " + self.name)


def _strict_assets(root: Path, policy: dict, approved: list[str]) -> list[str]:
    """Fail closed for the COMPLETE site/ output, hash-pinned theme and images."""
    site = root / "site"
    theme = policy.get("approved_theme_assets")
    images = policy.get("approved_image_sha256")
    if (not isinstance(theme, dict) or len(theme) != 24
            or not isinstance(images, dict)
            or any(not isinstance(k, str) or not isinstance(v, str)
                   or not re.fullmatch(r"[0-9a-f]{64}", v)
                   for k, v in [*theme.items(), *images.items()])
            or any(k not in approved for k in images)):
        return ["RENDER POLICY: invalid approved asset hashes"]
    expected_html = {"404.html"}
    expected_source = set()
    for rel in approved:
        path = Path(rel)
        if path.suffix.lower() == ".md":
            expected_html.add("index.html" if rel == "index.md"
                              else (path.with_suffix("") / "index.html").as_posix())
        else:
            expected_source.add(rel)
    expected = expected_html | expected_source | set(theme) | GENERATED
    scripts = {x for x in theme if x.endswith(".js")}
    found: set[str] = set()
    issues: list[str] = []
    for file in sorted(site.rglob("*")):
        rel = file.relative_to(site).as_posix()
        if file.is_symlink():
            issues.append("RENDER SYMLINK: " + rel)
            continue
        if file.is_dir():
            continue
        if (not file.is_file() or
                any(part.startswith(".") or part.lower() in SENSITIVE
                    for part in file.relative_to(site).parts)):
            issues.append("RENDER PRIVATE FILE: " + rel)
            continue
        if rel not in expected:
            issues.append("RENDER UNAPPROVED FILE: " + rel)
            continue
        found.add(rel)
        if rel in theme and hashlib.sha256(file.read_bytes()).hexdigest() != theme[rel]:
            issues.append("RENDER THEME HASH MISMATCH: " + rel)
        if rel in images and hashlib.sha256(file.read_bytes()).hexdigest() != images[rel]:
            issues.append("RENDER IMAGE HASH MISMATCH: " + rel)
        if file.suffix.lower() == ".html":
            try:
                body = file.read_text(encoding="utf-8")
                inspector = FullPageInspector(rel, scripts)
                inspector.feed(body)
                inspector.close()
                issues.extend(inspector.issues)
                if INTERNAL.search(body) or any(INTERNAL.search(u) for u in inspector.refs):
                    issues.append("RENDER INTERNAL REFERENCE: " + rel)
            except (OSError, UnicodeError, ValueError):
                issues.append("RENDER UNREADABLE HTML: " + rel)
        elif rel == "search/search_index.json":
            try:
                index = file.read_text(encoding="utf-8")
                if INTERNAL.search(index):
                    issues.append("RENDER INTERNAL SEARCH INDEX")
            except (OSError, UnicodeError):
                issues.append("RENDER UNREADABLE SEARCH INDEX")
    for rel in sorted(expected_html | set(theme) | expected_source):
        if rel not in found:
            issues.append("RENDER MISSING APPROVED ASSET: " + rel)
    return issues


def check_rendered_pages(root: Path = ROOT, *, strict: bool = False) -> list[str]:
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

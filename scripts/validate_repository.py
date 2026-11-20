"""Offline structural and metadata validation for one library template.

Scaffold is intentionally unconfigured. Release checks declared evidence and
local artifacts; they do not replace independent review or publication approval.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

# Direct execution and isolated test imports resolve helper modules alike.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_documentation import check_documentation
from validate_pages import check_pages

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "README.md", "AGENTS.md", "ARCHITECTURE.md", "PROJECT_STATE.yaml",
    "SECURITY.md", "CODE_OF_CONDUCT.md", "GOVERNANCE.md", "SUPPORT.md",
    ".github/AGENT_WORKFLOW.md", "LICENSE", "CITATION.cff",
    "CHANGELOG.md", "TEMPLATE_SETUP.md", "mkdocs.yml", ".gitignore",
    ".gitattributes", ".github/ACTIONS_POLICY.md", ".github/workflows/ci.yml",
    ".github/PULL_REQUEST_TEMPLATE.md", ".github/ISSUE_TEMPLATE/work-item.md",
    "config/component.json", "config/release-gate.json", "contracts/api.json",
    "config/documentation-policy.json", "config/pages-policy.json",
    "pages/index.md", "scripts/validate_documentation.py",
    "scripts/validate_pages.py", "scripts/validate_rendered_pages.py",
    "tests/test_documentation_policy.py", "tests/test_pages_policy.py",
    "tests/test_rendered_pages.py", "tests/test_agent_policy.py",
    "docs/index.md", "docs/contracts.md", "docs/compatibility.md",
    "docs/consumers.md", "docs/dependencies.md", "docs/testing.md",
    "docs/installation.md", "docs/privacy.md", "docs/releases.md",
    "docs/pages.md", "docs/documentation.md",
    "docs/architecture/README.md", "docs/architecture/components.md",
    "docs/architecture/data-flow.md", "docs/architecture/distribution.md",
    "docs/adr/README.md", "docs/adr/0001-contract.md",
    "docs/adr/0002-security-boundaries.md", "docs/adr/0003-supply-chain.md",
    "docs/security/threat-model.md", "docs/security/supply-chain.md",
    "docs/security/incident-response.md", "docs/operations/runbook.md",
    "profiles/python/AGENTS.md", "profiles/npm/AGENTS.md",
    "profiles/maven/AGENTS.md", "profiles/nuget/AGENTS.md",
    "profiles/oci/AGENTS.md", "profiles/unity/AGENTS.md",
    "src/README.md",
    "examples/README.md", "tests/test_contract.py", "scripts/validate_repository.py",
)
# SemVer 2.0.0: disallow leading zeros in numeric identifiers.
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9]\d*|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*))*))?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
SHA40 = re.compile(r"^[a-f0-9]{40}$")
SHA256 = re.compile(r"^[a-f0-9]{64}$")


def _load_json(root, path, errors):
    try:
        value = json.loads((root / path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        errors.append(f"MALFORMED JSON: {path}: {exc}")
        return None
    if not isinstance(value, dict):
        errors.append(f"INVALID OBJECT: {path}")
        return None
    return value


def _state_metadata(root, errors):
    """Validate the simple top-level YAML mapping used by PROJECT_STATE.yaml.

    This is deliberately *not* a general-purpose YAML parser. Complex YAML
    requires an explicit parser and matching schema before use.
    """
    state = {}
    try:
        lines = (root / "PROJECT_STATE.yaml").read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        errors.append(f"STATE: {exc}")
        return state
    for i, line in enumerate(lines, 1):
        if "\t" in line:
            errors.append(f"STATE: tab at line {i}")
        if not line or line.isspace() or line.lstrip().startswith("#") or line[0].isspace():
            continue
        match = re.fullmatch(r"([a-z][a-z0-9_]*):(?:\s+(.*))?", line)
        if not match:
            errors.append(f"STATE: invalid top-level key at line {i}")
            continue
        key, raw = match.groups()
        if key in state:
            errors.append(f"STATE: duplicate key {key}")
        value = (raw or "").strip()
        if value.startswith(('"', "'")):
            if len(value) < 2 or value[-1] != value[0]:
                errors.append(f"STATE: malformed quoted value {key}")
            else:
                value = value[1:-1]
        state[key] = value
    return state


def _safe_path(root, raw):
    if not isinstance(raw, str) or not raw.strip():
        return None
    rel = Path(raw)
    if rel.is_absolute() or ".." in rel.parts:
        return None
    resolved_root = root.resolve()
    candidate = (root / rel).resolve()
    if not candidate.is_relative_to(resolved_root) or not candidate.is_file():
        return None
    return candidate


def _required_str(data, field, errors, prefix):
    val = data.get(field)
    if not isinstance(val, str) or not val.strip():
        errors.append(f"{prefix}: invalid {field}")
        return ""
    return val


def check(root=ROOT, phase="scaffold"):
    root = Path(root)
    errors = []
    if phase not in ("scaffold", "release"):
        return ["INVALID PHASE"]
    for rel in REQUIRED:
        if not (root / rel).is_file():
            errors.append("MISSING: " + rel)
    if errors:
        return errors
    errors.extend(check_documentation(root))
    errors.extend(check_pages(root))
    if (root / "CONTRIBUTING.md").exists():
        errors.append("CONTRIBUTING.md is not part of the library template")
    if errors:
        return errors
    component = _load_json(root, "config/component.json", errors)
    gate = _load_json(root, "config/release-gate.json", errors)
    contract = _load_json(root, "contracts/api.json", errors)
    if errors:
        return errors

    if component.get("type") != "lib":
        errors.append("WRONG KIND: config/component.json:type")
    if type(component.get("schema_version")) is not int or component["schema_version"] != 1:
        errors.append("SCHEMA: component must be version 1")
    if type(gate.get("schema_version")) is not int or gate["schema_version"] != 1:
        errors.append("SCHEMA: release gate must be version 1")
    if type(contract.get("schema_version")) is not int or contract["schema_version"] != 1:
        errors.append("SCHEMA: API contract must be version 1")
    template_version = _required_str(component, "template_version", errors, "COMPONENT")
    if not SEMVER.fullmatch(template_version):
        errors.append("TEMPLATE VERSION: invalid SemVer")
    version = _required_str(component, "version", errors, "COMPONENT")
    if not SEMVER.fullmatch(version):
        errors.append("VERSION: invalid SemVer")
    for key in ("component_id", "package_identifier", "owner", "display_name"):
        _required_str(component, key, errors, "COMPONENT")
    if component.get("release_status") not in ("scaffold", "development", "release_candidate", "released"):
        errors.append("COMPONENT: invalid release_status")
    for key in ("dependencies", "peer_dependencies", "consumers", "supported_platforms", "compatibility", "dependency_lockfiles", "source_paths"):
        value = component.get(key)
        if not isinstance(value, list):
            errors.append("COMPONENT: expected list " + key)
    entrypoints = contract.get("public_entrypoints")
    if not isinstance(entrypoints, list) or any(not isinstance(s, str) or not s.strip() for s in entrypoints):
        errors.append("CONTRACT: public_entrypoints must be nonempty strings")
    elif len(entrypoints) != len(set(entrypoints)):
        errors.append("CONTRACT: duplicate public_entrypoints")
    for key in ("serialization_contracts", "runtime_requirements"):
        if not isinstance(contract.get(key), list):
            errors.append("CONTRACT: expected list " + key)
    for key in ("stability", "breaking_change_policy", "deprecation_policy"):
        _required_str(contract, key, errors, "CONTRACT")
    if contract.get("name") != component.get("package_identifier"):
        errors.append("CONTRACT: name != package_identifier")
    if contract.get("api_version") != version:
        errors.append("CONTRACT: api_version != component version")
    if component.get("api_contract") != "contracts/api.json":
        errors.append("COMPONENT: api_contract path mismatch")

    state = _state_metadata(root, errors)
    if state.get("repository_type") != "lib":
        errors.append("STATE: repository_type != lib")
    if state.get("schema_version") != "1":
        errors.append("STATE: schema_version != 1")
    if state.get("template_version") != template_version:
        errors.append("STATE: template_version mismatch")
    if state.get("source_version") != version:
        errors.append("STATE: source_version mismatch")
    # Placeholder identifiers may differ in a freshly copied scaffold.
    for state_key, component_key in (("component_id", "component_id"), ("owner", "owner")):
        a, b = state.get(state_key, ""), component.get(component_key, "")
        if not (phase == "scaffold" and str(a).startswith("REPLACE_") and str(b).startswith("REPLACE_")) and a != b:
            errors.append(f"STATE: {state_key} mismatch")
    if not (root / "CITATION.cff").read_text(encoding="utf-8").count('family-names: "Pomianek"'):
        errors.append("CITATION: required author missing")

    if phase == "release":
        for key in ("component_id", "display_name", "owner", "repository_url", "license_spdx", "language", "package_identifier"):
            value = component.get(key)
            if not isinstance(value, str) or not value.strip() or "REPLACE" in value or value == "UNDECIDED":
                errors.append("UNCONFIGURED: config/component.json:" + key)
        if component.get("release_status") in ("scaffold", "development"):
            errors.append("NOT_RELEASED: component is not release-ready")
        if component.get("distribution_kind") in (None, "unselected"):
            errors.append("DISTRIBUTION: missing selected format")
        if not isinstance(entrypoints, list) or not entrypoints:
            errors.append("CONTRACT: no public entrypoints")
        if state.get("lifecycle") == "scaffold" or state.get("release_status") == "not_released":
            errors.append("STATE: not release-ready")
        mandatory = (
            "tests_executed", "license_reviewed", "dependency_audit_passed",
            "clean_install_verified", "public_api_verified",
            "compatibility_documented", "consumer_contracts_verified",
            "publisher_approved",
        )
        for key in mandatory:
            if gate.get(key) is not True:
                errors.append("GATE BLOCKED: " + key)
        sha = gate.get("tested_commit_sha")
        if not isinstance(sha, str) or not SHA40.fullmatch(sha):
            errors.append("MISSING TESTED SHA")
        if _safe_path(root, gate.get("test_report_path")) is None:
            errors.append("MISSING LOCAL TEST EVIDENCE")
        artifact = _safe_path(root, gate.get("release_artifact_path"))
        checksum = gate.get("release_artifact_sha256")
        if artifact is None:
            errors.append("MISSING RELEASE ARTIFACT")
        if not isinstance(checksum, str) or not SHA256.fullmatch(checksum):
            errors.append("MISSING RELEASE ARTIFACT SHA256")
        elif artifact is not None and hashlib.sha256(artifact.read_bytes()).hexdigest() != checksum:
            errors.append("RELEASE ARTIFACT SHA256 MISMATCH")
        license_text = (root / "LICENSE").read_text(encoding="utf-8")
        if "UNDECIDED" in license_text or "NO PUBLIC LICENSE" in license_text:
            errors.append("LICENSE: placeholder has not been replaced")
        elif component.get("license_spdx") == "MIT" and not ("MIT License" in license_text and "Permission is hereby granted" in license_text):
            errors.append("LICENSE: MIT declaration does not match LICENSE")
        elif component.get("license_spdx") == "Apache-2.0" and "Apache License" not in license_text:
            errors.append("LICENSE: Apache-2.0 declaration does not match LICENSE")
        # SHA format and local evidence alone cannot establish independent review,
        # CI provenance, archive content or attribution for third-party dependencies.
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("scaffold", "release"), default="scaffold")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    errors = check(args.root, args.phase)
    for error in errors:
        print("ERROR:", error)
    print(("FAIL" if errors else "PASS") + ": lib " + args.phase + " metadata/evidence checks")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

"""Offline template contract checks; no network, packages, or external commands."""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_KIND = "lib"
REQUIRED = (
  "README.md", "AGENTS.md", "ARCHITECTURE.md", "PROJECT_STATE.yaml",
  "SECURITY.md", "CONTRIBUTING.md", "LICENSE", "CITATION.cff",
  "CHANGELOG.md", "TEMPLATE_SETUP.md", "mkdocs.yml", ".gitignore",
  ".gitattributes", ".github/ACTIONS_POLICY.md",
  ".github/PULL_REQUEST_TEMPLATE.md", ".github/ISSUE_TEMPLATE/work-item.md",
  "config/component.json", "config/release-gate.json", "docs/index.md",
  "docs/contracts.md", "docs/compatibility.md", "docs/consumers.md",
  "docs/dependencies.md", "docs/testing.md",
  "docs/installation.md", "docs/privacy.md", "docs/releases.md",
  "docs/pages.md", "docs/adr/0001-contract.md", "src/README.md",
  "examples/README.md", "tests/test_contract.py", "scripts/validate_repository.py",
)
VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
CHECKSUM_PATTERN = re.compile(r"^[0-9a-f]{64}$")

def check(root=ROOT, phase="scaffold"):
    errors=[]
    for rel in REQUIRED:
        if not (root/rel).is_file():
            errors.append("MISSING: " + rel)
    if EXPECTED_KIND == "app":
        additional=("docs/hardware.md", "contracts/events.schema.json", "examples/event.synthetic.json")
    else:
        additional=("contracts/api.json",)
    for rel in additional:
        if not (root/rel).is_file():
            errors.append("MISSING: " + rel)
    if errors:
        return errors
    try:
        c=json.loads((root/"config/component.json").read_text(encoding="utf-8"))
        gate=json.loads((root/"config/release-gate.json").read_text(encoding="utf-8"))
        contract=json.loads((root/("contracts/events.schema.json" if EXPECTED_KIND=="app" else "contracts/api.json")).read_text(encoding="utf-8"))
    except (OSError,ValueError) as exc:
        return ["MALFORMED JSON: " + str(exc)]
    if c.get("type") != EXPECTED_KIND:
        errors.append("WRONG KIND: config/component.json:type")
    if c.get("template_version") != "1.0.0":
        errors.append("TEMPLATE VERSION: expected 1.0.0")
    if not isinstance(c.get("schema_version"),int) or c["schema_version"]!=1:
        errors.append("SCHEMA: expected schema_version 1")
    if not VERSION_PATTERN.fullmatch(str(c.get("version",""))):
        errors.append("VERSION: invalid SemVer")
    if gate.get("schema_version") != 1:
        errors.append("RELEASE GATE: invalid schema_version")
    if contract.get("schema_version",1)!=1:
        errors.append("CONTRACT: unsupported schema_version")
    # Independent starter has a declared but non-validated component.
    if phase=="release":
        for key in ("component_id","display_name","owner","repository_url","license_spdx"):
            val=c.get(key)
            if not isinstance(val,str) or not val.strip() or "REPLACE" in val or val=="UNDECIDED":
                errors.append("UNCONFIGURED: config/component.json:"+key)
        if c.get("release_status")=="scaffold":
            errors.append("NOT_RELEASED: component still scaffold")
        if c.get("type")=="app":
            for k in ("runtime",):
                if "REPLACE" in str(c.get(k,"")):
                    errors.append("UNCONFIGURED: "+k)
            if not c.get("platforms"):
                errors.append("PLATFORMS: no declared platform")
            if c.get("data_classification")=="unassessed" or c.get("network_egress")=="unassessed":
                errors.append("DATA GOVERNANCE: not assessed")
            if c.get("hardware_required"):
                if not c.get("equipment_refs"):
                    errors.append("EQUIPMENT: missing references")
                if not gate.get("hardware_verified") or not gate.get("hardware_report_path"):
                    errors.append("HARDWARE: physical validation not evidenced")
            mandatory=("tests_executed","license_reviewed","privacy_reviewed","dependency_audit_passed","installation_verified","compatibility_documented","publisher_approved")
        else:
            for k in ("language","package_identifier"):
                if "REPLACE" in str(c.get(k,"")):
                    errors.append("UNCONFIGURED: "+k)
            if c.get("distribution_kind") in (None,"unselected"):
                errors.append("DISTRIBUTION: missing selected format")
            if not c.get("consumers"):
                errors.append("CONSUMERS: no verified consumer documented")
            mandatory=("tests_executed","license_reviewed","dependency_audit_passed","clean_install_verified","public_api_verified","compatibility_documented","consumer_contracts_verified","publisher_approved")
        for field in mandatory:
            if gate.get(field) is not True:
                errors.append("GATE BLOCKED: "+field)
        sha=gate.get("tested_commit_sha")
        if not isinstance(sha,str) or not SHA_PATTERN.fullmatch(sha):
            errors.append("MISSING TESTED SHA")
        report=gate.get("test_report_path")
        if not isinstance(report,str) or not report or Path(report).is_absolute() or ".." in Path(report).parts or not (root/report).is_file():
            errors.append("MISSING LOCAL TEST EVIDENCE")
        checksum=gate.get("release_artifact_sha256")
        if not isinstance(checksum,str) or not CHECKSUM_PATTERN.fullmatch(checksum):
            errors.append("MISSING RELEASE ARTIFACT SHA256")
        # The validator cannot prove that the report was independently reviewed.
    return errors

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--phase",choices=("scaffold","release"),default="scaffold")
    parser.add_argument("--root",type=Path,default=ROOT)
    args=parser.parse_args()
    errors=check(args.root,args.phase)
    for line in errors:
        print("ERROR:",line)
    print(("FAIL" if errors else "PASS")+": "+EXPECTED_KIND+" "+args.phase+" structural/declared-evidence check")
    return 1 if errors else 0

if __name__=="__main__":
    sys.exit(main())

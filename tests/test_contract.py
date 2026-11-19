"""Negative and positive scaffold tests; no external SDK or network calls."""
import json
import tempfile
import unittest
import shutil
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from validate_repository import check

class ContractTests(unittest.TestCase):
    def test_scaffold_structure_is_complete(self):
        self.assertEqual([],check(ROOT,"scaffold"))

    def test_release_cannot_pass_by_default(self):
        errors=check(ROOT,"release")
        self.assertTrue(errors)
        self.assertIn("GATE BLOCKED: tests_executed",errors)

    def test_missing_required_file_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)
            shutil.copytree(ROOT,target,dirs_exist_ok=True)
            (target/"README.md").unlink()
            self.assertIn("MISSING: README.md",check(target,"scaffold"))

    def test_wrong_component_kind_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)
            shutil.copytree(ROOT,target,dirs_exist_ok=True)
            p=target/"config/component.json"
            x=json.loads(p.read_text(encoding="utf-8"))
            x["type"]="wrong"
            p.write_text(json.dumps(x),encoding="utf-8")
            self.assertIn("WRONG KIND: config/component.json:type",check(target,"scaffold"))

if __name__=="__main__":
    unittest.main()

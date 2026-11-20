"""Core security and agent policy invariants for library template."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class GovernanceTests(unittest.TestCase):
    def test_policy_and_workflow_present(self):
        content = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        content += (ROOT / ".github/AGENT_WORKFLOW.md").read_text(encoding="utf-8")
        for token in ("R0", "R1", "R2", "R3", "DoR", "DoD",
                      "SHA", "Research Autopilot", "pages/"):
            with self.subTest(token=token):
                self.assertIn(token.lower(), content.lower())

    def test_local_profiles_exist(self):
        for profile in ("python", "npm", "maven", "nuget", "oci", "unity"):
            with self.subTest(profile=profile):
                doc = ROOT / "profiles" / profile / "AGENTS.md"
                self.assertTrue(doc.is_file())
                self.assertIn("AGENTS.md", doc.read_text(encoding="utf-8"))

    def test_no_contribution_guide(self):
        self.assertFalse((ROOT / "CONTRIBUTING.md").exists())
        self.assertFalse((ROOT / "pages/CONTRIBUTING.md").exists())

    def test_only_publicly_approved_pages(self):
        policy = json.loads((ROOT / "config/pages-policy.json").read_text())
        self.assertEqual(["index.md"], policy["public_files"])
        self.assertFalse((ROOT / "pages/AGENTS.md").exists())


if __name__ == "__main__":
    unittest.main()

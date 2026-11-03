"""Spec Ghost tests — fresh code for Kiroween 2026, stdlib unittest."""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.specghost import banish_plan, discover_code_files, discover_specs, scan

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def write(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)
    return path


class TestDiscovery(unittest.TestCase):
    def test_discovers_directory_spec(self):
        with tempfile.TemporaryDirectory() as root:
            write(root, ".kiro/specs/alpha/requirements.md", "Spec alpha.")
            specs = discover_specs(root)
            self.assertIn("alpha", specs)

    def test_discovers_lone_file_spec(self):
        with tempfile.TemporaryDirectory() as root:
            write(root, ".kiro/specs/beta.md", "Spec beta.")
            self.assertIn("beta", discover_specs(root))

    def test_no_specs_dir_is_zero_not_crash(self):
        with tempfile.TemporaryDirectory() as root:
            self.assertEqual(discover_specs(root), {})

    def test_code_discovery_skips_kiro_and_pycache(self):
        with tempfile.TemporaryDirectory() as root:
            write(root, "app/main.py", "print(1)")
            write(root, "__pycache__/main.pyc", "x")
            write(root, ".kiro/specs/alpha/requirements.md", "not code")
            files = discover_code_files(root)
            self.assertIn("app/main.py", files)
            self.assertNotIn(".kiro/specs/alpha/requirements.md", files)


class TestCoverage(unittest.TestCase):
    def _house(self, root):
        write(root, ".kiro/specs/covered/requirements.md", "See app/a.py.")
        write(root, ".kiro/specs/ghost/requirements.md", "Nothing references me.")
        write(root, "app/a.py", "# spec: covered\nprint(1)")
        write(root, "app/b.py", "print(2)")

    def test_covered_and_ghost(self):
        with tempfile.TemporaryDirectory() as root:
            self._house(root)
            report = scan(root)
            self.assertIn("covered", report["covered_specs"])
            self.assertIn("ghost", report["ghost_specs"])

    def test_unmarked_code(self):
        with tempfile.TemporaryDirectory() as root:
            self._house(root)
            report = scan(root)
            self.assertIn("app/b.py", report["unmarked_code_files"])
            self.assertNotIn("app/a.py", report["unmarked_code_files"])

    def test_hyphen_underscore_equivalent(self):
        with tempfile.TemporaryDirectory() as root:
            write(root, ".kiro/specs/my-spec/requirements.md", "Spec.")
            write(root, "app/a.py", "my_spec is referenced here")
            report = scan(root)
            self.assertIn("my-spec", report["covered_specs"])

    def test_stale_spec(self):
        with tempfile.TemporaryDirectory() as root:
            write(root, ".kiro/specs/old/requirements.md", "See app/gone.py for details.")
            write(root, "app/a.py", "print(1)")
            report = scan(root)
            stale = {s["spec"]: s["missing_files"] for s in report["stale_specs"]}
            self.assertIn("old", stale)
            self.assertIn("app/gone.py", stale["old"])

    def test_existing_mention_is_not_stale(self):
        with tempfile.TemporaryDirectory() as root:
            write(root, ".kiro/specs/ok/requirements.md", "See app/a.py.")
            write(root, "app/a.py", "# spec: ok\nprint(1)")
            report = scan(root)
            self.assertEqual(report["stale_specs"], [])


class TestBanishAndDemo(unittest.TestCase):
    def test_banish_plan_changes_nothing(self):
        with tempfile.TemporaryDirectory() as root:
            write(root, ".kiro/specs/ghost/requirements.md", "Ghost.")
            write(root, "app/a.py", "print(1)")
            before = sorted(os.listdir(root))
            report = scan(root)
            plan = banish_plan("ghost", report)
            self.assertFalse(plan["deletes_anything"])
            self.assertIn("BY HAND", " ".join(plan["actions"]))
            self.assertEqual(sorted(os.listdir(root)), before)

    def test_banish_non_ghost_says_so(self):
        with tempfile.TemporaryDirectory() as root:
            write(root, ".kiro/specs/real/requirements.md", "Real.")
            write(root, "app/a.py", "# spec: real\nprint(1)")
            plan = banish_plan("real", scan(root))
            self.assertIn("Not a ghost", plan["plan"])

    def test_demo_house_shows_all_four_categories(self):
        report = scan(os.path.join(BASE, "sample"))
        self.assertIn("room-lighting", report["covered_specs"])
        self.assertIn("ghost-door", report["ghost_specs"])
        self.assertIn("app/unmarked.py", report["unmarked_code_files"])
        stale = {s["spec"]: s["missing_files"] for s in report["stale_specs"]}
        self.assertIn("app/missing.py", stale.get("room-lighting", []))

    def test_gitignore_never_ignores_kiro(self):
        with open(os.path.join(BASE, ".gitignore")) as f:
            content = f.read()
        for line in content.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                self.assertNotIn(".kiro", line)

    def test_scan_is_json_serialisable(self):
        with tempfile.TemporaryDirectory() as root:
            write(root, ".kiro/specs/a/requirements.md", "Spec a.")
            write(root, "app/a.py", "print(1)")
            json.dumps(scan(root))  # must not raise


if __name__ == "__main__":
    unittest.main()

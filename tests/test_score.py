#!/usr/bin/env python3
"""score.py prints a lifecycle sequence or refuses a generic drip and a cold email."""

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = "incomplete-json-probe"


GOOD = json.loads((ROOT / "examples" / "lifecycle-good.json").read_text())


def run(args, stdin=None):
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "score.py"), *args],
        input=stdin,
        capture_output=True,
        text=True,
    )


class ScoreLifecycle(unittest.TestCase):
    def test_good_draft_prints_three(self):
        result = run(["--file", str(ROOT / "examples" / "lifecycle-good.json")])
        self.assertEqual(result.returncode, 0)
        self.assertIn("welcome: You asked for the trial checklist.", result.stdout)
        self.assertIn("bargain: The checklist is the bargain.", result.stdout)
        self.assertIn("nurture: The next note stays on the pain you showed: the trial dies after the first login.", result.stdout)

    def test_refused_exits_1(self):
        result = run(["--file", str(ROOT / "examples" / "lifecycle-refused.json")])
        self.assertEqual(result.returncode, 1)
        self.assertIn("a generic drip and a cold email", result.stdout)
        self.assertNotIn("welcome:", result.stdout)

    def test_bad_json_hides_input(self):
        bad = run(["--stdin"], stdin='{"welcome": "' + CELL)
        self.assertNotEqual(bad.returncode, 0)
        self.assertNotIn(CELL, bad.stdout + bad.stderr)
        self.assertIn("invalid JSON", bad.stderr)
        array = run(["--stdin"], stdin='["' + CELL + '"]')
        self.assertNotEqual(array.returncode, 0)
        self.assertNotIn(CELL, array.stdout + array.stderr)
        self.assertIn("JSON must be an object", array.stderr)

    def test_refused_names_each_gate(self):
        result = run(["--file", str(ROOT / "examples" / "lifecycle-refused.json")])
        self.assertIn('- cold email: welcome says "introduce our"', result.stdout)
        self.assertIn('- generic drip: bargain says "Day 1"', result.stdout)
        self.assertIn("- pain mismatch:", result.stdout)

    def test_missing_part_is_incomplete(self):
        draft = dict(GOOD, bargain="  ")
        result = run(["--stdin"], stdin=json.dumps(draft))
        self.assertEqual(result.returncode, 1)
        self.assertIn("draft is incomplete", result.stdout)
        self.assertIn("- missing: bargain", result.stdout)

    def test_pain_mismatch_refused(self):
        draft = dict(GOOD, nurture="Here is a tip about onboarding.")
        result = run(["--stdin"], stdin=json.dumps(draft))
        self.assertEqual(result.returncode, 1)
        self.assertIn("a generic drip and a cold email", result.stdout)
        self.assertIn("- pain mismatch:", result.stdout)

    def test_pain_match_ignores_case_spacing_and_end_punctuation(self):
        draft = dict(GOOD, pain="The Trial dies after the first login.",
                     nurture="Still on it: the trial  dies after\nthe first login, again.")
        result = run(["--stdin"], stdin=json.dumps(draft))
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_json_output(self):
        good = run(["--file", str(ROOT / "examples" / "lifecycle-good.json"), "--json"])
        self.assertEqual(good.returncode, 0)
        body = json.loads(good.stdout)
        self.assertTrue(body["pass"])
        self.assertEqual(body["reasons"], [])
        self.assertEqual(body["nurture"], GOOD["nurture"])
        bad = run(["--file", str(ROOT / "examples" / "lifecycle-refused.json"), "--json"])
        self.assertEqual(bad.returncode, 1)
        body = json.loads(bad.stdout)
        self.assertFalse(body["pass"])
        self.assertNotIn("welcome", body)
        self.assertTrue(body["reasons"])

    def test_input_errors_exit_2(self):
        self.assertEqual(run([]).returncode, 2)
        self.assertEqual(run(["--file", str(ROOT / "nope.json")]).returncode, 2)
        both = run(["--file", str(ROOT / "examples" / "lifecycle-good.json"), "--stdin"], stdin="{}")
        self.assertEqual(both.returncode, 2)


class PackLayout(unittest.TestCase):
    def frontmatter(self):
        text = (ROOT / "SKILL.md").read_text()
        match = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
        self.assertIsNotNone(match, "SKILL.md needs YAML frontmatter")
        fields = {}
        for line in match.group(1).splitlines():
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip().strip('"')
        return fields

    def test_skill_frontmatter(self):
        fields = self.frontmatter()
        self.assertRegex(fields["name"], r"^[a-z0-9-]{1,64}$")
        self.assertTrue(0 < len(fields["description"]) <= 1024)
        self.assertLessEqual(set(fields), {"name", "description", "license", "allowed-tools", "metadata", "models"})

    def test_plugin_manifest(self):
        manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        self.assertRegex(manifest["name"], r"^[a-z0-9-]+$")
        self.assertRegex(manifest["version"], r"^\d+\.\d+\.\d+$")
        self.assertTrue((ROOT / manifest["icon"]).is_file())


if __name__ == "__main__":
    unittest.main()

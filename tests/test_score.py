#!/usr/bin/env python3
"""score.py prints a lifecycle sequence or refuses a generic drip and a cold email."""

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = "incomplete-json-probe"


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
        self.assertIn("welcome subject: You asked for the trial checklist", result.stdout)
        self.assertIn("bargain subject: The checklist is attached", result.stdout)
        self.assertIn("nurture subject: The trial dies after the first login", result.stdout)
        self.assertIn("welcome when: The day they opt in.", result.stdout)
        self.assertIn("bargain when: The next morning.", result.stdout)
        self.assertIn("nurture when: After the bargain is in their hands.", result.stdout)

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

    def test_three_notes_substance(self):
        import json
        payload = {
            "pain": "the trial dies after the first login",
            "welcome_subject": "You asked for the trial checklist",
            "welcome_when": "The day they opt in. Example timing, replace this: within 1 hour.",
            "welcome": "You asked for the trial checklist. This note starts there.",
            "bargain_subject": "The checklist is attached",
            "bargain_when": "The next morning. Example timing, replace this: 1 morning after the welcome.",
            "bargain": "The checklist is the bargain. It is attached.",
            "nurture_subject": "Checking in",
            "nurture_when": "After the bargain is in their hands. Example timing, replace this: 2 mornings after the bargain.",
            "nurture": "The next note stays on the pain you showed: the trial dies after the first login.",
        }
        missed = run(["--stdin"], stdin=json.dumps(payload))
        self.assertEqual(missed.returncode, 1)
        self.assertEqual(missed.stdout.strip(), "nurture does not name the pain")
        payload["nurture_subject"] = "The trial dies after the first login"
        payload["welcome_when"] = "Send it whenever."
        late = run(["--stdin"], stdin=json.dumps(payload))
        self.assertEqual(late.returncode, 1)
        self.assertEqual(late.stdout.strip(), "timing is not three notes")
        payload["welcome_when"] = "The day they opt in, within 4 hours."
        numbered = run(["--stdin"], stdin=json.dumps(payload))
        self.assertEqual(numbered.returncode, 1)
        self.assertEqual(numbered.stdout.strip(), "timing number is not labeled example")
        payload["welcome_when"] = "The day they opt in."
        payload["bargain"] = payload["welcome"]
        same = run(["--stdin"], stdin=json.dumps(payload))
        self.assertEqual(same.returncode, 1)
        self.assertEqual(same.stdout.strip(), "the notes are not three")


if __name__ == "__main__":
    unittest.main()

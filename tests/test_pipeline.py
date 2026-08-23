#!/usr/bin/env python3
"""Sanity checks for the Mahabali storyboard pipeline (no API calls)."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from grok_storyboard_pipeline import (  # noqa: E402
    SHOTS,
    build_motion_prompt,
    build_prompt,
)


class ShotListTests(unittest.TestCase):
    def test_unique_ids(self):
        ids = [s["id"] for s in SHOTS]
        self.assertEqual(ids, sorted(set(ids), key=ids.index))

    def test_required_fields(self):
        required = {"id", "scene", "timecode", "lens", "start_action", "end_action"}
        for shot in SHOTS:
            self.assertTrue(required.issubset(shot), shot["id"])
            self.assertGreater(len(shot["start_action"]), 20, shot["id"])
            self.assertGreater(len(shot["end_action"]), 20, shot["id"])

    def test_thirteen_shots(self):
        self.assertEqual(len(SHOTS), 13)


class PromptTests(unittest.TestCase):
    def test_prompt_embeds_action_and_lens(self):
        shot = SHOTS[0]
        prompt = build_prompt(shot["start_action"], shot["lens"])
        self.assertIn(shot["start_action"], prompt)
        self.assertIn(shot["lens"], prompt)
        self.assertIn("Mahabali", prompt)
        self.assertIn("photorealistic", prompt.lower())

    def test_motion_prompt_names_both_beats(self):
        shot = SHOTS[4]
        motion = build_motion_prompt(shot)
        self.assertIn(shot["id"], motion)
        self.assertIn(shot["start_action"], motion)
        self.assertIn(shot["end_action"], motion)


class DryRunTests(unittest.TestCase):
    def test_dry_run_writes_twenty_six_prompts_and_viewer(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [sys.executable, str(ROOT / "grok_storyboard_pipeline.py"),
                 "--dry-run", "--out-dir", tmp],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("26 frame(s)", result.stdout)
            out = Path(tmp)
            txts = sorted(out.glob("*.txt"))
            self.assertEqual(len(txts), 26)
            self.assertTrue((out / "index.html").exists())
            manifest = json.loads((out / "storyboard_manifest.json").read_text())
            self.assertEqual(len(manifest), 26)
            self.assertEqual(manifest[0]["shot_id"], "shot_01")
            self.assertEqual(manifest[0]["frame_type"], "start")
            self.assertEqual(manifest[-1]["shot_id"], "title_card")
            self.assertEqual(manifest[-1]["frame_type"], "end")

    def test_single_shot_filter(self):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                [sys.executable, str(ROOT / "grok_storyboard_pipeline.py"),
                 "--dry-run", "--shot", "shot_05", "--out-dir", tmp],
                check=True,
                capture_output=True,
                text=True,
            )
            names = sorted(p.name for p in Path(tmp).glob("*.txt"))
            self.assertEqual(names, ["001_shot_05_start.txt", "002_shot_05_end.txt"])

    def test_unknown_shot_exits(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [sys.executable, str(ROOT / "grok_storyboard_pipeline.py"),
                 "--dry-run", "--shot", "shot_99", "--out-dir", tmp],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("shot_99", result.stderr + result.stdout)


if __name__ == "__main__":
    unittest.main()

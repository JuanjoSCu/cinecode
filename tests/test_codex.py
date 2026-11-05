"""Codex adapter checks for film setup and handoff. Author: JuanjoSC."""

import os
import subprocess
import sys
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch


KIT = Path(__file__).resolve().parents[1]


class CodexRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.env = dict(os.environ, CINECODE_HOST="codex", CINECODE_NO_OPEN="1")
        self.env.pop("CLAUDECODE", None)
        self.env.pop("CLAUDE_CODE_ENTRYPOINT", None)

    def run_script(self, script, *args, cwd=None):
        return subprocess.run([sys.executable, str(KIT / "scripts" / script), *map(str, args)],
                              cwd=cwd or self.root, env=self.env, capture_output=True, text=True,
                              encoding="utf-8", check=True)

    def test_quick_and_film_projects_point_to_the_codex_kit(self):
        for quick in (True, False):
            with self.subTest(quick=quick):
                film = self.root / ("quick" if quick else "film")
                args = [film, "--title", "A Film"] + (["--quick"] if quick else [])
                result = self.run_script("init_film.py", *args)
                agents = (film / "AGENTS.md").read_text(encoding="utf-8")
                self.assertIn(f"`{KIT}/SKILL.md`", agents)
                self.assertIn("Codex adapter", agents)
                self.assertNotIn("Skill tool", agents)
                self.assertNotIn("OUTSIDE THIS CHAT", result.stdout)
                self.assertTrue((film / "tools" / "brief.py").is_file())

    def test_update_tools_keeps_the_films_own_instructions(self):
        film = self.root / "quick"
        self.run_script("init_film.py", film, "--quick")
        agents = film / "AGENTS.md"
        agents.write_text(agents.read_text(encoding="utf-8") + "\nMY RULE: keep the title\n", encoding="utf-8")
        result = self.run_script("init_film.py", film, "--update-tools")
        self.assertIn("MY RULE: keep the title", agents.read_text(encoding="utf-8"))
        self.assertIn("Codex adapter", agents.read_text(encoding="utf-8"))
        self.assertIn("tools refreshed", result.stdout)

    def test_brief_names_available_codex_model_families(self):
        film = self.root / "quick"
        self.run_script("init_film.py", film, "--quick")
        for kind, model, effort in (("voice", "gpt-6-luna", "low"),
                                    ("files", "gpt-6-luna", "low"),
                                    ("sourcing", "gpt-6-sol", "medium")):
            with self.subTest(kind=kind):
                result = self.run_script("brief.py", kind, "--task", "One task", "--writes", "review/own.md",
                                         "--reads", "STATE.md", "--done", "one result", cwd=film)
                self.assertIn(f"model {model}, effort {effort}", result.stderr)
                self.assertIn("check availability", result.stderr)
                self.assertIn("WRITES: review/own.md", result.stdout)

    def test_handoff_is_manual_and_supports_spanish(self):
        film = self.root / "quick"
        self.run_script("init_film.py", film, "--quick")
        result = self.run_script("handoff.py", "--folder", film, "--lang", "es", "--dry-run")
        self.assertIn("new Codex chat", result.stdout)
        self.assertIn("Continúa desde STATE.md", result.stdout)
        self.assertIn("No chat was opened", result.stdout)
        self.assertNotIn("claude://", result.stdout)

    def test_codex_host_takes_precedence_over_inherited_claude_variables(self):
        film = self.root / "quick"
        mixed = dict(self.env, CLAUDECODE="1", CLAUDE_CODE_ENTRYPOINT="claude-desktop")
        with patch.dict(self.env, mixed, clear=True):
            result = self.run_script("init_film.py", film, "--quick")
        self.assertNotIn("OUTSIDE THIS CHAT", result.stdout)
        self.assertNotIn("GUARD OFF", result.stdout)

        sys.path.insert(0, str(KIT / "scripts"))
        import init_film
        import make
        with patch.dict(os.environ, mixed, clear=True):
            self.assertEqual(init_film.outside_chat(str(film), str(self.root / "elsewhere")), "")
            self.assertEqual(init_film.guard_off(), "")
            self.assertEqual(make.guard_off(), "")

    def test_init_rejects_projects_inside_the_kit_before_writing(self):
        name = "cinecode-test-" + uuid.uuid4().hex
        target = KIT / name
        for destination, cwd in ((name, KIT), (str(target), self.root)):
            with self.subTest(destination=destination):
                result = subprocess.run([sys.executable, str(KIT / "scripts" / "init_film.py"), destination, "--quick"],
                                        cwd=cwd, env=self.env, capture_output=True, text=True, encoding="utf-8")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("KIT FOLDER", result.stderr)
                self.assertIn("separate project folder", result.stderr)
                self.assertFalse(target.exists())
                self.assertFalse((KIT / "Filmler" / name).exists())
                self.assertFalse((KIT / "Films" / name).exists())


if __name__ == "__main__":
    unittest.main()

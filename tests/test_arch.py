import shutil
import subprocess
import tempfile
from pathlib import Path
import unittest

from test_tickets import BASH, REPO


class ArchCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not BASH or not Path(BASH).is_file() or not shutil.which("php") or not shutil.which("git"):
            raise RuntimeError("A prova exige Bash, PHP e Git no PATH.")

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="skills-arch-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / "project"
        self.project.mkdir()
        subprocess.run(["git", "init", "-q", str(self.project)], check=True, capture_output=True)
        for directory in ("tests/Arch", "tests/Unit", "app/Models", "vendor/bin"):
            (self.project / directory).mkdir(parents=True)
        (self.project / "tests/Arch/ModelsTest.php").write_text("<?php\n", encoding="utf-8")
        # O stub isola a checagem do XML: não testa arch() nem substitui uma execução real do Pest.
        (self.project / "vendor/bin/pest").write_text(
            """<?php
if (is_file('app/Models/ViolacaoControladaArch.php')) {
    echo "ViolacaoControladaArch failed\n";
    exit(1);
}
exit(0);
""",
            encoding="utf-8",
        )

    def prove(self, suites):
        (self.project / "phpunit.xml").write_text(
            '<?xml version="1.0"?><phpunit><testsuites>' + suites + "</testsuites></phpunit>",
            encoding="utf-8",
        )
        return subprocess.run(
            [
                BASH,
                str(REPO / ".ai/skills/requirement-to-rule/scripts/prova-arch.sh"),
                "tests/Arch/ModelsTest.php",
                "app/Models/ViolacaoControladaArch.php",
                str(self.root / "evidence"),
            ],
            cwd=self.project,
            input="<?php namespace App\\Models; class ViolacaoControladaArch {}\n",
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            timeout=30,
        )

    def test_directory_that_covers_the_actual_test(self):
        for directory in ("tests", "tests/Arch"):
            with self.subTest(directory=directory):
                result = self.prove('<testsuite name="Arch"><directory>' + directory + "</directory></testsuite>")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(result.stdout, "")
                self.assertFalse((self.project / "app/Models/ViolacaoControladaArch.php").exists())

    def test_directory_suffix_must_match_the_test_filename(self):
        for suffix, expected in (("Test.php", 0), (".php", 0), (".phpt", 1)):
            with self.subTest(suffix=suffix):
                result = self.prove(
                    '<testsuite name="Arch"><directory suffix="' + suffix + '">tests/Arch</directory></testsuite>'
                )
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_excluded_test_or_directory_is_not_covered(self):
        for excluded in ("tests/Arch", "tests/Arch/ModelsTest.php"):
            with self.subTest(excluded=excluded):
                result = self.prove(
                    '<testsuite name="Arch"><directory>tests</directory><exclude>'
                    + excluded + "</exclude></testsuite>"
                )
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("nenhuma", result.stdout)

    def test_explicit_file_is_covered(self):
        result = self.prove('<testsuite name="Arch"><file>tests/Arch/ModelsTest.php</file></testsuite>')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_exclusion_in_one_suite_does_not_exclude_other_suites(self):
        result = self.prove(
            '<testsuite name="Unit"><directory>tests</directory><exclude>tests/Arch</exclude></testsuite>'
            '<testsuite name="Arch"><directory>tests/Arch</directory></testsuite>'
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
